"""
Graph coordinate utilities for BFMC navigation.
Primary Contributor: NLattas
"""
import networkx as nx
import numpy as np



def load_graph_positions(graph_path: str):
    """
    Load the GraphML and return:
      - node_ids: list of node ids (as strings or ints)
      - coords:  N x 2 numpy array with [x, y] for each node
    """
    G = nx.read_graphml(graph_path)

    # Guess which attributes hold the coordinates
    # Adjust this if you know the exact names
    sample_node, sample_data = next(iter(G.nodes(data=True)))
    if {"x", "y"}.issubset(sample_data.keys()):
        xkey, ykey = "x", "y"
    elif {"X", "Y"}.issubset(sample_data.keys()):
        xkey, ykey = "X", "Y"
    elif {"posx", "posy"}.issubset(sample_data.keys()):
        xkey, ykey = "posx", "posy"
    else:
        raise ValueError(
            f"Could not find position attributes in node data. "
            f"Available keys: {list(sample_data.keys())}"
        )

    node_ids = []
    coords = []
    for nid, data in G.nodes(data=True):
        node_ids.append(nid)  # keep as string; cast to int later if you want
        coords.append([float(data[xkey]), float(data[ykey])])

    coords = np.array(coords, dtype=float)
    return node_ids, coords


def xy_to_nearest_node(x: float, y: float,
                       node_ids, coords) -> str:
    """
    Given a point (x, y) and precomputed node coordinates,
    return the id of the nearest node.
    """
    p = np.array([x, y], dtype=float)
    diffs = coords - p
    dist_sq = np.einsum("ij,ij->i", diffs, diffs)  # squared distance
    idx = np.argmin(dist_sq)
    return node_ids[idx]

def node_id_to_xy(node_id, node_ids, coords):
    """
    Returns the coordinates of the given node.
    """
    try:
        idx = node_ids.index(node_id)
        return coords[idx]
    except:
        print("Error: false input of node")