import random
from enums.distributions.AgeDistribution import AgeDistribution
from enums.distributions.EducationDistribution import EducationDistribution
from enums.State import State


class UserAgent:
    def __init__(self, unique_id, model, age_group, sex_group, education_group):
        """
        Initializes a user agent.

        Args:
            unique_id (int): Unique identifier for the agent.
            model (DisinformationModel): Reference to the model.
            age_group (AgeGroup): Age group of the agent.
            sex_group (SexGroup): Sex of the agent.
            education_group (EducationGroup): Education level of the agent.
        """
        self.unique_id = unique_id
        self.model = model
        self.age_group = age_group
        self.sex_group = sex_group
        self.education_group = education_group
        self.state = State.SUSCEPTIBLE 
        self.neighbors = []

    def step(self):
        """
        Method executed in each simulation step.
        Determines state transitions based on probabilities.
        """
        if self.state == State.SUSCEPTIBLE:
            self._susceptible_to_exposed()
        elif self.state == State.EXPOSED:
            self._exposed_transition()
        elif self.state == State.INFECTED:
            self._infected_to_recovered()
        elif self.state == State.DOUBTFUL:
            self._doubtful_to_exposed()
        # RECOVERED is a terminal state; no transitions

    def _susceptible_to_exposed(self):
        """
        Transition from S (Susceptible) to E (Exposed) with probability alpha adjusted by attributes.
        """
        res = random.random(0.9,1.0) * self.model.a*AgeDistribution.get(self.state).get(self.age_group)
        res += random.random(0.9,1.0) * self.model.b*EducationDistribution.get(self.state).get(self.education_group)
        #res += 

        if self.model.susceptible_threshold < res:
            self.state = State.EXPOSED

    def _exposed_transition(self):
        pass
 

    def _infected_to_recovered(self):
        pass

    def _doubtful_to_exposed(self):
        pass

    def __repr__(self):
        return (f"UserAgent(id={self.unique_id}, age_group={self.age_group.name}, "
                f"sex_group={self.sex_group.name}, education_group={self.education_group.name}, "
                f"social_platform={self.social_platform.name}, state={self.state.name})")

    def to_dict(self):
        """
        Returns a dictionary representation of the UserAgent.
        """
        return {
            "ID": self.unique_id,
            "Age Group": self.age_group.name,
            "Sex Group": self.sex_group.name,
            "Education Group": self.education_group.name,
            "State": self.state.name
        }

    def to_string(self):
        """
        Returns a detailed string representation of the UserAgent.
        """
        return (f"UserAgent [ID: {self.unique_id}, Age Group: {self.age_group.name}, "
                f"Sex Group: {self.sex_group.name}, Education Group: {self.education_group.name}, "
                  f"State: {self.state.name}]")
    def add_neighbor(self, other_agent):
        if not hasattr(self, "neighbors"):
            self.neighbors = []
        self.neighbors.append(other_agent)
