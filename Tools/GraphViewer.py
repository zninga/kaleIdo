import os
import tempfile

from graphviz import Digraph, Graph


class GraphViewer:
    def view(self, graph, is_directed_graph=True, fmt="png"):
        if not isinstance(graph, dict):
            raise TypeError("expected dict")

        G = Digraph() if is_directed_graph else Graph()
        self.graph = G
        nodes = set()
        edges = []

        for k, v in graph.items():
            nodes.add(k)
            nodes.add(v) if not isinstance(v, list) else nodes.update(v)

        node_id = {}
        for k in nodes:
            node_id[k] = str(len(node_id))
            G.node(node_id[k], str(k))

        p = set()
        if is_directed_graph:
            for k, v in graph.items():
                t = v.copy() if isinstance(v, list) else [v]
                for x in t:
                    er = [node_id[k], node_id[x]]
                    s = "-".join(er)
                    if s not in p:
                        p.add(s)
                        edges.append(er)
        else:
            for k, v in graph.items():
                t = v.copy() if isinstance(v, list) else [v]
                for x in t:
                    er = [node_id[k], node_id[x]]
                    s1 = "-".join(er)
                    s2 = "-".join(er[::-1])
                    if s1 not in p and s2 not in p:
                        p.update({s1, s2})
                        edges.append(er)
        G.edges(edges)
        G.format = fmt
        G.view(os.path.basename(tempfile.mktemp()), cleanup=True)