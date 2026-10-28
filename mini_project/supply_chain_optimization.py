import pulp

# Small supply chain optimization project
# Goal: minimize production and transportation costs

factories = ["F1", "F2"]
products = ["P1", "P2"]
customers = ["C1", "C2"]

# Demand for each product at each customer
demand = {
    ("C1", "P1"): 30,
    ("C1", "P2"): 20,
    ("C2", "P1"): 25,
    ("C2", "P2"): 35
}

# Production cost per unit
production_cost = {
    ("F1", "P1"): 4,
    ("F1", "P2"): 6,
    ("F2", "P1"): 5,
    ("F2", "P2"): 4
}

# Transportation cost per unit
transport_cost = {
    ("F1", "C1"): 2,
    ("F1", "C2"): 5,
    ("F2", "C1"): 4,
    ("F2", "C2"): 2
}

fixed_cost = {
    "F1": 100,
    "F2": 120
}

# Resource usage per product
resource_use = {
    "P1": 1,
    "P2": 2
}


def solve_problem(resource_budget):

    model = pulp.LpProblem("Supply_Chain", pulp.LpMinimize)

    open_factory = {}
    production = {}
    shipping = {}

    # Variables
    for f in factories:
        open_factory[f] = pulp.LpVariable(
            "open_" + f, cat="Binary"
        )

        for p in products:
            production[f, p] = pulp.LpVariable(
                "produce_" + f + "_" + p,
                lowBound=0
            )

            for c in customers:
                shipping[f, c, p] = pulp.LpVariable(
                    "ship_" + f + "_" + c + "_" + p,
                    lowBound=0
                )

    # Objective function
    model += (
        pulp.lpSum(
            fixed_cost[f] * open_factory[f]
            for f in factories
        )
        + pulp.lpSum(
            production_cost[f, p] * production[f, p]
            for f in factories for p in products
        )
        + pulp.lpSum(
            transport_cost[f, c] * shipping[f, c, p]
            for f in factories for c in customers for p in products
        )
    )

    # Demand constraints
    for c in customers:
        for p in products:
            model += (
                pulp.lpSum(shipping[f, c, p] for f in factories)
                == demand[c, p]
            )

    # Production = total shipping
    for f in factories:
        for p in products:
            model += (
                production[f, p]
                == pulp.lpSum(shipping[f, c, p] for c in customers)
            )

    # Resource capacity for each factory
    for f in factories:
        model += (
            pulp.lpSum(
                resource_use[p] * production[f, p]
                for p in products
            )
            <= resource_budget * open_factory[f]
        )

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    status = pulp.LpStatus[model.status]

    print("\nResource budget:", resource_budget)
    print("Status:", status)

    if status != "Optimal":
        print("No optimal solution found")
        return

    print("Total cost:", pulp.value(model.objective))

    for f in factories:
        print(f, "open:", open_factory[f].value())

    print("\nProduction:")
    for f in factories:
        for p in products:
            print(f, p, production[f, p].value())

    print("\nShipping:")
    for f in factories:
        for c in customers:
            for p in products:
                amount = shipping[f, c, p].value()
                if amount > 0.001:
                    print(f, "->", c, p, amount)


# Compare different resource budgets
solve_problem(140)
solve_problem(180)
solve_problem(220)

# TODO:
# 1. Add another factory
# 2. Change transportation costs
# 3. Compare total cost for different budgets