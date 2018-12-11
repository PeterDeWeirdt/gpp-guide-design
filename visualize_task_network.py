import numpy as np
import pandas as pd
import holoviews as hv
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import random
import matplotlib.pyplot as plt


def build_task_graph(hash, hash_data, node_info, sources, targets, old_tuple, position):
    """ Recursively build a task graph from hash data
    :param hash_data:
    :param node_info:
    :param sources:
    :param targets:
    :return:
    """
    hash_row = hash_data[hash_data.Hash == hash]
    node_info[hash] = hash_row['Node'].to_string(index=False)
    position[hash] = old_tuple
    new_tuple = (old_tuple[0] + random.uniform(-1, 1), old_tuple[1] - 0.15, )

    if not hash_row['Deps'].isnull().bool():
        for source in hash_row['Deps'].str.split('|').tolist()[0]:
            sources.append(source)
            targets.append(hash)
            node_info, sources, targets, position = build_task_graph(source, hash_data,
                                                           node_info, sources,
                                                           targets, new_tuple,
                                                           position)
    return node_info, sources, targets, position

if __name__ == '__main__':
    hash = 'f27f1337'
    hash_data = pd.read_table('./data/hash.txt')
    node_info, sources, targets, position = build_task_graph(hash, hash_data,
                                                             {}, [], [], (0,1), {})
    graph_df = pd.DataFrame({'target': targets, 'source': sources}).drop_duplicates()
    g = nx.from_pandas_edgelist(graph_df, 'source', 'target',
                                create_using=nx.DiGraph)
    node_color = {}
    for node in node_info.keys():
        if node == hash:
            node_color[node] = 'Final Output'
        else:
            node_color[node] = 'Interim'
    nx.set_node_attributes(g, node_info, 'Node Info')
    nx.set_node_attributes(g, node_color, 'Node Type')
    write_dot(g, 'data/hash_nets/' + hash + '.dot')
    plt.title(hash)
    pos = graphviz_layout(g, prog='dot')
    nx.draw(g, pos, with_labels=True, arrows = True)
    plt.savefig('data/hash_nets/' + hash + '.pdf')

    padding = dict(x=(-1.2, 1.2), y=(-1.2, 1.2))
    renderer = hv.renderer('bokeh').instance(fig='html', holomap='auto')
    g_hv = hv.Graph.from_networkx(g, nx.layout.kamada_kawai_layout).redim.range(**padding) \
        .options(color_index='Node Type', cmap=['#e41a1c', '#377eb8'], directed = True,
                 arrowhead_length=0.015, node_alpha =0.4, edge_line_width = 0.7,
                 node_size = 10)
    renderer.save(g_hv, 'data/hash_nets/' + hash)
