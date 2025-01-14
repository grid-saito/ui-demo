#!/bin/bash

# Install the graph module in editable mode
pip install -e app/graph

# Run the Streamlit application
streamlit run app/main.py