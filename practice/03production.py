import pulp

# Production planning with two products
# A: profit 30, B: profit 50

model = pulp.LpProblem("Production_Planning", pulp.LpMaximize)

a = pulp.LpVariable("Product_A", lowBound=0)
b = pulp.LpVariable("Product_B", lowBound=0)

# objective function
model += 30*a + 50*b

# machine time
model += 2*a + 4*b <= 100

# material
model += 3*a + 2*b <= 90

model.solve(pulp.PULP_CBC_CMD(msg=False))

print("Status:", pulp.LpStatus[model.status])
print("Product A:", a.value())
print("Product B:", b.value())
print("Profit:", pulp.value(model.objective))

# TODO: try changing the machine time from 100 to 120 