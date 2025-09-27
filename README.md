# India Pincode Verifier App

Streamlit web application for India-specific address verification assignments.

Features:
- Admin portal: upload Excel of customers, assign tasks (greedy or optimized using OR-Tools).
- Employee portal: employees complete verifications with forms + photo upload.
- SQLite backend.
- OR-Tools optimizer for minimum total travel distance assignment.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
