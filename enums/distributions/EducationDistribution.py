from enums.groups.EducationGroup import EducationGroup
from enums.State import State

EducationDistribution = {
    State.SUSCEPTIBLE: {
        EducationGroup.PRIMARY: 0.02,
        EducationGroup.SECONDARY: 0.18,
        EducationGroup.HIGHER: 0.75,
        EducationGroup.VOCATIONAL: 0.05,
    },
    State.EXPOSED: {
        EducationGroup.PRIMARY: 0.10,
        EducationGroup.SECONDARY: 0.40,
        EducationGroup.HIGHER: 0.45,
        EducationGroup.VOCATIONAL: 0.05,
    },
     State.INFECTED: {
        EducationGroup.PRIMARY: 0.05,
        EducationGroup.SECONDARY: 0.30,
        EducationGroup.HIGHER: 0.60,
        EducationGroup.VOCATIONAL: 0.05,
    },
    State.DOUBTFUL: {
        EducationGroup.PRIMARY: 0.03,
        EducationGroup.SECONDARY: 0.27,
        EducationGroup.HIGHER: 0.65,
        EducationGroup.VOCATIONAL: 0.05,
    },
    State.RECOVERED: {
        EducationGroup.PRIMARY: 0.04,
        EducationGroup.SECONDARY: 0.35,
        EducationGroup.HIGHER: 0.55,
        EducationGroup.VOCATIONAL: 0.06,
    }
}