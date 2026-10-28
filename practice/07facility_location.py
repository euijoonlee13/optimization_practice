import pulp

warehouses = ["W1", "W2", "W3"]
customers = ["C1", "C2", "C3"]

fixed_cost = {"W1": 100, "W2": 120, "W3": 90}
capacity = {"W1": 80, "W2": 100, "W3": 60}
demand = {"C1": 40, "C2": 50, "C3": 30}

shipping_cost = {
    ("W1", "C1"): 3, ("W1", "C2"): 6, ("W1", "C3"): 5,
    ("W2", "C1"): 5, ("W2", "C2"): 2, ("W2", "C3"): 4,
    ("W3", "C1"): 6, ("W3", "C2"): 4, ("W3", "C3"): 3
}

model = pulp.LpProblem("Facility_Location", pulp.LpMinimize)

open_w = {}
ship = {}

for w in warehouses:
    open_w[w] = pulp.LpVariable("open_" + w, cat="Binary")

    for c in customers:
        ship[w, c] = pulp.LpVariable(
            "ship_" + w + "_" + c, lowBound=0
        )

# fixed cost + shipping cost
model += (
    pulp.lpSum(fixed_cost[w] * open_w[w] for w in warehouses)
    + pulp.lpSum(
        shipping_cost[w, c] * ship[w, c]
        for w in warehouses for c in customers
    )
)

# satisfy customer demand
for c in customers:
    model += pulp.lpSum(ship[w, c] for w in warehouses) == demand[c]

# cannot ship from a closed warehouse
for w in warehouses:
    model += (
        pulp.lpSum(ship[w, c] for c in customers)
        <= capacity[w] * open_w[w]
    )

model.solve(pulp.PULP_CBC_CMD(msg=False))

print("Status:", pulp.LpStatus[model.status])

for w in warehouses:
    print(w, "open:", open_w[w].value())

for w in warehouses:
    for c in customers:
        if ship[w, c].value() > 0.001:
            print(w, "->", c, ":", ship[w, c].value())

print("Total cost:", pulp.value(model.objective))

# TODO: try increasing the fixed cost of W2