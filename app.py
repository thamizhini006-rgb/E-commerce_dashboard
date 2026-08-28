
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("cleaned_dataset.csv")

# -----------------------------
# TITLE
# -----------------------------
st.title("🛒 E-Commerce Analysis Dashboard")
st.markdown("### Complete Sales, Customer & Payment Analysis")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📊 Dashboard Menu")

page = st.sidebar.radio(
    "Select Section",
    [
        "🏠 Overview",
        "📈 Sales Analysis",
        "💳 Payment Analysis",
        "👥 Customer Analysis",
        "🔍 Customer Search",
        "🧹 Data Quality",
        "📋 Data Preview"
    ]
)

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🔎 Filters")

filtered_df = df.copy()

# Payment filter
if "Payment_Method" in filtered_df.columns:

    payments = filtered_df["Payment_Method"].dropna().unique()

    selected_payment = st.sidebar.multiselect(
        "💳 Payment Method",
        payments
    )

    if selected_payment:
        filtered_df = filtered_df[
            filtered_df["Payment_Method"].isin(selected_payment)
        ]

# Amount filter
if "Total_Amount" in filtered_df.columns:

    min_amount = float(filtered_df["Total_Amount"].min())
    max_amount = float(filtered_df["Total_Amount"].max())

    if min_amount < max_amount:

        amount_range = st.sidebar.slider(
            "💰 Sales Amount Range",
            min_value=min_amount,
            max_value=max_amount,
            value=(min_amount, max_amount)
        )

        filtered_df = filtered_df[
            (filtered_df["Total_Amount"] >= amount_range[0]) &
            (filtered_df["Total_Amount"] <= amount_range[1])
        ]

# =========================================================
# OVERVIEW
# =========================================================

if page == "🏠 Overview":

    st.header("📌 Business Overview")

    total_sales = filtered_df["Total_Amount"].sum()
    total_orders = len(filtered_df)
    total_customers = filtered_df["Customer_ID"].nunique()
    avg_order = filtered_df["Total_Amount"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Sales",
        f"₹{total_sales:,.2f}"
    )

    col2.metric(
        "🛒 Total Orders",
        total_orders
    )

    col3.metric(
        "👥 Total Customers",
        total_customers
    )

    col4.metric(
        "💵 Average Order",
        f"₹{avg_order:,.2f}"
    )

    st.markdown("---")

    # -----------------------------
    # Payment Summary
    # -----------------------------

    if "Payment_Method" in filtered_df.columns:

        st.subheader("💳 Payment Method Summary")

        payment_sales = (
            filtered_df
            .groupby("Payment_Method")["Total_Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(9, 4))

        payment_sales.plot(
            kind="bar",
            ax=ax
        )

        ax.set_xlabel("Payment Method")
        ax.set_ylabel("Total Sales")
        ax.set_title("Payment Method-wise Sales")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

    # -----------------------------
    # Business Insights
    # -----------------------------

    st.subheader("💡 Business Insights")

    top_customer = (
        filtered_df
        .groupby("Customer_ID")["Total_Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    if len(top_customer) > 0:

        st.success(
            f"🏆 Highest spending customer: "
            f"{top_customer.index[0]} "
            f"with ₹{top_customer.iloc[0]:,.2f}"
        )

    if "Payment_Method" in filtered_df.columns:

        top_payment = (
            filtered_df
            .groupby("Payment_Method")["Total_Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        if len(top_payment) > 0:

            st.info(
                f"💳 Highest sales payment method: "
                f"{top_payment.index[0]}"
            )

# =========================================================
# SALES ANALYSIS
# =========================================================

elif page == "📈 Sales Analysis":

    st.header("📈 Sales Analysis")

    sales = filtered_df["Total_Amount"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"₹{sales.sum():,.2f}")
    col2.metric("Average", f"₹{sales.mean():,.2f}")
    col3.metric("Minimum", f"₹{sales.min():,.2f}")
    col4.metric("Maximum", f"₹{sales.max():,.2f}")

    st.subheader("📊 Sales Distribution")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        sales,
        bins=20
    )

    ax.set_title("Sales Distribution")
    ax.set_xlabel("Total Amount")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

    st.subheader("📋 Sales Statistics")

    st.dataframe(
        sales.describe().to_frame("Value"),
        use_container_width=True
    )

# =========================================================
# PAYMENT ANALYSIS
# =========================================================

elif page == "💳 Payment Analysis":

    st.header("💳 Payment Method Analysis")

    payment_sales = (
        filtered_df
        .groupby("Payment_Method")["Total_Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.dataframe(
        payment_sales.to_frame("Total Sales"),
        use_container_width=True
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    payment_sales.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Payment Method-wise Sales")
    ax.set_xlabel("Payment Method")
    ax.set_ylabel("Total Sales")

    plt.xticks(rotation=45)

    st.pyplot(fig)

# =========================================================
# CUSTOMER ANALYSIS
# =========================================================

elif page == "👥 Customer Analysis":

    st.header("👥 Customer Analysis")

    customer_sales = (
        filtered_df
        .groupby("Customer_ID")["Total_Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.subheader("🏆 Top 10 Customers")

    top10 = customer_sales.head(10)

    st.dataframe(
        top10.to_frame("Total Sales"),
        use_container_width=True
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    top10.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Top 10 Customers by Sales")
    ax.set_xlabel("Customer ID")
    ax.set_ylabel("Total Sales")

    plt.xticks(rotation=45)

    st.pyplot(fig)

# =========================================================
# CUSTOMER SEARCH
# =========================================================

elif page == "🔍 Customer Search":

    st.header("🔍 Customer Search")

    customers = (
        filtered_df["Customer_ID"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_customer = st.selectbox(
        "Select Customer ID",
        customers
    )

    customer_data = filtered_df[
        filtered_df["Customer_ID"] == selected_customer
    ]

    st.subheader("Customer Purchase Details")

    st.dataframe(
        customer_data,
        use_container_width=True
    )

    total = customer_data["Total_Amount"].sum()

    st.metric(
        "Customer Total Sales",
        f"₹{total:,.2f}"
    )

# =========================================================
# DATA QUALITY
# =========================================================

elif page == "🧹 Data Quality":

    st.header("🧹 Data Quality Analysis")

    missing = int(
        filtered_df.isnull().sum().sum()
    )

    duplicates = int(
        filtered_df.duplicated().sum()
    )

    rows = len(filtered_df)
    columns = len(filtered_df.columns)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", rows)
    col2.metric("Columns", columns)
    col3.metric("Missing Values", missing)
    col4.metric("Duplicate Rows", duplicates)

    st.subheader("Missing Values by Column")

    missing_data = (
        filtered_df
        .isnull()
        .sum()
        .sort_values(ascending=False)
    )

    st.dataframe(
        missing_data.to_frame("Missing Values"),
        use_container_width=True
    )

    st.subheader("Data Types")

    st.dataframe(
        filtered_df.dtypes.astype(str).to_frame("Data Type"),
        use_container_width=True
    )

# =========================================================
# DATA PREVIEW
# =========================================================

elif page == "📋 Data Preview":

    st.header("📋 Dataset Preview")

    st.subheader("First 5 Rows")

    st.dataframe(
        filtered_df.head(),
        use_container_width=True
    )

    st.subheader("Last 5 Rows")

    st.dataframe(
        filtered_df.tail(),
        use_container_width=True
    )

    st.subheader("Complete Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =========================================================
# DOWNLOAD
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Download")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.sidebar.download_button(
    "⬇️ Download Filtered Data",
    csv_data,
    "filtered_ecommerce_data.csv",
    "text/csv"
)

st.sidebar.success("Dashboard Ready ✅")
