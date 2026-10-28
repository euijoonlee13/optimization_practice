import pulp

# 1. Create an optimization model
model = pulp.LpProblem("Project_Selection", pulp.LpMaximize)

# 2. Define decision variables
x_A = pulp.LpVariable("Project_A", lowBound=0, upBound=1, cat="Continuous")
x_B = pulp.LpVariable("Project_B", lowBound=0, upBound=1, cat="Continuous")
x_C = pulp.LpVariable("Project_C", lowBound=0, upBound=1, cat="Continuous")

# 3. Define objective Function 
model += 500 * x_A + 400 * x_B + 600 * x_C

# 4. Define constraint
model += 4 * x_A + 3 * x_B + 5 * x_C <= 8

# 5. Solve the optimization problem
model.solve()

# 6. Print results
print("Status:", pulp.LpStatus[model.status])
print("Project A:", x_A.value())
print("Project B:", x_B.value())
print("Project C:", x_C.value())
print("Maximum Profit:", pulp.value(model.objective))