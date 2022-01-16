import argparse
import pandas as pd
import yaml

def atleast_1(x):
    if x < 1: return 1
    return x

parser = argparse.ArgumentParser()

parser.add_argument("--dataset", type=str, default="./dataset/italy.xlsx")
parser.add_argument("--output", type=str, default="scenarios/italy.yaml")
parser.add_argument("--quantity-mu-formula", type=str, default="{zone_machines_count}")
parser.add_argument("--quantity-std-formula", type=str, default="{zone_machines_count}")
parser.add_argument("--probability", type=float, default=0.01)
parser.add_argument("--duration-mu", type=float, default=60)
parser.add_argument("--duration-std", type=float, default=5)
parser.add_argument("--max-delivery-delta-formula", type=str, default="24*5+{duration}")

parser.add_argument("--same-zone-logistic-cost", type=float, default=12)
parser.add_argument("--global-zone-logistic-cost", type=float, default=36)


args = parser.parse_args()

dataset = pd.read_excel(args.dataset)

zones_nodes_count = dict()
zones_machines_count = dict()
node_machines_count = dict()
zones = []
nodes = []
demands = []
for idx, elem in dataset.iterrows():
    region = elem["Region"]
    if region not in zones_nodes_count: zones_nodes_count[region] = 0
    zones_nodes_count[region] += 1
    node_name = f"{region}-{zones_nodes_count[region]}"
    zone_name = f"{region}Zone"
    if zone_name not in zones_machines_count: zones_machines_count[zone_name] = 0

    zone = None
    for z in zones:
        if z["name"] == zone_name:
            zone = z
    if zone is None:
        zone = dict(
            name=zone_name,
            nodes=[],
            customers=[f"{zone_name}Customer"]
        )
        zones.append(zone)
    
    zone["nodes"].append(node_name)
    zones_machines_count[zone_name] += elem["Quantity"]
    node_machines_count[node_name] = elem["Quantity"]
    
global_zone = dict(
    name="GlobalZone",
    nodes=[],
    customers=[]
)
for zone in zones:
    global_zone["nodes"].extend(zone["nodes"])
    global_zone["customers"].extend(zone["customers"])
    
    zone_machines_count = zones_machines_count[zone["name"]]

    demand = dict(
        type="ZoneDemand",
        name=f"{zone['name']}Demand",
        zone=zone["name"],
        quantity=dict(
            type="normal",
            cast="positive_integer",
            mu=atleast_1(eval(args.quantity_mu_formula.format(zone_machines_count=zone_machines_count))),
            std=atleast_1(eval(args.quantity_std_formula.format(zone_machines_count=zone_machines_count)))
        ),
        probability=dict(
            type="constant",
            value=args.probability
        ),
        duration=dict(
            type="normal",
            cast="positive_integer",
            mu=args.duration_mu,
            std=args.duration_std,
        ),
        max_delivery_delta=dict(
            type="formula",
            cast="positive_integer",
            value=args.max_delivery_delta_formula
        )
    )
    demands.append(demand)

    for node_name in zone["nodes"]:
        quantity = node_machines_count[node_name]
        
        node = dict(
            name=node_name,
            capacity=dict(
                type="constant",
                value=quantity
            ),
            zones=["GlobalZone", zone["name"]],
            neighbours="*",
            logistics=[
                dict(
                    zone=zone["name"],
                    cost=dict(
                        type="constant",
                        value=args.same_zone_logistic_cost
                    )
                ),
                dict(
                    zone="GlobalZone",
                    cost=dict(
                        type="constant",
                        value=args.global_zone_logistic_cost
                    )
                )
            ]
        )

        nodes.append(node)

zones.append(global_zone)

with open(args.output, "w") as f:
    yaml.dump(dict(
        nodes=nodes,
        zones=zones,
        demands=demands
    ), f)

print(f"File {args.output} saved!")
