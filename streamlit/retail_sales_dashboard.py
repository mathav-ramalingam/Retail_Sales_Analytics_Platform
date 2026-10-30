
import streamlit as st
import plotly.express as px
from snowflake.snowpark.context import get_active_session

st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)


# Dashboard header
st.title("📊 Retail Sales Analytics Platform")
st.markdown(
    "Explore retail performance, revenue trends, "
    "customer segments, and product insights."
)
st.caption("POWERED BY SNOWFLAKE - INTERACTIVE BUSINESS INTELLIGENCE")
st.divider()


session = get_active_session()

# Load filter options from Snowflake
filter_options = session.sql("""
    SELECT DISTINCT
        ORDER_YEAR,
        REGION,
        CATEGORY,
        SEGMENT
    FROM RETAIL_SALES_DB.ANALYTICS.RETAIL_SALES_VW
""").to_pandas()




# Toggleable sidebar filters
with st.sidebar:
    st.header("🎛️ Dashboard Filters")
    st.caption("Choose filters to update your dashboard")

    years = sorted(
        filter_options["ORDER_YEAR"].dropna().unique().tolist()
    )
    selected_year = st.selectbox(
        "Order Year", ["All"] + years
    )

    regions = sorted(
        filter_options["REGION"].dropna().unique().tolist()
    )
    selected_region = st.selectbox(
        "Region", ["All"] + regions
    )

    categories = sorted(
        filter_options["CATEGORY"].dropna().unique().tolist()
    )
    selected_category = st.selectbox(
        "Category", ["All"] + categories
    )

    segments = sorted(
        filter_options["SEGMENT"].dropna().unique().tolist()
    )
    selected_segment = st.selectbox(
        "Customer Segment", ["All"] + segments
    )


# st.subheader("Dashboard Filters")

# f1, f2, f3, f4 = st.columns(4)

# with f1:
#     years = sorted(filter_options["ORDER_YEAR"].dropna().unique().tolist())
#     selected_year = st.selectbox("Order Year", ["All"] + years)

# with f2:
#     regions = sorted(filter_options["REGION"].dropna().unique().tolist())
#     selected_region = st.selectbox("Region", ["All"] + regions)

# with f3:
#     categories = sorted(filter_options["CATEGORY"].dropna().unique().tolist())
#     selected_category = st.selectbox("Category", ["All"] + categories)

# with f4:
#     segments = sorted(filter_options["SEGMENT"].dropna().unique().tolist())
#     selected_segment = st.selectbox("Customer Segment", ["All"] + segments)



# Build safe SQL conditions from selected dropdown values
conditions = []

if selected_year != "All":
    conditions.append(f"ORDER_YEAR = {int(selected_year)}")

if selected_region != "All":
    safe_region = selected_region.replace("'", "''")
    conditions.append(f"REGION = '{safe_region}'")

if selected_category != "All":
    safe_category = selected_category.replace("'", "''")
    conditions.append(f"CATEGORY = '{safe_category}'")

if selected_segment != "All":
    safe_segment = selected_segment.replace("'", "''")
    conditions.append(f"SEGMENT = '{safe_segment}'")

where_clause = (
    " WHERE " + " AND ".join(conditions)
    if conditions else ""
)




# KPI cards update based on the selected filters
summary = session.sql(f"""
    SELECT
        COUNT(*) AS TOTAL_RECORDS,
        COUNT(DISTINCT ORDER_ID) AS UNIQUE_ORDERS,
        COUNT(DISTINCT CUSTOMER_ID) AS UNIQUE_CUSTOMERS,
        COALESCE(SUM(QUANTITY), 0) AS TOTAL_QUANTITY,
        COALESCE(SUM(SALES), 0) AS TOTAL_GROSS_SALES,
        COALESCE(SUM(NET_SALES), 0) AS TOTAL_NET_SALES
    FROM RETAIL_SALES_DB.ANALYTICS.RETAIL_SALES_VW
    {where_clause}
""").collect()[0]


# KPI cards — financial performance
st.subheader("💰 Sales Overview")

c1, c2 = st.columns(2)

c1.metric(
    "Net Sales",
    f"${summary['TOTAL_NET_SALES']:,.2f}",
    help="Total sales after applying discounts."
)
c2.metric(
    "Gross Sales",
    f"${summary['TOTAL_GROSS_SALES']:,.2f}",
    help="Total sales before applying discounts."
)
st.divider()



# KPI cards — operational overview
st.subheader("📊 Business Overview")

c3, c4, c5, c6 = st.columns(4)

c3.metric(
    "Total Records",
    f"{summary['TOTAL_RECORDS']:,}"
)

c4.metric(
    "Unique Orders",
    f"{summary['UNIQUE_ORDERS']:,}"
)

c5.metric(
    "Unique Customers",
    f"{summary['UNIQUE_CUSTOMERS']:,}"
)

c6.metric(
    "Total Quantity",
    f"{summary['TOTAL_QUANTITY']:,}"
)

st.divider()





# Yearly sales chart
st.subheader("📈 Yearly Net Sales Trend")

yearly_df = session.sql(f"""
    SELECT
        ORDER_YEAR,
        ROUND(SUM(NET_SALES), 2) AS TOTAL_NET_SALES,
        ROUND(SUM(SALES), 2) AS TOTAL_GROSS_SALES
    FROM RETAIL_SALES_DB.ANALYTICS.RETAIL_SALES_VW
    {where_clause}
    GROUP BY ORDER_YEAR
    ORDER BY ORDER_YEAR
""").to_pandas()

if not yearly_df.empty:
    yearly_df["ORDER_YEAR"] = yearly_df["ORDER_YEAR"].astype(str)

    fig_year = px.bar(
        yearly_df,
        x="ORDER_YEAR",
        y="TOTAL_NET_SALES",
        title="Yearly Net Sales After Discount",
        # labels={
        #     "ORDER_YEAR": "Order Year",
        #     "TOTAL_NET_SALES": "Net Sales ($)"
        # },
        # hover_data={
        #     "TOTAL_NET_SALES": ":,.2f",
        #     "TOTAL_GROSS_SALES": ":,.2f"
        # }
    )

    fig_year.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=20, r=20, t=70, b=20),
        title_x=0.02,
        xaxis_title="Order Year",
        yaxis_title="Net Sales ($)",
        showlegend=False
    )

    fig_year.update_yaxes(
        tickprefix="$",
        tickformat=",.0f",
        showgrid=True,
        gridcolor="lightgray"
    )

    fig_year.update_traces(
        marker_line_width=0,
        hovertemplate=(
            "Year: %{x}<br>"
            "Net Sales: $%{y:,.2f}<br>"
            "<extra></extra>"
        )
    )

    st.plotly_chart(fig_year, use_container_width=True)

else:
    st.info("No yearly data matches these filters.")

st.divider()





# Category and regional net sales charts
left, right = st.columns(2)

with left:
    st.subheader("📦 Net Sales by Category")

    category_df = session.sql(f"""
        SELECT
            CATEGORY,
            ROUND(SUM(NET_SALES), 2) AS TOTAL_NET_SALES,
            ROUND(SUM(SALES), 2) AS TOTAL_GROSS_SALES
        FROM RETAIL_SALES_DB.ANALYTICS.RETAIL_SALES_VW
        {where_clause}
        GROUP BY CATEGORY
        ORDER BY TOTAL_NET_SALES DESC
    """).to_pandas()

    if not category_df.empty:
        fig_category = px.bar(
            category_df,
            x="CATEGORY",
            y="TOTAL_NET_SALES",
            color="CATEGORY",
            title="Net Sales by Category",
            # labels={
            #     "CATEGORY": "Category",
            #     "TOTAL_NET_SALES": "Net Sales ($)"
            # },
            # hover_data={
            #     "TOTAL_NET_SALES": ":,.2f",
            #     "TOTAL_GROSS_SALES": ":,.2f"
            # }
        )
        
        fig_category.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(l=20, r=20, t=70, b=20),
            title_x=0.02,
            xaxis_title="Product Category",
            yaxis_title="Net Sales ($)",
            showlegend=True
        )

        fig_category.update_yaxes(
            tickprefix="$",
            tickformat=",.0f",
            showgrid=True,
            gridcolor="lightgray"
        )

        fig_category.update_traces(
            marker_line_width=0,
            hovertemplate=(
            "Category: %{x}<br>"
            "Net Sales: $%{y:,.2f}"
            "<extra></extra>"
            )
        )


        st.plotly_chart(fig_category, use_container_width=True)
    else:
        st.info("No category data matches these filters.")

with right:
    st.subheader("🌎 Net Sales by Region")

    region_df = session.sql(f"""
        SELECT
            REGION,
            ROUND(SUM(NET_SALES), 2) AS TOTAL_NET_SALES,
            ROUND(SUM(SALES), 2) AS TOTAL_GROSS_SALES
        FROM RETAIL_SALES_DB.ANALYTICS.RETAIL_SALES_VW
        {where_clause}
        GROUP BY REGION
        ORDER BY TOTAL_NET_SALES DESC
    """).to_pandas()

    if not region_df.empty:
        fig_region = px.bar(
            region_df,
            x="REGION",
            y="TOTAL_NET_SALES",
            color="REGION",
            title="Net Sales by Region",
            # labels={
            #     "REGION": "Region",
            #     "TOTAL_NET_SALES": "Net Sales ($)"
            # },
            # hover_data={
            #     "TOTAL_NET_SALES": ":,.2f",
            #     "TOTAL_GROSS_SALES": ":,.2f"
            # }
        )

        
        fig_region.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(l=20, r=20, t=70, b=20),
            title_x=0.02,
            xaxis_title="Region",
            yaxis_title="Net Sales ($)",
            showlegend=True
        )

        fig_region.update_yaxes(
            tickprefix="$",
            tickformat=",.0f",
            showgrid=True,
            gridcolor="lightgray"
        )

        fig_region.update_traces(
            marker_line_width=0,
            hovertemplate=(
            "Region: %{x}<br>"
            "Net Sales: $%{y:,.2f}"
            "<extra></extra>"
            )
        )

        st.plotly_chart(fig_region, use_container_width=True)
    else:
        st.info("No regional data matches these filters.")

st.divider()






# Customer segment analysis and shipping performance
left, right = st.columns(2)

with left:
    st.subheader("👥 Net Sales by Customer Segment")

    segment_df = session.sql(f"""
        SELECT
            SEGMENT,
            ROUND(SUM(NET_SALES), 2) AS TOTAL_NET_SALES,
            ROUND(SUM(SALES), 2) AS TOTAL_GROSS_SALES
        FROM RETAIL_SALES_DB.ANALYTICS.RETAIL_SALES_VW
        {where_clause}
        GROUP BY SEGMENT
        ORDER BY TOTAL_NET_SALES DESC
    """).to_pandas()

    if not segment_df.empty:
        fig_segment = px.pie(
            segment_df,
            names="SEGMENT",
            values="TOTAL_NET_SALES",
            title="Net Sales by Segment",
            # hole=0.4,
        )

        
        fig_segment.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(l=20, r=20, t=70, b=20),
            title_x=0.02,
            legend_title_text="Customer Segment"
        )   

        fig_segment.update_traces(
            textinfo="percent",
            # textinfo="percent+label",
            textposition="inside",
            hole=0.45,
            hovertemplate=(
                "Segment: %{label}<br>"
                "Net Sales: $%{value:,.2f}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )

        st.plotly_chart(fig_segment, use_container_width=True)
    else:
        st.info("No segment data matches these filters.")

with right:
    st.subheader("🚚 Shipping Performance")

    shipping_df = session.sql(f"""
        SELECT
            SHIP_MODE,
            ROUND(AVG(DAYS_TO_SHIP), 2) AS AVG_DAYS_TO_SHIP
        FROM RETAIL_SALES_DB.ANALYTICS.RETAIL_SALES_VW
        {where_clause}
        GROUP BY SHIP_MODE
        ORDER BY AVG_DAYS_TO_SHIP
    """).to_pandas()

    if not shipping_df.empty:
        fig_shipping = px.bar(
            shipping_df,
            x="SHIP_MODE",
            y="AVG_DAYS_TO_SHIP",
            text="AVG_DAYS_TO_SHIP",
            title="Average Days to Ship",
            # labels={
            #     "SHIP_MODE": "Shipping Mode",
            #     "AVG_DAYS_TO_SHIP": "Average Days"
            # }
        )
        
        fig_shipping.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(l=20, r=20, t=70, b=20),
            title_x=0.02,
            xaxis_title="Shipping Mode",
            yaxis_title="Average Days to Ship",
            showlegend=False
        )

        fig_shipping.update_yaxes(
            showgrid=True,
            gridcolor="lightgray",
            rangemode="tozero"
        )

        fig_shipping.update_traces(
            marker_line_width=0,
            texttemplate="%{y:.2f} days",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "Shipping Mode: %{x}<br>"
                "Average Days: %{y:.2f}"
                "<extra></extra>"
            )
        )

        
        st.plotly_chart(fig_shipping, use_container_width=True)
    else:
        st.info("No shipping data matches these filters.")

st.divider()




# Top 10 products — rank after applying all filters
st.subheader("🏆 Top 10 Products")

products_df = session.sql(f"""
    SELECT
        PRODUCT_ID,
        CATEGORY,
        SUB_CATEGORY,
        SUM(QUANTITY) AS TOTAL_QUANTITY,
        ROUND(SUM(SALES), 2) AS TOTAL_GROSS_SALES,
        ROUND(SUM(NET_SALES), 2) AS TOTAL_NET_SALES
    FROM RETAIL_SALES_DB.ANALYTICS.RETAIL_SALES_VW
    {where_clause}
    GROUP BY PRODUCT_ID, CATEGORY, SUB_CATEGORY
""").to_pandas()

if not products_df.empty:
    products_df["PRODUCT_ID"] = products_df["PRODUCT_ID"].astype(str)

    metric_choice = st.selectbox(
        "Rank products by",
        ["Net Sales", "Gross Sales", "Quantity"],
        key="global_product_metric"
    )

    metric_columns = {
        "Net Sales": "TOTAL_NET_SALES",
        "Gross Sales": "TOTAL_GROSS_SALES",
        "Quantity": "TOTAL_QUANTITY"
    }

    metric_labels = {
        "Net Sales": "Net Sales ($)",
        "Gross Sales": "Gross Sales ($)",
        "Quantity": "Quantity Sold"
    }

    metric_column = metric_columns[metric_choice]
    metric_label = metric_labels[metric_choice]

    top_products = (
        products_df.nlargest(10, metric_column)
        .sort_values(metric_column, ascending=True)
    )

    fig_products = px.bar(
        top_products,
        x=metric_column,
        y="PRODUCT_ID",
        color="CATEGORY",
        orientation="h",
        title=f"Top 10 Products by {metric_choice}",
        # labels={
        #     metric_column: metric_label,
        #     "PRODUCT_ID": "Product ID",
        #     "CATEGORY": "Category"
        # },
        hover_data=[
            "SUB_CATEGORY",
            "TOTAL_QUANTITY",
            "TOTAL_GROSS_SALES",
            "TOTAL_NET_SALES"
        ]
    )

    fig_products.update_layout(
        template="plotly_white",
        height=520,
        margin=dict(l=20, r=30, t=70, b=30),
        title_x=0.02,
        xaxis_title=metric_label,
        yaxis_title="Product ID",
        legend_title_text="Category"
    )

    fig_products.update_xaxes(
        showgrid=True,
        gridcolor="lightgray",
        rangemode="tozero"
    )

    fig_products.update_yaxes(
        showgrid=False
    )

    fig_products.update_traces(
        marker_line_width=0,
        hovertemplate=(
            "Product ID: %{y}<br>"
            f"{metric_label}: %{{x:,.2f}}<br>"
            "Category: %{customdata[0]}<br>"
            "Sub-category: %{customdata[1]}"
            "<extra></extra>"
            )
    )

    st.plotly_chart(fig_products, use_container_width=True)


    st.dataframe(
        top_products.sort_values(metric_column, ascending=False),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No products match these filters.")

