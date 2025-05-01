import math
import networkx as nx
from mesa import Model
from mesa.experimental.cell_space.cell_collection import CellCollection
from mesa.experimental.cell_space.network import Network
from mesa.datacollection import DataCollector

from agents.UserAgent import UserAgent, State
from enums.groups.AgeGroup import AgeGroup
from enums.groups.EducationGroup import EducationGroup


# State counters
def number_state(model, state):
    return sum(1 for a in model.grid.all_cells.agents if a.state is state)

def number_infected(model):
    return number_state(model, State.INFECTED)

def number_susceptible(model):
    return number_state(model, State.SUSCEPTIBLE)

def number_exposed(model):
    return number_state(model, State.EXPOSED)

def number_doubtful(model):
    return number_state(model, State.DOUBTFUL)

def number_recovered(model):
    return number_state(model, State.RECOVERED)


class DisinformationModel(Model):
    def __init__(
        self,
        num_nodes=10,
        avg_node_degree=3,
        initial_outbreak_size=1,
        # demographic influence weights
        age_weight=1.0,
        education_weight=1.0,
        sex_weight=1.0,
        # state transition thresholds
        threshold_SE=1.5,
        threshold_EI=1.2,
        threshold_ED=1.0,
        threshold_IR=1.3,
        threshold_DE=1.4,
        seed=None,
    ):
        super().__init__(seed=seed)

        # Model parameters
        self.num_nodes = num_nodes
        self.age_weight = age_weight
        self.education_weight = education_weight
        self.sex_weight = sex_weight

        self.threshold_SE = threshold_SE
        self.threshold_EI = threshold_EI
        self.threshold_ED = threshold_ED
        self.threshold_IR = threshold_IR
        self.threshold_DE = threshold_DE

        self.initial_outbreak_size = min(initial_outbreak_size, num_nodes)

        # Build graph and network
        prob = avg_node_degree / num_nodes
        graph = nx.erdos_renyi_graph(n=num_nodes, p=prob)
        self.grid = Network(graph, capacity=1, random=self.random)

        # Data collection
        self.datacollector = DataCollector(
            {
                "Infected": number_infected,
                "Susceptible": number_susceptible,
                "Recovered": number_recovered,
                "Exposed": number_exposed,
                "Doubtful": number_doubtful,
            }
        )

        # Create agents
        for node, cell in zip(graph.nodes, self.grid.all_cells):
            age_group = self.random.choice(list(AgeGroup))
            education_group = self.random.choice(list(EducationGroup))
            sex_group = self.random.choice([0, 1])  # 0 = female, 1 = male

            agent = UserAgent(
                model=self,
                unique_id=node,
                initial_state=State.SUSCEPTIBLE,
                age_group=age_group,
                education_group=education_group,
                sex_group=sex_group,
                cell=cell,
            )
            cell.agents.append(agent)

        # Infect a few
        infected_cells = CellCollection(
            self.random.sample(list(self.grid.all_cells), self.initial_outbreak_size),
            random=self.random,
        )
        for a in infected_cells.agents:
            a.state = State.INFECTED

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
