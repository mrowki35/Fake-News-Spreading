import math
import solara

from models.DisinformationModel import (
    DisinformationModel,
    State,
    number_infected,
)

from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)

def agent_portrayal(agent):
    node_color_dict = {
        State.SUSCEPTIBLE: "tab:green",
        State.EXPOSED: "tab:blue",
        State.INFECTED: "tab:red",
        State.DOUBTFUL: "tab:orange",
        State.RECOVERED: "tab:gray",
    }
    return {
        "color": node_color_dict.get(agent.state, "black"),
        "size": 10,
        "tooltip": f"Agent {agent.unique_id}<br>State: {agent.state.name}",
    }

"""
def get_model_summary(model):
    ratio = model.resistant_susceptible_ratio() if hasattr(model, "resistant_susceptible_ratio") else None
    ratio_text = r"$\infty$" if ratio is math.inf else f"{ratio:.2f}" if ratio is not None else "N/A"
    infected_text = str(number_infected(model)) if number_infected else "N/A"

    return solara.Markdown(
        f"Resistant/Susceptible Ratio: {ratio_text}<br>Infected Remaining: {infected_text}"
    )
"""
# Parameter controls
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "threshold_SE": {
        "type": "InputText",
        "value": 1,
        "label": "threshold_SE",
    },
    "threshold_EI": {
        "type": "InputText",
        "value": 1,
        "label": "threshold_EI",
    },
    "threshold_ED": {
        "type": "InputText",
        "value": 1,
        "label": "threshold_ED",
    },
    "threshold_IR": {
        "type": "InputText",
        "value": 1,
        "label": "threshold_IR",
    },
    "threshold_DE": {
        "type": "InputText",
        "value": 1,
        "label": "threshold_ED",
    },
    "num_agents": Slider(
        label="Number of Agents",
        value=100,
        min=10,
        max=1000,
        step=10,
    ),
    "initial_outbreak_size": Slider(
        label="Initial Infected",
        value=5,
        min=1,
        max=100,
        step=1,
    ),
    "initial_exposed_size": Slider(
        label="Initial Exposed",
        value=5,
        min=1,
        max=100,
        step=1,
    ),
    "initial_doubtful_size": Slider(
        label="Initial Doubtful",
        value=5,
        min=1,
        max=100,
        step=1,
    ),
    "initial_recovered_size": Slider(
        label="Initial Recovered",
        value=5,
        min=1,
        max=100,
        step=1,
    ),
    "age_weight": Slider(
        label="Age Influence Weight",
        value=1.0,
        min=0.0,
        max=2.0,
        step=0.1,
    ),
    "education_weight": Slider(
        label="Education Influence Weight",
        value=1.0,
        min=0.0,
        max=2.0,
        step=0.1,
    ),
    "sex_weight": Slider(
        label="Sex Influence Weight",
        value=0.1,
        min=0.0,
        max=1.0,
        step=0.05,
    ),
}

# Visualization components
SpacePlot = make_space_component(agent_portrayal)
StatePlot = make_plot_component(
    {
        "Susceptible": "tab:green",
        "Exposed": "tab:blue",
        "Infected": "tab:red",
        "Doubtful": "tab:orange",
        "Recovered": "tab:gray",
    },
    post_process=lambda ax: (ax.set_ylim(ymin=0), ax.set_ylabel("# Agents")),
)

model =  DisinformationModel()
# SolaraViz app
page = SolaraViz(
   model,
    components=[
        SpacePlot,
        StatePlot,
        #get_model_summary,
    ],
    model_params=model_params,
    name="Disinformation Model",
)

page  # For notebook or script entrypoint
