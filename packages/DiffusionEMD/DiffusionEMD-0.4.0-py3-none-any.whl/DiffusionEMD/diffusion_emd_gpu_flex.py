"""
This calculates the DiffusionEMD using pytorch which is automatically
differentiable. We will then examine the gradients of the DiffusionEMD with
respect to the points.

The first version here uses a KNN graph.
"""
import numpy as np
import time
import torch
from torch_cluster import knn_graph
from torch_sparse import matmul
from torch_geometric.nn.conv.gcn_conv import gcn_norm
from torch_geometric.nn.conv import MessagePassing, ChebConv
from torch_geometric.data import Data
from torch_geometric.transforms import Compose
from torch_geometric.typing import OptTensor
from torch_geometric.utils import (
    to_undirected,
    remove_self_loops,
    get_laplacian,
)
from torch_geometric.utils.num_nodes import maybe_num_nodes
from torch_scatter import scatter_add

from typing import Optional

from DiffusionGAN.diffusion_emd import DiffusionEMD, DiffusionCheb

torch.autograd.set_detect_anomaly(True)


def add_self_loops(
    edge_index,
    edge_weight: Optional[torch.Tensor] = None,
    fill_value: float = 1.0,
    num_nodes: Optional[int] = None,
):
    r"""Adds a self-loop :math:`(i,i) \in \mathcal{E}` to every node
    :math:`i \in \mathcal{V}` in the graph given by :attr:`edge_index`.
    In case the graph is weighted, self-loops will be added with edge weights
    denoted by :obj:`fill_value`. Altered from standard pytorch_geometric
    version, for multi-dimensional edge_weights
    Args:
        edge_index (LongTensor): The edge indices.
        edge_weight (Tensor, optional): Multi-dimensional edge weights.
            (default: :obj:`None`)
        fill_value (float, optional): If :obj:`edge_weight` is not :obj:`None`,
            will add self-loops with edge weights of :obj:`fill_value` to the
            graph. (default: :obj:`1.`)
        num_nodes (int, optional): The number of nodes, *i.e.*
            :obj:`max_val + 1` of :attr:`edge_index`. (default: :obj:`None`)
    :rtype: (:class:`LongTensor`, :class:`Tensor`)
    """
    N = maybe_num_nodes(edge_index, num_nodes)

    loop_index = torch.arange(0, N, dtype=torch.long, device=edge_index.device)
    loop_index = loop_index.unsqueeze(0).repeat(2, 1)

    if edge_weight is not None:
        # Line changed from edge_weight.numel() to edge_weight.size(0) for
        # multi-dimensional edge_weight as well as loop weights are filled fully
        assert edge_weight.size(0) == edge_index.size(1)
        if edge_weight.ndim > 1:
            loop_weight = edge_weight.new_full((N, edge_weight.size(1)), fill_value)
        else:
            loop_weight = edge_weight.new_full((N,), fill_value)
        print(edge_index.shape)
        print(edge_weight.shape)
        edge_weight = torch.cat([edge_weight, loop_weight], dim=0)
        print(edge_weight.shape)

    edge_index = torch.cat([edge_index, loop_index], dim=1)
    print(edge_index.shape)

    return edge_index, edge_weight


class ToUndirected(object):
    """Converts the graph to an undirected graph, so that
    :math:`(j,i) \in \mathcal{E}` for every edge :math:`(i,j) \in \mathcal{E}`.
    """

    def __call__(self, data):
        if "edge_index" in data:
            data.edge_index = to_undirected(data.edge_index, data.num_nodes)
        if "adj_t" in data:
            data.adj_t = data.adj_t.to_symmetric()
        return data

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class Diffuse(MessagePassing):
    # TODO we might want to investigate fixing the parameters of a ChebConv layer provided in pytorch_geometric
    def __init__(self, node_dim=-3):
        super().__init__(aggr="add", node_dim=node_dim)  # "Add" aggregation.

    def forward(self, x, edge_index, edge_weight=None):
        edge_index, edge_weight = gcn_norm(
            edge_index,
            edge_weight,
            x.size(self.node_dim),
            dtype=x.dtype,
            add_self_loops=False,
        )
        propogated = self.propagate(
            edge_index, edge_weight=edge_weight, size=None, x=x,
        )
        # Lazy random walks???
        return 0.5 * (x + propogated)

    def message(self, x_j, edge_weight):
        return edge_weight[:, None, :] * x_j

    def message_and_aggregate(self, adj_t, x):
        return matmul(adj_t, x, reduce=self.aggr)

    def update(self, aggr_out):
        return aggr_out


class Kernel(object):
    def __init__(self, radii=0.1):
        self.radii = radii

    def __call__(self, data):
        # TODO would it be useful to use multiple radius kernels?
        (row, col), pos = data.edge_index, data.pos
        # norms = torch.norm(pos[col] - pos[row], p=2, dim=1)
        # exponent = -torch.norm(pos[col] - pos[row], p=2, dim=1)[:, None] / (2 * self.radii[None, :] ** 2)
        # Clamping is necesary to prevent underflow
        cart = torch.clamp(
            torch.exp(
                -torch.norm(pos[col] - pos[row], p=2, dim=1)[:, None]
                / (2 * self.radii[None, :] ** 2)
            ),
            min=1e-4,
        )
        # ), min=1e-8)
        cart = cart.view(-1, 1) if cart.dim() == 1 else cart
        data.edge_attr = cart
        return data


class ChebConvFixed(MessagePassing):
    def __init__(self, input_dim, coeffs, normalization="sym", **kwargs):
        super().__init__(**kwargs)
        self.node_dim = 0
        assert normalization in [None, "sym", "rw"], "Invalid normalization"

        self.coeffs = coeffs
        # TODO (alex) could be faster with better broadcasting
        # self.coeffs = self.coeffs.repeat(1, input_dim, 1)
        self.normalization = normalization

    def __norm__(
        self,
        edge_index,
        num_nodes: Optional[int],
        edge_weight: OptTensor,
        normalization: Optional[str],
        lambda_max,
        dtype: Optional[int] = None,
        batch: OptTensor = None,
    ):
        row, col = edge_index[0], edge_index[1]
        deg = scatter_add(edge_weight, row, dim=0, dim_size=num_nodes)
        deg_inv_sqrt = deg.pow_(-0.5)
        deg_inv_sqrt.masked_fill_(deg_inv_sqrt == float("inf"), 0)
        edge_weight = deg_inv_sqrt[row] * edge_weight * deg_inv_sqrt[col]
        if batch is not None and lambda_max.numel() > 1:
            lambda_max = lambda_max[batch[edge_index[0]]]
        assert edge_weight is not None
        return edge_index, edge_weight

    def forward(self, data, lambda_max=None):
        x, edge_index, edge_weight = data.x, data.edge_index, data.edge_attr
        if self.normalization != "sym" and lambda_max is None:
            raise ValueError(
                "You need to pass `lambda_max` to `forward() in`"
                "case the normalization is non-symmetric."
            )
        edge_index, edge_weight = remove_self_loops(edge_index, edge_weight)
        row = edge_index[0]
        deg = scatter_add(edge_weight, row, dim=0, dim_size=x.size(self.node_dim))
        self.deg_sqrt = deg.pow(0.5)
        x = torch.einsum("nr,ndr->ndr", deg.pow(-0.5), x)

        if lambda_max is None:
            lambda_max = torch.tensor(2.0, dtype=x.dtype, device=x.device)
        if not isinstance(lambda_max, torch.Tensor):
            lambda_max = torch.tensor(lambda_max, dtype=x.dtype, device=x.device)
        assert lambda_max is not None

        edge_index, norm = self.__norm__(
            edge_index,
            x.size(self.node_dim),
            edge_weight,
            self.normalization,
            lambda_max,
            dtype=x.dtype,
            batch=None,
        )

        Tx_0 = x
        Tx_1 = x  # Dummy.
        out = torch.einsum("ndr,s->sndr", Tx_0, self.coeffs[0])
        Tx_1 = self.propagate(edge_index, x=x, norm=norm, size=None)

        out = out + torch.einsum("ndr,s->sndr", Tx_1, self.coeffs[1])
        for k in range(2, self.coeffs.shape[0]):
            Tx_2 = self.propagate(edge_index, x=Tx_1, norm=norm, size=None)
            Tx_2 = 2.0 * Tx_2 - Tx_0
            out = out + torch.einsum("ndr,s->sndr", Tx_2, self.coeffs[k])
            Tx_0, Tx_1 = Tx_1, Tx_2
        return out

    def message(self, x_j, norm):
        return norm[:, None, :] * x_j


class DiffusionChebGPU(DiffusionCheb):
    def _get_coeffs(self):
        kernels = [lambda x, s=s: np.minimum((1 - x) ** s, 1) for s in self.scales]
        # Assumes the normalized laplacian
        a_arange = [0, 2]
        a1 = (a_arange[1] - a_arange[0]) / 2
        a2 = (a_arange[1] + a_arange[0]) / 2
        c = np.zeros((len(self.scales), self.cheb_order + 1))
        tmpN = np.arange(self.N)
        num = np.cos(np.pi * (tmpN + 0.5) / self.N)
        for s in range(len(self.scales)):
            for o in range(self.cheb_order + 1):
                c[s, o] = (
                    2.0
                    / self.N
                    * np.dot(
                        kernels[s](a1 * num + a2),
                        np.cos(np.pi * o * (tmpN + 0.5) / self.N),
                    )
                )
        return c.T

    def __call__(self, data):
        diffusions = [data.x]
        self.N = data.x.shape[0]
        coeffs = torch.tensor(self._get_coeffs(), dtype=torch.float32).to(data.x.device)
        conv = ChebConvFixed(data.edge_attr.shape[1], coeffs)
        # diffusions are of shape [n_nodes, n_distributions, n_scales]
        diffusions = conv(data)
        # Renormalize by degree to convert to markov matrix
        diffusions = diffusions * conv.deg_sqrt[None, :, None, :]
        n_scales, n, n_samples, n_radii = diffusions.shape
        embeddings = []
        for k in range(n_scales):
            d = diffusions[k]
            if k < n_scales - 1:
                d -= diffusions[k + 1]
            weight = 0.5 ** ((n_scales - k - 1) * self.alpha)
            lvl_embed = weight * d
            embeddings.append(lvl_embed)
        embeddings = torch.stack(embeddings, dim=-1)
        # embeddings are of shape [n_distributions, n_nodes, n_radii, n_scales]
        embeddings.transpose_(0, 1)
        return torch.sum(torch.abs(embeddings[0] - embeddings[1]))

    def transform(self, y):
        raise NotImplementedError

    def fit(self, X):
        raise NotImplementedError

    def _compute_rank(self):
        raise NotImplementedError


class DiffusionSmallGPU(DiffusionEMD):
    def __call__(self, data):
        diff_layer = Diffuse()
        diffusions = [data.x]
        for i in range(16):
            diffusions.append(
                diff_layer(diffusions[-1], data.edge_index, data.edge_attr)
            )
        diffusions = torch.stack(diffusions)
        selections = torch.tensor([0, 1, 2, 4, 8, 16])

        # dyadic_diffusions are of shape [n_scales, n_nodes, n_distributions, n_radii]
        dyadic_diffusions = diffusions[selections]
        embeddings = []
        n_scales = len(selections)
        for k in range(n_scales):
            d = dyadic_diffusions[k]
            if k < n_scales - 1:
                d -= diffusions[k + 1]
            weight = 0.5 ** ((n_scales - k - 1) * self.alpha)
            lvl_embed = weight * d
            embeddings.append(lvl_embed)
        embeddings = torch.stack(embeddings, dim=-1)
        # embeddings are of shape [n_distributions, n_nodes, n_radii, n_scales]
        embeddings.transpose_(0, 1)
        return torch.sum(torch.abs(embeddings[0] - embeddings[1]))

    def transform(self, y):
        raise NotImplementedError

    def fit(self, X):
        raise NotImplementedError

    def _compute_rank(self):
        raise NotImplementedError


def to_graph_and_labels(data_list, k=10, num_workers=1, radii=None):
    """ Converts a list of pointsets to a unified graph with label vector

    Parameters
    ----------
    data_list:
        list of tensors containing datapoints on the cpu, the GPU
        implementation of nearest neighbor search in torch_cluster is currently
        much slower.

    Returns
    -------
    graph:
        pytorch_geoemtric Data object representing a graph. Signals on this
        graph label the pointsets.

    """
    if radii is None:
        # radii = torch.tensor([1])
        # radii = torch.tensor([0.1, 1, 2])
        radii = torch.tensor([0.1, 0.2, 0.3, 0.5, 1, 10])
    # Construct the 1-hot distribution matrix
    labels = []
    for i, data in enumerate(data_list):
        labels.append(torch.ones(data.shape[0], dtype=torch.int64) * i)
    labels = torch.cat(labels, dim=0)

    labels_onehot = torch.zeros(labels.shape[0], len(data_list))
    labels_onehot.scatter_(1, labels.unsqueeze(1), 1.0)
    labels_onehot = labels_onehot / (labels_onehot.sum(dim=0)[None, :])

    # Construct the graph using k nearest neighbors
    pos = torch.cat(data_list, dim=0)

    batch = torch.zeros(pos.shape[0], dtype=torch.int64)
    edge_index = knn_graph(pos, k=10, batch=batch, loop=False, num_workers=num_workers)
    data = Data(
        x=labels_onehot[:, :, None].repeat(1, 1, radii.shape[0]),
        pos=pos,
        edge_index=edge_index,
    )
    transform = Compose([ToUndirected(), Kernel(radii=radii)])
    data = transform(data)
    return data


# def np_to_torch(graph, signals


def diffemd_loss(data):
    """ Function to compute the loss with respect the DiffusionEMD between two
    sets of points.

    Parameters
    ----------
    input:
        Tensor of arbitrary shape
    target:
        Tensor of the same shape as input
    """
    diff_layer = Diffuse()
    diffusions = [data.x]
    for i in range(16):
        diffusions.append(diff_layer(diffusions[-1], data.edge_index, data.edge_attr))
    diffusions = torch.stack(diffusions)
    selections = torch.tensor([0, 1, 2, 4, 8, 16])

    # dyadic_diffusions are of shape [n_scales, n_nodes, n_distributions, n_radii]
    dyadic_diffusions = diffusions[selections]
    embeddings = []
    n_scales = len(selections)
    for k in range(n_scales):
        d = dyadic_diffusions[k]
        if k < n_scales - 1:
            d -= diffusions[k + 1]
        weight = 0.5 ** ((n_scales - k - 1) * alpha)
        lvl_embed = weight * d
        embeddings.append(lvl_embed)
    embeddings = torch.stack(embeddings, dim=-1)
    # embeddings are of shape [n_distributions, n_nodes, n_radii, n_scales]
    embeddings.transpose_(0, 1)
    return torch.sum(torch.abs(embeddings[0] - embeddings[1]))


if __name__ == "__main__":
    torch.set_printoptions(precision=2)
    torch.manual_seed(42)
    np.random.seed(42)
    n = 1000
    input = torch.randn((n, 2), requires_grad=True)
    # input = torch.randn((n, 2), requires_grad=True)
    target = torch.rand((n, 2), requires_grad=False)
    # for device in ["cuda"]:
    hist = []
    for device in ["cpu"]:  # , "cuda"]:
        print(device)
        loss_fn = DiffusionChebGPU(cheb_order=16, n_scales=5, alpha=0.5, max_scale=5)
        # loss_fn = DiffusionSmallGPU(alpha=0.5)
        # hist = [input.detach().clone()]
        optimizer = torch.optim.SGD([input], lr=1)
        start = time.time()
        for step in range(1, 1000 + 1):
            data = to_graph_and_labels([input, target]).to(device)
            loss = loss_fn(data)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            hist.append(input.detach().clone())
            if step % 10 == 0:
                end = time.time()
                print(
                    "iter: %d, time: %0.2f, loss: %0.3f"
                    % (step, end - start, loss.item())
                )
                start = end
        hist = torch.stack(hist)
        hist = hist.detach().numpy()
    """
    for device in ["cpu", "cuda"]:
        print(device)
        # loss_fn = DiffusionChebGPU(cheb_order=16, n_scales=5, alpha=0.5, max_scale=5)
        loss_fn = DiffusionSmallGPU(alpha=0.5)
        # hist = [input.detach().clone()]
        optimizer = torch.optim.SGD([input], lr=1)
        start = time.time()
        for step in range(1, 10 + 1):
            data = to_graph_and_labels([input, target]).to(device)
            loss = loss_fn(data)
            # loss.backward()
            # optimizer.step()
            # optimizer.zero_grad()
            # hist.append(input.detach().clone())
            if step % 10 == 0:
                end = time.time()
                print(
                    "iter: %d, time: %0.2f, loss: %0.3f"
                    % (step, end - start, loss.item())
                )
                start = end

    """
    np.save("hist_cheb.npy", hist)
    np.save("target_cheb.npy", target.numpy())
