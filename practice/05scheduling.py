import pulp

employees = ["Anna", "Ben", "Chris", "Dina"]
shifts = ["Morning", "Afternoon", "Evening"]

cost = {
    "Anna": 70,
    "Ben": 65,
    "Chris": 80,
    "Dina": 60
}

model = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

x = {}

for e in employees:
    for s in shifts:
        x[e, s] = pulp.LpVariable(
            "assign_" + e + "_" + s,
            cat="Binary"
        )

# minimize employee cost
model += pulp.lpSum(
    cost[e] * x[e, s]
    for e in employees
    for s in shifts
)

# every shift needs one employee
for s in shifts:
    model += pulp.lpSum(x[e, s] for e in employees) >= 1

# each employee can work at most one shift
for e in employees:
    model += pulp.lpSum(x[e, s] for s in shifts) <= 1

model.solve(pulp.PULP_CBC_CMD(msg=False))

print("Status:", pulp.LpStatus[model.status])

for e in employees:
    for s in shifts:
        if x[e, s].value() > 0.5:
            print(e, "works", s)

print("Total cost:", pulp.value(model.objective))

# TODO: add availability constraints