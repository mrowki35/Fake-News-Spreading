from enum import Enum


class State(Enum):
    SUSCEPTIBLE = 0
    EXPOSED = 1
    INFECTED = 2
    DOUBTFUL = 3
    RECOVERED = 4
