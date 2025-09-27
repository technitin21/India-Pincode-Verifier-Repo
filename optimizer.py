# optimizer.py
# Use OR-Tools to solve an assignment problem: assign customers to employees minimizing total distance
# subject to employee capacities. We model this as a min-cost flow / assignment with capacities.


from ortools.graph import pywrapgraph
from math import isfinite


# customers: list of dicts {'id':..., 'lat':..., 'lon':...}
# employees: list of dicts {'employee_id':..., 'lat':..., 'lon':..., 'capacity': int}
# dist_fn: function(a_lat,a_lon,b_lat,b_lon)->distance (float)


def optimize_assignment(customers, employees, dist_fn):
"""Returns list of (customer_id, employee_id) assignments minimizing total distance.
If an employee has capacity 0 -> treated as unlimited (or you can set a large number).
Unassignable customers (no finite distance) will not be assigned and omitted from result.
"""
# Build node indices
# We'll create: source -> customer nodes -> employee nodes -> sink
# Each customer has demand 1. Each employee has capacity = capacity.


# Indexing
customer_nodes = {c['id']: i for i, c in enumerate(customers)}
num_customers = len(customers)
employee_nodes = {e['employee_id']: i for i, e in enumerate(employees)}
num_employees = len(employees)


# Create min cost flow
start_nodes = []
end_nodes = []
capacities = []
unit_costs = []


# special node indices
source = 0
cust_start = 1
emp_start = cust_start + num_customers
sink = emp_start + num_employees


# Source -> each customer (supply 1)
for i in range(num_customers):
start_nodes.append(source)
end_nodes.append(cust_start + i)
capacities.append(1)
unit_costs.append(0)


# Each employee -> sink with capacity = employee.capacity
for j, e in enumerate(employees):
cap = e.get('capacity', 0)
if cap == 0:
cap = num_customers # treat 0 as unlimited up to num_customers
start_nodes.append(emp_start + j)
end_nodes.append(sink)
capacities.append(cap)
unit_costs.append(0)


# Customer -> employee edges with cost = round(distance * 1000) (convert to int)
for i, c in enumerate(customers):
a_lat = c.get('lat'); a_lon = c.get('lon')
for j, e in enumerate(employees):
b_lat = e.get('lat'); b_lon = e.get('lon')
d = dist_fn(a_lat, a_lon, b_lat, b_lon)
if not isfinite(d):
continue
# add edge cust -> emp
