from streamlit_agraph import Node, Edge

def nx_to_agraph(graph):
    nodes = []
    edges = []

    for node, data in graph.nodes(data=True):
        nodes.append(
            Node(
                id=str(node),
                label=str(node),
                size=20,
                color="#00A8E8"
            )
        )

    for source, target, data in graph.edges(data=True):
        edges.append(
            Edge(
                source=str(source),
                target=str(target),
                label=data.get("type", "")
            )
        )

    return nodes, edges