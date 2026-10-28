import pulp

projects = ["A", "B", "C", "D", "E"]

budget = {
    "A": 30, "B": 40, "C": 25, "D": 50, "E": 20
}

people = {
    "A": 3, "B": 4, "C": 2, "D": 5, "E": 2
}

value = {
    "A": 60, "B": 80, "C": 45, "D": 95, "E": 35
}

max_budget = 100
max_people = 10

model = pulp.LpProblem("Budget_Allocation", pulp.LpMaximize)

x = {}

for p in projects:
    x[p] = pulp.LpVariable("project_" + p, cat="Binary")

# maximize total value
model += pulp.lpSum(value[p] * x[p] for p in projects)

# budget constraint
model += pulp.lpSum(budget[p] * x[p] for p in projects) <= max_budget

# people constraint
model += pulp.lpSum(people[p] * x[p] for p in projects) <= max_people

# project D requires project A
model += x["D"] <= x["A"]

model.solve(pulp.PULP_CBC_CMD(msg=False))

print("Status:", pulp.LpStatus[model.status])

for p in projects:
    if x[p].value() > 0.5:
        print("Selected:", p)

print("Maximum value:", pulp.value(model.objective))

# TODO: try changing max_budget to 120