import agentpy as ap
import random
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# -------- Agent Definition -----------
class RandomWalker(ap.Agent):
    def setup(self):
        self.position = (0, 0)
        self.path = [self.position]

    def step(self):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        occupied = {other.position for other in self.model.agents
                    if other is not self}

        if self.model.p.preferred_direction:
            preferred = self.model.p.preferred_direction
            directions = [preferred] + [d for d in directions if d != preferred]
        else:
            random.shuffle(directions)

        x, y = self.position
        candidates = []
        for dx, dy in directions:
            candidate = (
                max(0, min(self.model.p.grid_size[0] - 1, x + dx)),
                max(0, min(self.model.p.grid_size[1] - 1, y + dy)),
            )
            if candidate != self.position and (
                not self.model.p.avoid_agents or candidate not in occupied
            ):
                candidates.append(candidate)

        if candidates:
            self.position = candidates[0]
        self.path.append(self.position)

# -------- Model Definition -----------
class RandomWalkModel(ap.Model):
    def setup(self):
        self.agents = ap.AgentList(self, self.p.agents, RandomWalker)

        positions = set()
        for agent in self.agents:
            position = (random.randrange(self.p.grid_size[0]),
                        random.randrange(self.p.grid_size[1]))
            while self.p.avoid_agents and position in positions:
                position = (random.randrange(self.p.grid_size[0]),
                            random.randrange(self.p.grid_size[1]))
            positions.add(position)
            agent.position = position
            agent.path = [position]

        # Create grid (optional)
        self.grid = ap.Grid(self, self.p.grid_size, torus=False)
        self.grid.add_agents(self.agents)

    def step(self):
        for agent in self.agents:
            agent.step()

def run_scenario(name, parameters):
    model = RandomWalkModel(parameters)
    model.setup()
    for _ in range(parameters["steps"]):
        model.step()
    return name, model


def analyze_final_positions(model):
    positions = [agent.position for agent in model.agents]
    counts = Counter(positions)
    values = np.array(positions)
    print(f"\n{model.p.name} final-position analysis")
    print("Final positions:", positions)
    print("Unique cells:", len(counts), "of", model.p.grid_size[0] * model.p.grid_size[1])
    print("Most occupied cells:", counts.most_common(5))
    print("Mean position: (%.2f, %.2f)" % tuple(values.mean(axis=0)))
    print("Position standard deviation: (%.2f, %.2f)" % tuple(values.std(axis=0)))
    return counts


def display_comparison(results):
    fig, axes = plt.subplots(2, len(results), figsize=(14, 8), squeeze=False)
    for column, (name, model) in enumerate(results):
        ax_path = axes[0, column]
        ax_final = axes[1, column]
        for index, agent in enumerate(model.agents):
            path = np.array(agent.path)
            ax_path.plot(path[:, 0], path[:, 1], marker=".", linewidth=1,
                         label=f"Agent {index + 1}")
            ax_final.scatter(agent.position[0], agent.position[1], s=80)

        ax_path.set_title(f"{name}: paths")
        ax_final.set_title(f"{name}: final positions")
        for ax in (ax_path, ax_final):
            ax.set_xlim(-0.5, model.p.grid_size[0] - 0.5)
            ax.set_ylim(-0.5, model.p.grid_size[1] - 0.5)
            ax.set_xticks(range(model.p.grid_size[0]))
            ax.set_yticks(range(model.p.grid_size[1]))
            ax.grid(True, alpha=0.3)
        ax_path.legend(fontsize="small")
    plt.tight_layout()
    plt.show()


num_agents = int(input("Enter number of agents: "))
grid_size = int(input("Enter grid size (e.g., 10 for 10x10): "))
num_steps = int(input("Enter number of steps: "))

common = {
    "agents": num_agents,
    "grid_size": (grid_size, grid_size),
    "steps": num_steps,
}

scenario_random = dict(common, name="Random movement", avoid_agents=False,
                       preferred_direction=None)
scenario_preferred = dict(common, name="Avoidance + preferred direction",
                          avoid_agents=True, preferred_direction=(1, 0))

results = [run_scenario("Random movement", scenario_random),
           run_scenario("Avoidance + preferred direction", scenario_preferred)]
for _, model in results:
    analyze_final_positions(model)
display_comparison(results)
