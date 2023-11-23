import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import geopandas as gpd
import json

import pyproj

import pydeck as pdk
from streamlit_option_menu import option_menu
import seaborn as sns
import os
import warnings

# warnings.filterwearnings("ignore")


########################
st.set_page_config(
    page_title="Pending Cases In Indian Judicial Court",
    page_icon=":bar_chart",
    layout="wide",
)


#######################
# st.set_page_config(
#   page_title="Pending Cases In Indian Judicial Court",
#  page_icon=":bar_chart",
# layout="wide",
# )

st.title(":bar_chart:Pending Cases In Indian Judicial Court")
st.markdown(
    "<style>div.block-container{padding-top:1rem;text-align:center;}</style>",
    unsafe_allow_html=True,
)


# fl = st.file_uploader(":file_folder: Upload the file", type=(["csv", "xlsx", "xls"]))

# if fl is not None:
#    filename = fl.name
#    st.write(filename)
#    df = pd.read_csv(filename, encoding="ISO-8859-1")
# else:
#    os.chdir(r"C:/Users/Harika Naishadham/OneDrive/Documents/Pending Cases")
df = pd.read_csv("NDAP_REPORT_7150 - NDAP_REPORT_7150.csv", encoding="ISO-8859-1")

##########

civil_cases = df[df["District and taluk court case type"] == "Civil"][
    "Pending cases"
].sum()
criminal_cases = df[df["District and taluk court case type"] == "Criminal"][
    "Pending cases"
].sum()

col1, col2, col3 = st.columns(3)

block_style = """
    background-color: darkblue;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-size: 24px;
    text-align: center;
"""
with col1:
    st.markdown(
        f'<div style="{block_style}">Total Pending Criminal Cases in India<br>{criminal_cases}</div>',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f'<div style="{block_style}">Total Pending Civil Cases in India<br>{civil_cases}</div>',
        unsafe_allow_html=True,
    )
with col3:
    total_cases = civil_cases + criminal_cases
    st.markdown(
        f'<div style="{block_style}">Total Pending Cases in India<br>{total_cases}</div>',
        unsafe_allow_html=True,
    )


#############
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
fig.update_layout(legend=dict(title="", title_font=dict(size=20), font=dict(size=16)))

st.markdown("<style>.css-1l6hoj8 em{font-size: 24px;}</style>", unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True, width=1000, height=600)


# pie charts
states = df["State"].unique()

selected_state = st.selectbox("Select a State", states, key="state_selector")
year = 2021
col1, col2 = st.columns(2)

# Plot 1: Stacked bar chart
with col1:
    filtered_data = df[df["State"] == selected_state]
    filtered_data = filtered_data[
        filtered_data["District and taluk court case type"].isin(["Civil", "Criminal"])
    ]
    case_type = (
        filtered_data.groupby("District and taluk court case type")["Pending cases"]
        .agg("sum")
        .reset_index()
    )
    fig1 = go.Figure(
        data=go.Pie(
            labels=case_type["District and taluk court case type"],
            values=case_type["Pending cases"],
        )
    )
    fig1.update_layout(
        title="Break-up of Civil and Criminal Cases in " + selected_state
    )
    st.plotly_chart(fig1, use_container_width=True, width=500, height=400)
    st.markdown(
        "<style>.css-1l6hoj8 em{font-size: 24px;}</style>", unsafe_allow_html=True
    )
    # st.plotly_chart(fig, use_container_width=True, width=500, height=400)

# Plot 2: First Pie Chart
with col2:
    columns_to_plot = [
        "District",
        "Cases pending at pleadings or issues or charge stage",
        "Cases pending at appearance or service-related stage",
        "Cases pending at compliance or steps or stay stage",
    ]
    filtered_data = df[df["State"] == selected_state]
    district_data = (
        filtered_data.groupby("District")["Pending cases"].sum().reset_index()
    )

    fig = px.pie(
        district_data,
        names="District",
        values="Pending cases",
        title=f"Total Pending Cases in Districts of {selected_state}",
    )
    st.plotly_chart(fig, use_container_width=True)
    fig.update_layout(barmode="relative")


# >5years bar chart

df["pending_over_5_yrs"] = (
    df["Pending cases for a period of 5 to 10 years"]
    + df["Pending cases for a period of 10 to 20 years"]
    + df["Pending cases for a period of 20 to 30 years"]
    + df["Pending cases over 30 years"]
)
df["pending_less_5_yrs"] = (
    df["Pending cases for a period of 0 to 1 years"]
    + df["Pending cases for a period of 1 to 3 years"]
    + df["Pending cases for a period of 3 to 5 years"]
)
states_pending_total = df.groupby("State")["Pending cases"].agg("sum").reset_index()
states_5yrs_total = df.groupby("State")["pending_over_5_yrs"].agg("sum").reset_index()
states_5yrs_comb = pd.merge(states_pending_total, states_5yrs_total, on="State")
states_5yrs_comb["perc_over_5yrs"] = (
    states_5yrs_comb["pending_over_5_yrs"] / states_5yrs_comb["Pending cases"]
) * 100
states_5yrs_comb1 = (
    states_5yrs_comb.groupby("State")["perc_over_5yrs"]
    .agg("mean")
    .sort_values(ascending=False)
    .reset_index()
)


fig2 = px.bar(
    states_5yrs_comb1,
    x="State",
    y="perc_over_5yrs",
    title="States with the Highest % of Cases Pending for >5 Years",
)


############################
states_less_5yrs_total = (
    df.groupby("State")["pending_less_5_yrs"].agg("sum").reset_index()
)
states_less_5yrs_comb = pd.merge(
    states_pending_total, states_less_5yrs_total, on="State"
)
states_less_5yrs_comb["perc_less_5yrs"] = (
    states_less_5yrs_comb["pending_less_5_yrs"] / states_less_5yrs_comb["Pending cases"]
) * 100
selected_duration = st.selectbox(
    "Select Duration", ["Greater than 5 years", "Less than 5 years"]
)

if selected_duration == "Greater than 5 years":
    selected_data = states_5yrs_comb
    title = "States with the Highest % of Cases Pending for >5 Years"
else:
    selected_data = states_less_5yrs_comb
    title = "States with the Highest % of Cases Pending for <5 Years"


fig = px.bar(
    selected_data,
    x="State",
    y="perc_over_5yrs"
    if selected_duration == "Greater than 5 years"
    else "perc_less_5yrs",
    title=title,
)

fig.update_layout(height=600, width=1200)
fig.update_layout(legend=dict(title="", title_font=dict(size=20), font=dict(size=16)))

st.markdown("<style>.css-1l6hoj8 em{font-size: 24px;}</style>", unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)

#################
# polar line plot

state_case_type = (
    df.groupby(["State", "District and taluk court case type"])["Pending cases"]
    .agg("sum")
    .reset_index()
)
state_wise_case_pivot = pd.pivot_table(
    data=state_case_type,
    values="Pending cases",
    index="State",
    columns="District and taluk court case type",
).reset_index()

state_wise_case_pivot["criminal_pcnt"] = (
    state_wise_case_pivot["Criminal"]
    / (state_wise_case_pivot["Civil"] + state_wise_case_pivot["Criminal"])
) * 100
state_wise_case_pivot["civil_pcnt"] = 100 - state_wise_case_pivot["criminal_pcnt"]

state_wise_case_pivot1 = (
    state_wise_case_pivot.groupby("State")["criminal_pcnt"]
    .agg("mean")
    .sort_values(ascending=False)
    .reset_index()
)
fig = px.line_polar(
    state_wise_case_pivot1,
    r="criminal_pcnt",
    theta="State",
    line_close=True,
    title="States with the Highest % of Criminal Cases",
)

fig.update_layout(
    width=800,
    height=600,
)

st.plotly_chart(fig, use_container_width=True)


##line chart

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=state_wise_case_pivot["State"],
        y=state_wise_case_pivot["civil_pcnt"],
        mode="lines+markers",
        name="Civil Cases Percentage",
        line=dict(color="yellow"),
    )
)

fig.update_layout(
    title="States with Highest % of Civil Cases",
    xaxis_title="State",
    yaxis_title="% of Civil Cases",
    height=600,
    width=1200,
)

fig.update_xaxes(tickangle=45, tickfont=dict(size=16))
st.plotly_chart(fig, use_container_width=True)


###########donut chart

datpie = go.Pie(
    values=states_pending_total["Pending cases"],
    labels=states_pending_total["State"],
    hole=0.3,
)
laypie = go.Layout(title="Breakup of pending cases", height=800, width=1200)
figpie = go.Figure(datpie, laypie)

st.plotly_chart(figpie, use_container_width=True)


##bar chart

pend_evidence = (
    df.groupby("District and taluk court case type")[
        "Cases pending at evidence or argument or judgement stage"
    ]
    .agg("sum")
    .reset_index()
)
pending_compliance = (
    df.groupby("District and taluk court case type")[
        "Cases pending at compliance or steps or stay stage"
    ]
    .agg("sum")
    .reset_index()
)
pending_appearance = (
    df.groupby("District and taluk court case type")[
        "Cases pending at appearance or service-related stage"
    ]
    .agg("sum")
    .reset_index()
)
pending_charge = (
    df.groupby("District and taluk court case type")[
        "Cases pending at pleadings or issues or charge stage"
    ]
    .agg("sum")
    .reset_index()
)


pend_1 = pd.merge(
    pend_evidence, pending_compliance, on="District and taluk court case type"
)
pend_2 = pd.merge(
    pending_appearance, pending_charge, on="District and taluk court case type"
)
pend_3 = pd.merge(pend_1, pend_2, on="District and taluk court case type")

pend_pivot = pend_3.transpose()
pend_pivot = pend_pivot.rename(columns={0: "Civil", 1: "Criminal"})
pend_pivot = pend_pivot.drop("District and taluk court case type")


fig = px.bar(
    pend_pivot,
    x=pend_pivot.index,
    y="Civil",
    title="Pendency reasons for Civil cases",
)

fig.update_layout(width=800, height=600)
fig.update_xaxes(tickfont=dict(size=14))
fig.update_yaxes(title_font=dict(size=16))
fig.update_layout(
    title_text="Pendency reasons for Civil cases", title_font=dict(size=18)
)

####################
case_type = st.radio("Select Case Type", ("Civil", "Criminal"))

if case_type == "Civil":
    y_column = "Civil"
else:
    y_column = "Criminal"
fig = px.bar(
    pend_pivot,
    x=pend_pivot.index,
    y=y_column,
    title=f"Pendency reasons for {case_type} cases",
)

fig.update_layout(width=800, height=600)
fig.update_xaxes(tickfont=dict(size=14))
fig.update_yaxes(title_font=dict(size=16))
fig.update_layout(
    title_text=f"Pendency reasons for {case_type} cases",
    title_font=dict(size=18),
)

st.plotly_chart(fig, use_container_width=True)

##area chart

fig1 = px.area(
    pend_pivot,
    x=pend_pivot.index,
    y="Criminal",
    title="Pendency reasons for criminal cases",
)

selected_range = st.slider(
    "Select a range", 0, len(pend_pivot) - 1, (0, len(pend_pivot) - 1)
)
fig1.update_traces(fill="tozeroy")

fig1.update_xaxes(range=[selected_range[0], selected_range[1]])
fig1.update_layout(width=900, height=700)
fig1.update_xaxes(tickfont=dict(size=14))
fig1.update_yaxes(title_font=dict(size=16))
fig1.update_layout(
    title_text="Pendency reasons for criminal cases", title_font=dict(size=18)
)

fig1.update_layout(width=800, height=600)

st.plotly_chart(fig1, use_container_width=True)


##heatmap

selected_case_type = st.selectbox("Select Case Type", ["Criminal", "Civil"])

criminal_df = df[df["District and taluk court case type"] == selected_case_type]

pivot_df = criminal_df.pivot_table(index="State", values="Pending cases", aggfunc="sum")
plt.figure(figsize=(10, 8))
sns.heatmap(
    pivot_df,
    cmap="YlGnBu",
    annot=True,
    fmt="f",
    linewidths=0.5,
    cbar_kws={"label": f"Total Pending {selected_case_type} Cases"},
)
plt.title(f"Heatmap for Total Pending {selected_case_type} Cases")
st.set_option("deprecation.showPyplotGlobalUse", False)
st.pyplot()


##############
# line chart woman vs senior citizen
cases_women = df.groupby("State")["Cases filed by women"].agg("sum").reset_index()
state_replacements = {
    "Jammu And Kashmir": "Jammu and Kashmir",
    "The Dadra And Nagar Haveli And Daman And Diu": "Daman and Diu",
}
cases_women["State"].replace(state_replacements, inplace=True)
cases_women.at[29, "Cases filed by women"] = 207.0
cases_women.loc[len(cases_women.index)] = ["Dadra And Nagar Haveli", 177]
cases_senior = (
    df.groupby("State")["Cases filed by senior citizens"].agg("sum").reset_index()
)
cases_senior["State"].replace(state_replacements, inplace=True)
cases_senior.at[29, "Cases filed by senior citizens"] = 207.0
cases_senior.loc[len(cases_senior.index)] = ["Dadra And Nagar Haveli", 177]


fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=cases_women["State"],
        y=cases_women["Cases filed by women"],
        mode="lines+markers",
        name="Cases filed by Women",
        line=dict(color="yellow"),
    )
)
fig.add_trace(
    go.Scatter(
        x=cases_senior["State"],
        y=cases_senior["Cases filed by senior citizens"],
        mode="lines+markers",
        name="Cases filed by Senior Citizens",
        line=dict(color="red"),
    )
)
fig.update_layout(
    title="Comparison of Cases Filed by Women and Senior Citizens by State",
    xaxis_title="State",
    yaxis_title="Number of Cases",
    height=800,
    width=1500,
)
fig.update_xaxes(tickangle=45, tickfont=dict(size=16))
st.plotly_chart(fig, use_container_width=True)


###parallel plot
pend_year1 = (
    df.groupby("State")["Pending cases for a period of 0 to 1 years"]
    .agg("sum")
    .reset_index()
)
pend_year2 = (
    df.groupby("State")["Pending cases for a period of 1 to 3 years"]
    .agg("sum")
    .reset_index()
)
pend_year3 = (
    df.groupby("State")["Pending cases for a period of 3 to 5 years"]
    .agg("sum")
    .reset_index()
)
pend_year4 = (
    df.groupby("State")["Pending cases for a period of 5 to 10 years"]
    .agg("sum")
    .reset_index()
)
pend_year5 = (
    df.groupby("State")["Pending cases for a period of 10 to 20 years"]
    .agg("sum")
    .reset_index()
)
pend_year6 = (
    df.groupby("State")["Pending cases for a period of 20 to 30 years"]
    .agg("sum")
    .reset_index()
)

pending_1 = pd.merge(pend_year1, pend_year2, on="State")
pending_2 = pd.merge(pend_year3, pend_year4, on="State")
pending_3 = pd.merge(pend_year5, pend_year6, on="State")
pending_4 = pd.merge(pending_1, pending_2, on="State")
pending_5 = pd.merge(pending_4, pending_3, on="State")

available_states = pending_5["State"].unique()

st.title("Total Pending Cases by Period in Each State")

selected_states = st.multiselect(
    "Select States", available_states, default=available_states
)

filtered_data = pending_5[pending_5["State"].isin(available_states)]


labels = {
    "State": "State",
    "Pending cases for a period of 0 to 1 years": "0 to 1 years",
    "Pending cases for a period of 1 to 3 years": "1 to 3 years",
    "Pending cases for a period of 3 to 5 years": "3 to 5 years",
    "Pending cases for a period of 5 to 10 years": "5 to 10 years",
    "Pending cases for a period of 10 to 20 years": "10 to 20 years",
    "Pending cases for a period of 20 to 30 years": "20 to 30 years",
}


fig = px.parallel_coordinates(
    filtered_data,
    labels=labels,
)

fig.update_layout(
    autosize=False,
    width=1500,
    height=800,
    xaxis=dict(
        title=dict(font=dict(size=30)),
        tickfont=dict(size=25),
    ),
    yaxis=dict(
        title=dict(font=dict(size=30)),
        tickfont=dict(size=25),
    ),
)


st.plotly_chart(fig)


##cholorpleth

map_df = gpd.read_file(
    r"C:\Users\Harika Naishadham\OneDrive\Documents\Pending Cases\india-polygon.shp"
)

cases_women = df.groupby("State")["Cases filed by women"].agg("sum").reset_index()
cases_senior_citizens = (
    df.groupby("State")["Cases filed by senior citizens"].agg("sum").reset_index()
)

cases = cases_women.merge(cases_senior_citizens, on="State")

cases.rename(
    columns={
        "Cases filed by women": "Total Cases filed by Women",
        "Cases filed by senior citizens": "Total Cases filed by Senior Citizens",
    },
    inplace=True,
)


merged = map_df.set_index("st_nm").join(cases.set_index("State"))
merged["Total Cases filed by Women"] = merged["Total Cases filed by Women"].replace(
    np.nan, 0
)
merged["Total Cases filed by Senior Citizens"] = merged[
    "Total Cases filed by Senior Citizens"
].replace(np.nan, 0)


st.title("Choropleth Map of Pending Cases in India")
selected_variable = st.selectbox(
    "Select Variable",
    ["Total Cases filed by Women", "Total Cases filed by Senior Citizens"],
)


fig = px.choropleth(
    merged,
    geojson=merged.geometry,
    locations=merged.index,
    color=selected_variable,
    color_continuous_scale="speed",
    labels={selected_variable: selected_variable},
    title=f"Pending cases: {selected_variable}",
)


fig.update_geos(fitbounds="locations", visible=False)

fig.update_layout(autosize=False, width=1800, height=900)

st.plotly_chart(fig)


########box plot
duration_attributes = [
    "Pending cases for a period of 0 to 1 years",
    "Pending cases for a period of 1 to 3 years",
    "Pending cases for a period of 3 to 5 years",
    "Pending cases for a period of 5 to 10 years",
    "Pending cases for a period of 10 to 20 years",
    "Pending cases for a period of 20 to 30 years",
]

unique_states = df["State"].unique()

st.title("District-wise Pending Cases by Case Duration")

selected_state = st.selectbox("Select a State", unique_states)

state_df = df[df["State"] == selected_state]
state_df = state_df[["District"] + duration_attributes]
melted_df = pd.melt(
    state_df, id_vars=["District"], var_name="Duration", value_name="Pending Cases"
)

fig = px.box(
    melted_df,
    x="District",
    y="Pending Cases",
    color="Duration",
    title=f"{selected_state} - District-wise Pending Cases by Case Duration",
)

fig.update_layout(xaxis_title="District", yaxis_title="Pending Cases")
fig.update_layout(autosize=False, width=1800, height=900)

st.plotly_chart(fig)
