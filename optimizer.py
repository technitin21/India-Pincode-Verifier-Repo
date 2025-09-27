from utils import geocode_pincode
from ortools.graph.pywrapgraph import SimpleMinCostFlow

def optimize_assignment(customers, employees, dist_fn):
    start_nodes, end_nodes, capacities, unit_costs = [], [], [], []
    supplies = []

    for i, c in enumerate(customers):
        supplies.append(1)

    for e in employees:
        supplies.append(-len(customers)//len(employees))

    index = 0
    for ci, c in enumerate(customers):
        c_loc = geocode_pincode(c["pincode"])
        for ei, e in enumerate(employees):
            e_loc = geocode_pincode(e["pincode"])
            if c_loc and e_loc:
                start_nodes.append(ci)
                end_nodes.append(len(customers)+ei)
                capacities.append(1)
                unit_costs.append(int(dist_fn(c_loc, e_loc)))

    smcf = pywrapgraph.SimpleMinCostFlow()
    for i in range(len(start_nodes)):
        smcf.AddArcWithCapacityAndUnitCost(start_nodes[i], end_nodes[i], capacities[i], unit_costs[i])
    for i in range(len(supplies)):
        smcf.SetNodeSupply(i, supplies[i])

    if smcf.Solve() == smcf.OPTIMAL:
        results = []
        for i in range(smcf.NumArcs()):
            if smcf.Flow(i) > 0:
                c_id = start_nodes[i]
                e_id = end_nodes[i] - len(customers)
                results.append({"customer": customers[c_id]["name"], "employee": employees[e_id]["name"]})
        return results
    else:
        return []
