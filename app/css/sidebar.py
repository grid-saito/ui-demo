import streamlit as st

def past_searches_style():
    st.markdown("""
        <style>
        .stButton > button {
            border: none; /* Remove border lines */
            background-color: #f0f2f6; /* Light grey background */
            color: #000000; /* Black text */
            padding: 0.1px 0.1px; /* Padding */
            font-size: 3px; /* Font size */
            cursor: pointer; /* Pointer cursor on hover */
            text-align: left; /* Left-align text */
            margin-bottom: 0.1px;
        }
        .stButton > button:hover {
            background-color: #D4D4D4; /* Green background on hover */
            color: black; /* White text on hover */
        }
        </style>
        """, unsafe_allow_html=True)