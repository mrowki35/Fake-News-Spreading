import networkx as nx
from mesa import Agent, Model
from mesa.datacollection import DataCollector
import random
from agents.UserAgent import UserAgent

class DisinformationModel(Model):
    def __init__(self, num_agents=100):
        self.num_agents = num_agents
        self.G = nx.Graph()  # Tworzenie grafu (przestrzeń)
        self.schedule = []  # Lista agentów
        self.datacollector = DataCollector(
            model_reporters={
                "Exposed": lambda m: sum(
                    1 for a in m.schedule if a.state.name == "EXPOSED"
                ),
                "Infected": lambda m: sum(
                    1 for a in m.schedule if a.state.name == "INFECTED"
                ),
            }
        )

        # Tworzenie agentów i dodawanie ich do grafu oraz listy
        for i in range(self.num_agents):
            agent = UserAgent(i, self)
            self.schedule.append(agent)  # Dodaj agenta do listy
            self.G.add_node(i, agent=agent)  # Dodaj węzeł do grafu

        # Dodawanie krawędzi między agentami
        for i in range(self.num_agents):
            for j in range(i + 1, self.num_agents):
                if random.random() < 0.05:  # 5% szansy na krawędź
                    self.G.add_edge(i, j)
                    agent_i = self.G.nodes[i]['agent']
                    agent_j = self.G.nodes[j]['agent']
                    agent_i.add_neighbor(agent_j)
                    agent_j.add_neighbor(agent_i)

    def step(self):
        """Wykonuje krok symulacji dla wszystkich agentów."""
        self.datacollector.collect(self)
        for agent in self.schedule:
            agent.step()
