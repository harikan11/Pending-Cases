import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import seaborn as sns
import os
import warnings


selected = option_menu(
    menu_title=None,
    options=["Page-1", "Page-2", "Page-3"],
    default_index=0,
    menu_icon="cast",
    orientation="horizontal",
)

# st.set_page_config(
#    page_title="Pending Cases In Indian Judicial Court",
#    page_icon=":bar_chart",
#    layout="wide",
# )
df = pd.read_csv("NDAP_REPORT_7150 - NDAP_REPORT_7150.csv", encoding="ISO-8859-1")

# Define the navigation links in the sidebar
page = st.sidebar.selectbox("Select a Page", ["Page-1", "Page-2", "Page-3"])

if selected == "Page-1":
    states = [
        "Andhra Pradesh",
        "Arunachal Pradesh",
        "Assam",
        "Bihar",
        "Chhattisgarh",
        "Goa",
        "Gujarat",
        "Haryana",
        "Himachal Pradesh",
        "Jharkhand",
        "Karnataka",
        "Kerala",
        "Madhya Pradesh",
        "Maharashtra",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Odisha",
        "Punjab",
        "Rajasthan",
        "Sikkim",
        "Tamil Nadu",
        "Telangana",
        "Tripura",
        "Uttar Pradesh",
        "Uttarakhand",
        "West Bengal",
    ]
    selected_state = st.selectbox("Select a State", states)

    year = 2021
    state = selected_state

    columns_to_plot = [
        "District",
        "Cases pending at pleadings or issues or charge stage",
        "Cases pending at appearance or service-related stage",
        "Cases pending at compliance or steps or stay stage",
    ]

    filtered_df = df[(df["Year"] == year) & (df["State"] == state)][columns_to_plot]
    stacked_df = filtered_df.melt(
        id_vars=["District"], var_name="Stage", value_name="Number of Cases"
    )
    fig = px.bar(
        stacked_df,
        x="District",
        y="Number of Cases",
        color="Stage",
        title=f"Composition of Pending Cases by Stage in {state}",
        labels={
            "District": "District",
            "Stage": "Stage",
            "Number of Cases": "Number of Cases",
        },
    )
    fig.update_layout(barmode="relative")
    st.plotly_chart(fig, use_container_width=True, width=1000, height=600)
