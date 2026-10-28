import pulp

workers = ["A", "B", "C", "D"]
tasks = ["T1", "T2", "T3", "T4"]

time = [
    [9, 2, 7, 8],
    [6, 4, 3, 7],
    [5, 8, 1, 8],
    [7, 6, 9, 4]
]

model = pulp.LpProblem("Assignment", pulp.LpMinimize)

x = {}

for i in range(4):
    for j in range(4):
        x[i, j] = pulp.LpVariable(
            "assign_" + workers[i] + "_" + tasks[j],
            cat="Binary"
        )

# minimize total working time
model += pulp.lpSum(
    time[i][j] * x[i, j]
    for i in range(4)
    for j in range(4)
)

# every worker gets exactly one task
for i in range(4):
    model += pulp.lpSum(x[i, j] for j in range(4)) == 1

# every task is assigned to one worker
for j in range(4):
    model += pulp.lpSum(x[i, j] for i in range(4)) == 1

model.solve(pulp.PULP_CBC_CMD(msg=False))

print("Status:", pulp.LpStatus[model.status])

for i in range(4):
    for j in range(4):
        if x[i, j].value() > 0.5:
            print(workers[i], "->", tasks[j])

print("Total time:", pulp.value(model.objective))