import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title = 'Supermarket Sales Dashboard',
                   page_icon = ':bar_chart:',
                   layout = 'wide'
)

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io = 'supermarkt_sales.xlsx',
        engine = 'openpyxl',
        sheet_name = 'supermarkt_sales',
        skiprows = 3,
        usecols = 'A:Q',
        nrows = 1000,
    )

    # ADD 'hour' COLUMN TO DATAFRAME
    df['hour'] = pd.to_datetime(df['Time'], format = "%H:%M:%S").dt.hour
    return df
df = get_data_from_excel()

# SIDEBAR (filters)
st.sidebar.header("Apply Filters Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options = df['City'].unique(),
    default = df['City'].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options = df['Customer_type'].unique(),
    default = df['Customer_type'].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options = df['Gender'].unique(),
    default = df['Gender'].unique()
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)


# MAIN PAGE
st.title(":bar_chart: Supermarket Sales Dashboard")
st.markdown('##')


# TOP KPI's (score cards)
total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection["Rating"].mean(),1)
star_rating = ":star:" * int(round(average_rating,0))
average_sale_by_transaction = round(df_selection['Total'].mean(),2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"$ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"$ {average_sale_by_transaction}")
    
st.markdown("---") # to seperate this section with the below sections


# SALES BY PRODUCT LINE (bar chart)
sales_by_product_line = (
    df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x='Total', # x-axis is the total sales
    y=sales_by_product_line.index, # y-aixs is the product line (in this case it is the index(1st column))
    orientation="h", # horizontal bar chart
    title="<b>Sales by Product Line</b> ",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template = "plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", # background color to transparent
    xaxis = (dict(showgrid=False)) # remove grid from x-axis
)


# SALES BY HOUR (bar chart)
sales_by_hour = (
    df_selection.groupby(by=['hour'])[['Total']].sum().sort_values(by='Total')
)
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total", 
    title="<b>Sales by Hour</b> ",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template = "plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis = dict(tickmode='linear'),
    plot_bgcolor="rgba(0,0,0,0)", 
    yaxis = (dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# HIDE STREAMLIT STYLE
#hide_st_style = """
#            <style>
#            #MainMenu {visibility: hidden;}
#            footer {visibility: hidden;}
#            header {visibility: hidden;}
#            </style>
#            """
#st.markdown(hide_st_style, unsafe_allow_html=True)