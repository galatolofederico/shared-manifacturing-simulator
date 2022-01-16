import argparse
import pandas as pd
import yaml

def atleast_1(x):
    if x < 1: return 1
    return x

parser = argparse.ArgumentParser()

parser.add_argument("--dataset", type=str, default="./dataset/italy.xlsx")
parser.add_argument("--output", type=str, default="scenarios/italy.yaml")
parser.add_argument("--quantity-std", type=float, default=0)

args = parser.parse_args()

dataset = pd.read_excel(args.dataset)

zone_nodes_count = dict()
zone_machines_count = dict()
node_machines_count = dict()
zones = []
nodes = []
demands = []
for idx, elem in dataset.iterrows():
    region = elem["Region"]
    if region not in zone_nodes_count: zone_nodes_count[region] = 0
    zone_nodes_count[region] += 1
    node_name = f"{region}-{zone_nodes_count[region]}"
    zone_name = f"{region}Zone"
    if zone_name not in zone_machines_count: zone_machines_count[zone_name] = 0

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
    zone_machines_count[zone_name] += elem["Quantity"]
    node_machines_count[node_name] = elem["Quantity"]
    
global_zone = dict(
    name="GlobalZone",
    nodes=[],
    customers=[]
)
for zone in zones:
    global_zone["nodes"].extend(zone["nodes"])
    global_zone["customers"].extend(zone["customers"])
    
    demand = dict(
        type="ZoneDemand",
        name=f"{zone['name']}Demand",
        zone=zone["name"],
        quantity=dict(
            type="normal",
            cast="positive_integer",
            mu=atleast_1(zone_machines_count[zone["name"]]),
            std=args.quantity_std
        ),
        probability=dict(
            type="formula",
            value="1/100"
        ),
        duration=dict(
            type="normal",
            cast="positive_integer",
            mu=60,
            std=5,
        ),
        max_delivery_delta=dict(
            type="formula",
            cast="positive_integer",
            value="24*5+{duration}"
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
                        value=12
                    )
                ),
                dict(
                    zone="GlobalZone",
                    cost=dict(
                        type="constant",
                        value=36
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
