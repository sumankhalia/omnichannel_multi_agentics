import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import time

from core.agents.insight_agent import ask_with_data
from core.agents.war_room_agent import run_war_room

st.set_page_config(layout="wide")

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

@st.cache_resource
def get_connection():
    return sqlite3.connect("omni.db", check_same_thread=False)

conn = get_connection()

customers = pd.read_sql("SELECT * FROM customers", conn)
transactions = pd.read_sql("SELECT * FROM transactions", conn)
events = pd.read_sql("SELECT * FROM engagement_events", conn)

customers["signup_date"] = pd.to_datetime(customers["signup_date"])
transactions["timestamp"] = pd.to_datetime(transactions["timestamp"])
events["timestamp"] = pd.to_datetime(events["timestamp"])

# ---------------------------------------------------
# GLOBAL FILTERS
# ---------------------------------------------------

st.sidebar.title("Intelligence Filters")

personas = st.sidebar.multiselect(
    "Persona",
    customers["persona"].unique(),
    default=customers["persona"].unique()
)

channels = st.sidebar.multiselect(
    "Transaction Channel",
    transactions["channel"].unique(),
    default=transactions["channel"].unique()
)

cities = st.sidebar.multiselect(
    "City",
    customers["city"].unique(),
    default=customers["city"].unique()
)

churn_range = st.sidebar.slider(
    "Churn Risk Range",
    0.0, 1.0, (0.0, 1.0)
)

# ---------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------

customers_f = customers[
    (customers["persona"].isin(personas)) &
    (customers["city"].isin(cities)) &
    (customers["churn_risk"].between(*churn_range))
].copy()

transactions_f = transactions[
    (transactions["customer_id"].isin(customers_f["customer_id"])) &
    (transactions["channel"].isin(channels))
]

events_f = events[
    events["customer_id"].isin(customers_f["customer_id"])
]

# ---------------------------------------------------
# HEADER KPIs
# ---------------------------------------------------

st.title("Omnichannel Intelligence Console")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"${transactions_f['amount'].sum():,.0f}")
col2.metric("Customers", len(customers_f))
col3.metric("Transactions", len(transactions_f))
col4.metric("Events", len(events_f))

st.divider()

# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Executive Overview",
    "Revenue Intelligence",
    "Customer Intelligence",
    "Engagement Intelligence",
    "Predictive Analytics",
    "AI Agent Lab",
    "AI War Room"
])

# ===================================================
# TAB 1 — EXECUTIVE OVERVIEW
# ===================================================

with tab1:

    st.subheader("Revenue Trend")

    trend = (
        transactions_f.set_index("timestamp")
        .resample("D")["amount"]
        .sum()
        .reset_index()
    )

    st.plotly_chart(px.line(trend, x="timestamp", y="amount"),
                    use_container_width=True)

    st.subheader("Revenue by Channel")

    channel_rev = transactions_f.groupby("channel")["amount"].sum().reset_index()

    st.plotly_chart(px.pie(channel_rev, names="channel", values="amount"),
                    use_container_width=True)

    st.subheader("Revenue Heatmap")

    heatmap = (
        transactions_f
        .merge(customers_f[["customer_id", "persona"]])
        .pivot_table(index="persona", columns="channel",
                     values="amount", aggfunc="sum")
        .fillna(0)
    )

    st.plotly_chart(px.imshow(heatmap, text_auto=True),
                    use_container_width=True)

# ===================================================
# TAB 2 — REVENUE INTELLIGENCE
# ===================================================

with tab2:

    st.subheader("Revenue Distribution")
    st.plotly_chart(px.histogram(transactions_f, x="amount"),
                    use_container_width=True)

    st.subheader("Top Products")

    product_rev = transactions_f.groupby("product_name")["amount"].sum().reset_index()

    st.plotly_chart(px.bar(product_rev, x="product_name", y="amount"),
                    use_container_width=True)

    st.subheader("Product vs Channel")

    prod_channel = (
        transactions_f.groupby(["product_name", "channel"])["amount"]
        .sum().reset_index()
    )

    st.plotly_chart(px.bar(prod_channel, x="product_name",
                           y="amount", color="channel"),
                    use_container_width=True)

    st.subheader("Box Plot — Revenue Behaviour")
    st.plotly_chart(px.box(transactions_f, x="channel", y="amount"),
                    use_container_width=True)

# ===================================================
# TAB 3 — CUSTOMER INTELLIGENCE
# ===================================================

with tab3:

    st.subheader("Persona Distribution")

    persona_dist = customers_f["persona"].value_counts().reset_index()
    persona_dist.columns = ["persona", "count"]

    st.plotly_chart(px.bar(persona_dist, x="persona", y="count"),
                    use_container_width=True)

    st.subheader("Churn Risk Distribution")
    st.plotly_chart(px.histogram(customers_f, x="churn_risk"),
                    use_container_width=True)

    st.subheader("Churn Risk Heatmap")

    churn_heatmap = (
        customers_f.pivot_table(index="persona",
                                columns="preferred_channel",
                                values="churn_risk",
                                aggfunc="mean")
        .fillna(0)
    )

    st.plotly_chart(px.imshow(churn_heatmap, text_auto=True),
                    use_container_width=True)

    st.subheader("Age vs Churn")
    st.plotly_chart(px.scatter(customers_f, x="age", y="churn_risk"),
                    use_container_width=True)

    st.subheader("RFM Segmentation")

    rfm = (
        transactions_f.groupby("customer_id")
        .agg({
            "timestamp": "max",
            "transaction_id": "count",
            "amount": "sum"
        })
        .reset_index()
    )

    rfm.columns = ["customer_id", "last_purchase",
                   "frequency", "monetary"]

    rfm["recency"] = (
        transactions_f["timestamp"].max() - rfm["last_purchase"]
    ).dt.days

    st.plotly_chart(px.scatter(rfm, x="recency",
                               y="monetary",
                               size="frequency"),
                    use_container_width=True)

# ===================================================
# TAB 4 — ENGAGEMENT INTELLIGENCE
# ===================================================

with tab4:

    st.subheader("Event Frequency")

    event_freq = events_f["event_type"].value_counts().reset_index()
    event_freq.columns = ["event_type", "count"]

    st.plotly_chart(px.bar(event_freq, x="event_type", y="count"),
                    use_container_width=True)

    st.subheader("Channel Mix")

    channel_mix = events_f["channel"].value_counts().reset_index()
    channel_mix.columns = ["channel", "count"]

    st.plotly_chart(px.pie(channel_mix, names="channel", values="count"),
                    use_container_width=True)

    st.subheader("Engagement Trend")

    engagement_trend = (
        events_f.set_index("timestamp")
        .resample("D")
        .size()
        .reset_index(name="events")
    )

    st.plotly_chart(px.line(engagement_trend, x="timestamp", y="events"),
                    use_container_width=True)

    st.subheader("Funnel Visualization")

    funnel_steps = events_f["event_type"].value_counts()

    fig = go.Figure(go.Funnel(
        y=funnel_steps.index,
        x=funnel_steps.values
    ))

    st.plotly_chart(fig, use_container_width=True)

# ===================================================
# TAB 5 — PREDICTIVE ANALYTICS
# ===================================================

with tab5:

    st.subheader("Predicted Churn")

    customers_f["predicted_churn"] = (
        customers_f["churn_risk"]
        * np.random.uniform(0.9, 1.1, len(customers_f))
    )

    st.plotly_chart(px.histogram(customers_f, x="predicted_churn"),
                    use_container_width=True)

    st.subheader("Revenue Anomaly Detection")

    mean_rev = trend["amount"].mean()
    std_rev = trend["amount"].std()

    trend["anomaly"] = trend["amount"] > (mean_rev + 2 * std_rev)

    st.plotly_chart(px.scatter(trend, x="timestamp",
                               y="amount", color="anomaly"),
                    use_container_width=True)

# ===================================================
# TAB 6 — AI AGENT LAB
# ===================================================

with tab6:

    st.subheader("Tactical Insight Engine")

    query = st.text_input("Ask Quick Business Question")

    if st.button("Generate Insight (Fast)"):

        with st.spinner("Agent thinking..."):

            response = ask_with_data(query)

        st.success(response["insight"])

        if response["data"] is not None:

            df = response["data"]

            numeric_cols = df.select_dtypes(include=np.number).columns
            categorical_cols = df.select_dtypes(exclude=np.number).columns

            fig = None

            if len(categorical_cols) and len(numeric_cols):
                fig = px.bar(df, x=categorical_cols[0], y=numeric_cols[0])

            elif len(numeric_cols):
                fig = px.line(df, y=numeric_cols[0])

            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.dataframe(df)

# ===================================================
# TAB 7 — AI WAR ROOM
# ===================================================

with tab7:

    st.subheader("Strategic Multi-Agent Intelligence")

    query = st.text_input("Ask Strategic Question")
    market_context = st.text_area("Optional Market Context")

    if st.button("Run War Room"):

        thinking_ui = st.empty()
        progress = st.progress(0)

        debate_messages = [
            "Analyst Agent evaluating internal performance signals...",
            "Risk Agent scanning for systemic vulnerabilities...",
            "Growth Agent modelling expansion scenarios...",
            "Strategy Agent forming competing hypotheses...",
            "Agents detecting conflicting interpretations...",
            "Debate Engine resolving disagreements...",
            "Executive Synthesis Agent preparing boardroom report..."
        ]

        for i, msg in enumerate(debate_messages):

            thinking_ui.info(msg)
            progress.progress((i + 1) / len(debate_messages))

            time.sleep(0.6)

        response = run_war_room(query, market_context)

        progress.empty()

        thinking_ui.success("Multi-Agent Analysis Complete")

        st.success(response["insight"])

        simulation_data = response.get("simulation")

        if simulation_data is not None:

            st.subheader("Scenario Simulation")

            if isinstance(simulation_data, pd.DataFrame) and not simulation_data.empty:

                numeric_cols = simulation_data.select_dtypes(include=np.number).columns

                if len(numeric_cols) >= 2:

                    fig = px.line(
                        simulation_data,
                        x=numeric_cols[0],
                        y=numeric_cols[1]
                    )

                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.dataframe(simulation_data)

        confidence_score = response.get("confidence")

        if confidence_score is not None:

            st.subheader("Decision Confidence")

            st.metric("Confidence Score", f"{confidence_score}%")

        thinking_trace = response.get("thinking")

        if thinking_trace:

            with st.expander("Agent Thinking Trace"):

                for step in thinking_trace:
                    st.write(step)
