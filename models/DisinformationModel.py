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
    MODERATION_INFLUENCE = 2.0
    graph = None
    prob = 0.0
    seed = 0

    def __init__(
        self,
        num_agents=100,
        avg_node_degree=3,
        initial_outbreak_size=1,
        initial_exposed_size=15,
        initial_doubtful_size=15,
        initial_recovered_size=10,
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
        # switches for scenarios
        moderation=0
    ):
        super().__init__(seed=seed)

        self.num_agents = num_agents
        self.age_weight = age_weight
        self.education_weight = education_weight
        self.sex_weight = sex_weight

        if moderation:
            self.threshold_SE = float(threshold_SE) * DisinformationModel.MODERATION_INFLUENCE
        else:
            self.threshold_SE = float(threshold_SE)
        self.threshold_EI = float(threshold_EI)
        self.threshold_ED = float(threshold_ED)
        self.threshold_IR = float(threshold_IR)
        self.threshold_DE = float(threshold_DE)

        # Safety check: total of all initial states cannot exceed total agents
        total_initial = (
            initial_outbreak_size + initial_exposed_size +
            initial_doubtful_size + initial_recovered_size
        )
        if total_initial > num_agents:
            raise ValueError("Initial state counts exceed total number of agents.")

        # Build network
        prob = avg_node_degree / num_agents
        if DisinformationModel.graph is None or num_agents != DisinformationModel.graph.number_of_nodes() or DisinformationModel.prob != prob or DisinformationModel.seed != seed:
            DisinformationModel.seed = seed
            DisinformationModel.prob = prob
            DisinformationModel.graph = nx.erdos_renyi_graph(n=num_agents, p=prob)
        self.grid = Network(DisinformationModel.graph, capacity=1, random=self.random)

        self.datacollector = DataCollector(
            {
                "Infected": number_infected,
                "Susceptible": number_susceptible,
                "Recovered": number_recovered,
                "Exposed": number_exposed,
                "Doubtful": number_doubtful,
            }
        )

        # Create all agents as SUSCEPTIBLE first
        all_cells = list(self.grid.all_cells)
        for node, cell in zip(DisinformationModel.graph.nodes, all_cells):
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

        # Assign initial states to random agents
        state_assignments = [
            (initial_outbreak_size, State.INFECTED),
            (initial_exposed_size, State.EXPOSED),
            (initial_doubtful_size, State.DOUBTFUL),
            (initial_recovered_size, State.RECOVERED),
        ]

        remaining_cells = CellCollection(all_cells, random=self.random)

        for count, state in state_assignments:
            if count > 0:
                selected = CellCollection(
                    self.random.sample(list(remaining_cells), count),
                    random=self.random
                )
                for a in selected.agents:
                    a.state = state
                # Remove already assigned cells from the pool
                remaining_cells = CellCollection(
                    [c for c in remaining_cells if c not in selected],
                    random=self.random
                )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
