#!/bin/bash

# Ξεκινάει το Flask API στο παρασκήνιο (&)
python api.py &

# Ξεκινάει το Streamlit στο προσκήνιο
streamlit run ui.py --server.port=8501 --server.address=0.0.0.0