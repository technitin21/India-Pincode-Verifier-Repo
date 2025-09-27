import streamlit as st
from db import init_db, get_employees, get_customers, assign_customers
from utils import geocode_pincode, haversine_distance
from optimizer import optimize_assignment

st.set_page_config(page_title="India Pincode Verifier")

# Initialize DB
init_db()

st.sidebar.title("Navigation")
role = st.sidebar.radio("Choose portal", ["Admin", "Employee"])

if role == "Admin":
    st.title("Admin Portal")
    mode = st.radio("Assignment Mode", ["Nearest Greedy", "Optimized (OR-Tools)"])
    employees = get_employees()
    customers = get_customers()

    if st.button("Assign Tasks"):
        if mode == "Optimized (OR-Tools)"):
            assignments = optimize_assignment(customers, employees, haversine_distance)
        else:
            assignments = assign_customers(customers, employees)
        st.write(assignments)

elif role == "Employee":
    st.title("Employee Portal")
    st.info("Employees can view their assigned tasks and submit verification reports here.")
