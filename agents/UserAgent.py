from mesa.experimental.cell_space.cell_agent import FixedAgent
from enums.distributions.AgeDistribution import AgeDistribution
from enums.distributions.EducationDistribution import EducationDistribution
from enums.State import State

class UserAgent(FixedAgent):
    def __init__(self, model, initial_state, unique_id, age_group, sex_group, education_group,cell):
        super().__init__(model)
        self.state = initial_state
        self.unique_id = unique_id
        self.age_group = age_group
        self.sex_group = sex_group
        self.education_group = education_group
        self.cell = cell

    def get_neighbor_counts(self):
        counts = {state: 0 for state in State}
        for agent in self.cell.neighborhood.agents:
            counts[agent.state] += 1
        N = sum(counts.values())
        return counts, N


    def calculate_transition_score(self, counts, N, signs):
        a = self.model.age_weight
        b = self.model.education_weight
        c = self.model.sex_weight

        # Lookup distribution values based on agent's state and group
        age_score = AgeDistribution[self.state][self.age_group] * a * self.random.uniform(0.9, 1)
        edu_score = EducationDistribution[self.state][self.education_group] * b * self.random.uniform(0.9, 1)
        sex_score = self.sex_group * c * self.random.uniform(0.05, 0.1)

        neighbor_score = sum(
            (signs[state] * counts[state] / N) if N > 0 else 0
            for state in signs
        )

        return age_score + edu_score + sex_score + neighbor_score

    def step(self):
        counts, N = self.get_neighbor_counts()

        if self.state == State.SUSCEPTIBLE:
            # Transition S -> E
            signs = {State.EXPOSED: +1, State.INFECTED: +1, State.DOUBTFUL: -1, State.RECOVERED: -1}
            score = self.calculate_transition_score(counts, N, signs)
            if score > float(self.model.threshold_SE):
                self.state = State.EXPOSED

        elif self.state == State.EXPOSED:
            # Transition E -> I
            signs_EI = {State.EXPOSED: +1, State.INFECTED: +1, State.DOUBTFUL: -1, State.RECOVERED: -1}
            score_EI = self.calculate_transition_score(counts, N, signs_EI)
            if score_EI > float(self.model.threshold_EI):
                self.state = State.INFECTED
                return

            # Transition E -> D
            signs_ED = {State.EXPOSED: -1, State.INFECTED: -1, State.DOUBTFUL: +1, State.RECOVERED: +1}
            score_ED = self.calculate_transition_score(counts, N, signs_ED)
            if score_ED > float(self.model.threshold_ED):
                self.state = State.DOUBTFUL

        elif self.state == State.INFECTED:
            # Transition I -> R
            signs = {
                State.EXPOSED: -1,
                State.INFECTED: -1,
                State.DOUBTFUL: +1,
                State.RECOVERED: +1,
                State.SUSCEPTIBLE: -1
            }
            score = self.calculate_transition_score(counts, N, signs)
            if score > float(self.model.threshold_IR):
                self.state = State.RECOVERED

        elif self.state == State.DOUBTFUL:
            # Transition D -> E
            signs = {
                State.EXPOSED: +1,
                State.INFECTED: +1,
                State.DOUBTFUL: -1,
                State.RECOVERED: -1,
                State.SUSCEPTIBLE: +1
            }
            score = self.calculate_transition_score(counts, N, signs)
            if score > float(self.model.threshold_DE):
                self.state = State.EXPOSED

