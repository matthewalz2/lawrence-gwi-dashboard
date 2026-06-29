#DEMOGRAPHIC FUNCTIONS
from utils.processing import age_gender_processing, demo_race_processing, demo_hispanic_processing

#EDUCATION FUNCTIONS
from utils.processing import edu_attainment_processing, edu_enrollment_processing, edu_tech_access_processing, edu_internet_processing

#PLOTTING LIBRARIES
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.data_loader import read_csv_fallback


#Read in the raw data for each tab
demo = read_csv_fallback('data/Lawrence_Demographics.csv')
edu = read_csv_fallback('data/Lawrence_Education.csv')

#CLEANED DEMOGRAPHIC DATAFRAMES
demo_age_gender = age_gender_processing(demo)
demo_race = demo_race_processing(demo)
demo_hispanic = demo_hispanic_processing(demo)

#CLEANED EDUCATION DATAFRAMES
edu_attainment = edu_attainment_processing(edu)
edu_enrollment = edu_enrollment_processing(edu)
edu_tech_access = edu_tech_access_processing(edu)
edu_internet = edu_internet_processing(edu)



#🟩🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦DEMOGRAPHIC VISUALIZATION FUNCTIONS🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟩

#Population Distribution by Age and Gender (Almost identical to first iteration, but with some formatting and hover improvements)
def plot_age_gender(cleaned_age_gender):
    age_order = [
        "Under 5", "5–9", "10–17", "18–24", "25–34",
        "35–44", "45–54", "55–64", "65–74", "75–84", "85+"
    ]

    age_df = cleaned_age_gender.copy()

    age_df["Age Group"] = pd.Categorical(
        age_df["Age Group"],
        categories=age_order,
        ordered=True
    )

    age_df = age_df.sort_values("Age Group")

    age_long = age_df.melt(
        id_vars=["Age Group", "total"],
        value_vars=["male_count", "female_count"],
        var_name="Gender",
        value_name="Count"
    )

    age_long["Gender"] = age_long["Gender"].replace({
        "male_count": "Male",
        "female_count": "Female"
    })

    fig = px.bar(
        age_long,
        x="Age Group",
        y="Count",
        color="Gender",
        barmode="stack",
        text="Count",
        color_discrete_map={
            "Male": "#4C78A8",
            "Female": "#E74C3C"
        },
        title="Population Distribution by Age and Gender in Lawrence, MA"
    )

    fig.update_traces(
        texttemplate="%{y:,.0f}",
        textposition="inside",
        hovertemplate=
        "<b>Age Group:</b> %{x}<br>" +
        "<b>Gender:</b> %{fullData.name}<br>" +
        "<b>Population:</b> %{y:,.0f}<extra></extra>"
    )

    fig.add_scatter(
        x=age_df["Age Group"],
        y=age_df["total"],
        text=age_df["total"].map("{:,.0f}".format),
        mode="text",
        textposition="top center",
        showlegend=False,
        hoverinfo="skip"
    )

    fig.update_yaxes(
        tickformat=",",
        title="Population"
    )

    fig.update_xaxes(
        title="Age Group"
    )

    fig.update_layout(
        title={
            "text": "Population Distribution by Age and Gender in Lawrence, MA",
            "x": 0.5
        },
        legend_title="Gender",
        template="plotly_white",
        bargap=0.15,
        height=550
    )

    return fig

def plot_race(cleaned_race):
    fig = go.Figure(
        go.Bar(
            x=cleaned_race["values"],
            y=cleaned_race["groups"],
            orientation="h",
            text=cleaned_race["values"].map("{:,.0f}".format),
            textposition="outside",
            marker_color="#2A9D8F",
            hovertemplate=
            "<b>%{y}</b><br>" +
            "Population: %{x:,.0f}<extra></extra>"
        )
    )

    fig.update_layout(
        title={
            "text": "Racial Distribution of Residents of Lawrence, MA",
            "x": 0.5
        },
        xaxis_title="Population",
        yaxis_title="",
        template="plotly_white",
        height=600,
        margin=dict(l=100, r=50, t=80, b=50)
    )

    fig.update_xaxes(
        tickformat=",",
        showgrid=True
    )

    fig.update_yaxes(
        categoryorder="array",
        categoryarray=cleaned_race["groups"].tolist()[::-1]
    )

    return fig

def plot_hispanic(cleaned_hispanic):
    fig = go.Figure(
        go.Bar(
            x=cleaned_hispanic["values"],
            y=cleaned_hispanic["group"],
            orientation="h",
            text=cleaned_hispanic["values"].map("{:,.0f}".format),
            textposition="outside",
            marker_color="#FFA200",
            hovertemplate=
            "<b>%{y}</b><br>" +
            "Population: %{x:,.0f}<extra></extra>"
        )
    )

    fig.update_layout(
        title={
            "text": "Hispanic Population in Lawrence, MA",
            "x": 0.5
        },
        xaxis_title="Population",
        yaxis_title="",
        template="plotly_white",
        height=600,
        margin=dict(l=100, r=50, t=80, b=50)
    )

    fig.update_xaxes(
        tickformat=",",
        showgrid=True
    )

    fig.update_yaxes(
        categoryorder="array",
        categoryarray=cleaned_hispanic["group"].tolist()[::-1]
    )

    return fig

#🟩🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦EDUCATION VISUALIZATION FUNCTIONS🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟩


#Education Attainment for Individuals 25+ in Lawrence, MA (Also similar to first iteration, but with some formatting and hover improvements)
def plot_attainment(cleaned_attainment):

    fig = go.Figure(
        go.Bar(
            x=cleaned_attainment["values"],
            y=cleaned_attainment["groups"],
            orientation="h",
            text=cleaned_attainment["values"].map("{:,.0f}".format),
            textposition="outside",
            marker_color="#4C78A8",
            hovertemplate=
            "<b>%{y}</b><br>" +
            "Population: %{x:,.0f}<extra></extra>"
        )
    )

    fig.update_layout(
        title={
            "text": "Educational Attainment for Individuals 25+ in Lawrence, MA",
            "x": 0.3
        },
        xaxis_title="Population",
        yaxis_title="",
        template="plotly_white",
        height=700,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    fig.update_xaxes(
        tickformat=",",
        showgrid=True
    )

    fig.update_yaxes(
        categoryorder="array",
        categoryarray=cleaned_attainment["groups"].tolist()[::-1]
    )

    return fig

#Education Enrollment for all residents of Lawrence, MA
def plot_enrollment(cleaned_enrollment):

    labels = cleaned_enrollment["groups"]
    values = cleaned_enrollment["values"]

    blue_palette = [
        "#08306B",  # dark navy
        "#08519C",
        "#2171B5",
        "#4292C6",
        "#6BAED6",
        "#9ECAE1",
        "#C6DBEF"
    ]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                marker=dict(colors=blue_palette),
                textinfo="percent+label",
                hovertemplate=
                "<b>%{label}</b><br>" +
                "Population: %{value:,.0f}<br>" +
                "Percent: %{percent}<extra></extra>"
            )
        ]
    )

    fig.update_layout(
        title={
            "text": "Residents of Lawrence, MA Enrolled in School",
            "x": 0.3
        },
        template="plotly_white",
        height=600,
        legend_title="Enrollment Status"
    )

    return fig


#Technology Access for households in Lawrence, MA
def plot_tech_access(cleaned_tech_access):

    fig = go.Figure(
        go.Bar(
            x=cleaned_tech_access["values"],
            y=cleaned_tech_access["groups"],
            orientation="h",
            text=cleaned_tech_access["values"].map("{:,.0f}".format),
            textposition="outside",
            marker_color="#4C78A8",
            hovertemplate=
            "<b>%{y}</b><br>" +
            "Households: %{x:,.0f}<extra></extra>"
        )
    )

    fig.update_layout(
        title={
            "text": "Household Device Access in Lawrence, MA",
            "x": 0.3
        },
        xaxis_title="Population",
        yaxis_title="",
        template="plotly_white",
        height=700,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    fig.update_xaxes(
        tickformat=",",
        showgrid=True
    )

    return fig

#Internet Access for households in Lawrence, MA
def plot_internet(cleaned_internet):
    fig = go.Figure(
        go.Bar(
            x=cleaned_internet["values"],
            y=cleaned_internet["groups"],
            orientation="h",
            text=cleaned_internet["values"].map("{:,.0f}".format),
            textposition="outside",
            marker_color="#007BFF",
            hovertemplate=
            "<b>%{y}</b><br>" +
            "Households: %{x:,.0f}<extra></extra>"
        )
    )

    fig.update_layout(
        title={
            "text": "Internet Access for Households in Lawrence, MA",
            "x": 0.3
        },
        xaxis_title="Population",
        yaxis_title="",
        template="plotly_white",
        height=700,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    fig.update_xaxes(
        tickformat=",",
        showgrid=True
    )

    return fig

#🟩🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦ECONOMIC/EMPLOYMENT VISUALIZATION FUNCTIONS🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟩
#plot commute data
def plot_commute(cleaned_commute):
  fig = go.Figure(
        go.Bar(
            x=cleaned_commute["values"],
            y=cleaned_commute["groups"],
            orientation="h",
            text=cleaned_commute["values"].map("{:,.0f}".format),
            textposition="outside",
            marker_color="#228B22",
            hovertemplate=
            "<b>%{y}</b><br>" +
            "Commuters: %{x:,.0f}<extra></extra>"
        )
    )

  fig.update_layout(
        title={
            "text": "Means of Transportation for Workers in Lawrence, MA (16+)",
            "x": 0.5
        },
        xaxis_title="Population",
        yaxis_title="",
        template="plotly_white",
        height=700,
        margin=dict(l=50, r=50, t=80, b=50)
    )

  fig.update_xaxes(
        tickformat=",",
        showgrid=True
    )


  return fig

#plot the labor force distribution
def plot_labor(cleaned_labor):

    labels = cleaned_labor["groups"]
    values = cleaned_labor["values"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                textinfo="percent+label",
                marker=dict(
                    colors=[
                        "#1B5E20",  # deep forest
                        "#2E7D32",  # forest green
                        "#388E3C",  # medium green
                        "#43A047",  # lighter green
                        "#66BB6A",  # soft green
                        "#81C784"   # sage green
                    ],
                    line=dict(color="white", width=2)
                ),
                hovertemplate=
                "<b>%{label}</b><br>" +
                "Individuals: %{value:,.0f}<br>" +
                "Percent: %{percent}<extra></extra>"
            )
        ]
    )

    fig.update_layout(
        title={
            "text": "Distribution of Labor Force (16+) in Lawrence, MA",
            "x": 0.5
        },
        template="plotly_white",
        height=600,
        legend_title="Labor Force Status"
    )

    return fig

def plot_com_length(cleaned_com_length):

    fig = go.Figure(
        go.Bar(
            x=cleaned_com_length["values"],
            y=cleaned_com_length["groups"],
            text=cleaned_com_length["values"].map("{:,.0f}".format),
            textposition="outside",
            orientation="h",
            marker=dict(
                color="#1B5E20",      # Forest green
                line=dict(
                    color="#0D3B12",  # Darker border
                    width=1
                )
            ),
            hovertemplate=
            "<b>%{y}</b><br>" +
            "Individuals: %{x:,.0f}<extra></extra>"
        )
    )

    fig.update_layout(
        title={
            "text": "Distribution of Commute Length in Lawrence, MA",
            "x": 0.5
        },
        xaxis_title="Population",
        yaxis_title="",
        template="plotly_white",
        height=700,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    fig.update_xaxes(
        tickformat=",",
        showgrid=True
    )

    # Preserve dataframe order
    fig.update_yaxes(
        categoryorder="array",
        categoryarray=cleaned_com_length["groups"].tolist()
    )

    return fig