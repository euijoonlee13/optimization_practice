import pulp

nodes = ["A", "B", "C", "D", "E", "F"]

edges = {
    ("A", "B"): 4,
    ("A", "C"): 2,
    ("B", "D"): 5,
    ("B", "E"): 3,
    ("C", "B"): 1,
    ("C", "D"): 8,
    ("C", "E"): 10,
    ("D", "F"): 3,
    ("E", "F"): 4
}

start = "A"
end = "F"

model = pulp.LpProblem("Shortest_Path", pulp.LpMinimize)

x = {}

for edge in edges:
    x[edge] = pulp.LpVariable(
        "edge_" + edge[0] + "_" + edge[1],
        cat="Binary"
    )

# minimize distance
model += pulp.lpSum(edges[e] * x[e] for e in edges)

# flow conservation
for n in nodes:
    outgoing = pulp.lpSum(x[e] for e in edges if e[0] == n)
    incoming = pulp.lpSum(x[e] for e in edges if e[1] == n)

    if n == start:
        model += outgoing - incoming == 1
    elif n == end:
        model += outgoing - incoming == -1
    else:
        model += outgoing - incoming == 0

model.solve(pulp.PULP_CBC_CMD(msg=False))

print("Status:", pulp.LpStatus[model.status])

for e in edges:
    if x[e].value() > 0.5:
        print(e[0], "->", e[1])

print("Shortest distance:", pulp.value(model.objective))

# TODO: compare this result with Dijkstra's algorithm