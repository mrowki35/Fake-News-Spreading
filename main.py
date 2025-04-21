from models.DisinformationModel import DisinformationModel

from mesa.visualization.modules import NetworkModule
from mesa.visualization.ModularVisualization import ModularServer

def network_portrayal(G):
    def node_color(agent):
        color_map = {
            "SUSCEPTIBLE": "#a3c9f1",
            "EXPOSED": "#f0ad4e",
            "INFECTED": "#d9534f",
            "DOUBTFUL": "#9b59b6",
            "RECOVERED": "#5cb85c"
        }
        return color_map.get(agent.state.name, "#7f8c8d")

    portrayal = {
        "nodes": [
            {
                "id": node,
                "color": node_color(G.nodes[node]['agent']),
                "size": 5,
                "label": str(G.nodes[node]['agent'].unique_id)
            }
            for node in G.nodes
        ],
        "edges": [{"source": e[0], "target": e[1]} for e in G.edges]
    }
    return portrayal


network = NetworkModule(network_portrayal, 500, 500)
server = ModularServer(
    DisinformationModel,
    [network],
    "Disinformation Spread Model",
    {"num_agents": 100}
)

server.port = 8521
server.launch()


if __name__ == "__main__":
    pass

