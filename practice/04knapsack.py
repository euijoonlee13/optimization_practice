import pulp

items = ["A", "B", "C", "D", "E"]

weights = [4, 3, 5, 2, 6]
values = [10, 8, 12, 6, 14]

capacity = 12

model = pulp.LpProblem("Knapsack", pulp.LpMaximize)

x = {}

for i in range(len(items)):
    x[i] = pulp.LpVariable("item_" + items[i], cat="Binary")

# total value
model += pulp.lpSum(values[i] * x[i] for i in range(len(items)))

# weight constraint
model += pulp.lpSum(weights[i] * x[i] for i in range(len(items))) <= capacity

model.solve(pulp.PULP_CBC_CMD(msg=False))

print("Status:", pulp.LpStatus[model.status])

for i in range(len(items)):
    print(items[i], x[i].value())

print("Maximum value:", pulp.value(model.objective))

# TODO: what happens if capacity = 15?