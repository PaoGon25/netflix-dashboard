import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide"
)

# Load Data
df = pd.read_csv("netflix_titles.csv")

# Clean Data
df["country"] = df["country"].fillna("Unknown")
df["rating"] = df["rating"].fillna("Unknown")

# Sidebar
st.sidebar.title("Netflix Filters")

content_type = st.sidebar.selectbox(
    "Type",
    ["All", "Movie", "TV Show"]
)

selected_year = st.sidebar.selectbox(
    "Release Year",
    sorted(df["release_year"].unique(), reverse=True)
)

# Filter Data
filtered = df[df["release_year"] == selected_year]

if content_type != "All":
    filtered = filtered[filtered["type"] == content_type]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(filtered))
col2.metric(
    "Movies",
    len(filtered[filtered["type"] == "Movie"])
)
col3.metric(
    "TV Shows",
    len(filtered[filtered["type"] == "TV Show"])
)

st.divider()

# Movies vs TV Shows
type_counts = filtered["type"].value_counts()

if not type_counts.empty:
    fig1 = px.bar(
        x=type_counts.index,
        y=type_counts.values,
        title="Movies vs TV Shows",
        labels={"x":"Type","y":"Count"},
        color=type_counts.index
    )

    st.plotly_chart(fig1, use_container_width=True)

# Top Countries
country_counts = (
    filtered["country"]
    .value_counts()
    .head(10)
)

if not country_counts.empty:
    fig2 = px.bar(
        x=country_counts.values,
        y=country_counts.index,
        orientation="h",
        title="Top 10 Countries"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Rating Distribution
rating_counts = (
    filtered["rating"]
    .value_counts()
    .head(10)
)

if not rating_counts.empty:
    fig3 = px.pie(
        values=rating_counts.values,
        names=rating_counts.index,
        title="Rating Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

# Top Genres
genres = (
    filtered["listed_in"]
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)

if not genres.empty:
    fig4 = px.bar(
        x=genres.values,
        y=genres.index,
        orientation="h",
        title="Top 10 Genres"
    )

    st.plotly_chart(fig4, use_container_width=True)

# Data Table
st.subheader("Netflix Titles")

st.dataframe(
    filtered,
    use_container_width=True
)
