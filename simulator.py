import argparse
import yaml
import os

from src.controller import Controller
from src.hooks.statistics import Statistics
from src.node import Node
from src.zones import Zones
import src.demands as demands
import src.strategies as strategies
from src.utils import seed_everything

parser = argparse.ArgumentParser()

parser.add_argument("--scenario", type=str, default="./scenarios/test.yaml")
parser.add_argument("--results", type=str, default="./results")
parser.add_argument("--force-results-folder", action="store_true")
parser.add_argument("--strategy", type=str, default="NoSharing")
parser.add_argument("--seed", type=int, default=-1)
parser.add_argument("--ticks", type=int, default=24*7*2)
parser.add_argument("--save-plots", action="store_true")

args = parser.parse_args()

if args.seed < 0:
    random_data = os.urandom(4)
    args.seed = int.from_bytes(random_data, byteorder="big")

seed_everything(args.seed)

with open(args.scenario) as sf:
    scenario = yaml.safe_load(sf)

controller = Controller()

strategy = getattr(strategies, args.strategy)()
controller.set_strategy(strategy)

for node_args in scenario["nodes"]:
    controller.add_node(Node(node_args, controller))

for demand_args in scenario["demands"]:
    demand_type = getattr(demands, demand_args.pop("type"))
    controller.add_demand(demand_type(demand_args, controller))

zones = Zones(scenario["zones"], controller)
controller.set_zones(zones)

statistics = Statistics(controller)
controller.add_hook(statistics)

scenario_file = args.scenario.split("/")[-1]
if args.force_results_folder:
    results_folder = args.results
else:
    results_folder = os.path.join(args.results, scenario_file, args.strategy)

print("=== RUN INFO ===")
print(f"scenario={args.scenario}")
print(f"strategy={args.strategy}")
print(f"results_base_folder={args.results}")
print(f"results_folder={results_folder}")
print(f"ticks={args.ticks}")
print(f"seed={args.seed}")
print("================")

controller.run(args.ticks)

os.makedirs(results_folder, exist_ok=True)
statistics.save(results_folder, save_plots=args.save_plots)
controller.save_logs(os.path.join(results_folder, "logs.txt"))