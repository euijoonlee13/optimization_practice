import pulp

factories = ["F1", "F2"]
stores = ["S1", "S2", "S3"]

supply = {"F1": 80, "F2": 70}
demand = {"S1": 40, "S2": 50, "S3": 60}

cost = {
    ("F1", "S1"): 4,
    ("F1", "S2"): 6,
    ("F1", "S3"): 8,
    ("F2", "S1"): 5,
    ("F2", "S2"): 4,
    ("F2", "S3"): 3
}

model = pulp.LpProblem("Transportation", pulp.LpMinimize)

x = {}

for f in factories:
    for s in stores:
        x[f, s] = pulp.LpVariable(
            "ship_" + f + "_" + s,
            lowBound=0
        )

# total transportation cost
model += pulp.lpSum(
    cost[f, s] * x[f, s]
    for f in factories
    for s in stores
)

# factory capacity
for f in factories:
    model += pulp.lpSum(x[f, s] for s in stores) <= supply[f]

# store demand
for s in stores:
    model += pulp.lpSum(x[f, s] for f in factories) >= demand[s]

model.solve(pulp.PULP_CBC_CMD(msg=False))

print("Status:", pulp.LpStatus[model.status])

for f in factories:
    for s in stores:
        print(f, "->", s, ":", x[f, s].value())

print("Total transportation cost:", pulp.value(model.objective))