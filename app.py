import streamlit as st
import pandas as pd
import numpy as np
import decimal
import plotly.express as px
from streamlit_option_menu import option_menu
import mysql.connector as db
from query import *

st.set_page_config(page_title= "RedBus App", layout= "wide")
st.image("fc5b11fb-b135-4537-96ae-c3872b2164cb.jpeg")
st.title("Welcome to RedBus - My Seat My RedBus")

result = view_data()
col = [i[0] for i in curr.description]
df = pd.DataFrame(result, columns= col)

st.sidebar.image("redbus-app.webp", use_column_width= True, caption= "Redbus Web App")
st.sidebar.header("Please Filter Bus Route")
BusRouteName= st.sidebar.multiselect(
    "Select Bus Route Name", options= df["route_name"].unique()
    )

df_selection=df.query(
    "route_name==@BusRouteName"
    )

def Home():    
    col1,col2,col3,col4=st.columns(4, gap='large')
    with col1:
        top_bus_names = df_selection["bus_name"].value_counts().head(3).index.tolist()
        st.info('Top 3 Popular Bus Names:')
        for name in top_bus_names:
            st.write(name)
    with col2:
        top_bus_types= df_selection["bus_type"].value_counts().head(3).index.tolist()
        st.info('Top 3 Popular Bus Types:')
        for type in top_bus_types:
            st.write(type)
    with col3:
        Price_mean =df_selection["price"].mean()
        st.info("Average Price:")
        st.metric(label="Avg Price", value=f"{Price_mean:,.0f}")
    with col4:
        Star_rating =df_selection["star_rating"].mean()
        st.info("Average Star Rating:")
        st.metric(label="Avg Rating", value=f"{Star_rating:,.0f}")

    st.markdown("""---""")

def details(df_selection):
    col1,col2,col3,col4=st.columns(4, gap='large')
    with col1:
        bustype = st.selectbox("Select your bus type", options=["None"] + df_selection["bus_type"].unique().tolist())
        if bustype is "None":
            df_selection = df_selection
        else:
            df_selection = df_selection[df_selection["bus_type"] == bustype]
        st.write("You selected: ", bustype)
    with col2:
        df_selection['departing_time'] = df_selection['departing_time'].astype(str)
        df_selection['departing_time'] = df_selection['departing_time'].str.extract(r"(\d{2}:\d{2}:\d{2})")
        df_selection['reaching_time'] = df_selection['reaching_time'].astype(str)
        df_selection['reaching_time'] = df_selection['reaching_time'].str.extract(r"(\d{2}:\d{2}:\d{2})")
        departingtime = st.selectbox("Select departing time", options = ["None"] + df_selection["departing_time"].unique().tolist())
        if departingtime is "None":
            df_selection = df_selection
        else:
            df_selection = df_selection[df_selection["departing_time"] == departingtime]
        st.write("You selected: ", departingtime)

    with col3:
        df_selection["price"] = pd.to_numeric(df_selection["price"])
        price = st.selectbox("Price range in Rs : ", options = ("None", "100 - 300", "300 - 500", "500 - 700", "700 - 1000", "1000 above"))
        if price is "None":
            df_selection = df_selection
        if price == "100 - 300":
            df_selection = df_selection[(df_selection["price"] > decimal.Decimal("100")) & (df_selection["price"] <= decimal.Decimal("300"))]

        if price == "300 - 500":
            df_selection = df_selection[(df_selection["price"] > decimal.Decimal("300")) & (df_selection["price"] <= decimal.Decimal("500"))]

        if price == "500 - 700":
            df_selection = df_selection[(df_selection["price"] > decimal.Decimal("500")) & (df_selection["price"] <= decimal.Decimal("700"))]

        if price == "700 - 1000":
            df_selection = df_selection[(df_selection["price"] > decimal.Decimal("700")) & (df_selection["price"] <= decimal.Decimal("1000"))]

        if price == "1000 above":
            df_selection = df_selection[df_selection["price"] > decimal.Decimal("1000")]
        st.write("You selected: ", price)
        
    with col4:
        starrating = st.selectbox("Star Rating : ", options=["None", "⭐️⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️", "⭐️⭐️", "⭐️"])
        if starrating is "None":
            df_selection = df_selection
        if starrating == "⭐️⭐️⭐️⭐️⭐️":
            df_selection = df_selection[df_selection["star_rating"] == 5]

        if starrating == "⭐️⭐️⭐️⭐️":
            df_selection = df_selection[(df_selection["star_rating"] >= 4) & (df_selection["star_rating"] < 5)]

        if starrating == "⭐️⭐️⭐️":
            df_selection = df_selection[(df_selection["star_rating"] >= 3) & (df_selection["star_rating"] < 4)]

        if starrating == "⭐️⭐️":
            df_selection = df_selection[(df_selection["star_rating"] >= 2) & (df_selection["star_rating"] < 3)]

        if starrating == "⭐️":
            df_selection = df_selection[df_selection["star_rating"] < 2]
        st.write("You selected: ", starrating)

    return df_selection
    
def table():
    with st.expander("My Redbus Database"):
        shwdata=st.multiselect("Filter Dataset", df_selection.columns, default= ["bus_name", "bus_type", "departing_time", "duration","reaching_time","star_rating","price","seats_available"])
        st.dataframe(df_selection[shwdata], use_container_width = True)


with st.sidebar:
    menu = option_menu(
                menu_title = "Explore",
                options = ["Home", "Dashboard", "Route Links", "Customer Service"],
                styles = {
                    "nav-link-selected": {"background-color": "#FF4B4B"}
                }
    )
if menu=="Home":
    Home()
    df_selection = details(df_selection)
    table()
    
if menu=="Dashboard":
    Price_by_bus_route = (
        df_selection.groupby(by=["route_name"])
        .agg({"price": "max"})
        .sort_values(by="price", ascending=True)
    )
    fig_price = px.bar(
        Price_by_bus_route,
        x="price",
        y=Price_by_bus_route.index,
        orientation="h",
        title="Price by Bus Routes (Sorted)",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_scatter = px.scatter(
        df_selection,
        x="price",
        y="bus_type",
        title="Price vs. Bus Type",
        template="plotly_white",
        opacity=0.7  # Adjust the opacity value as needed
    )
    left,right=st.columns(2)
    left.plotly_chart(fig_price,use_container_width=True)
    right.plotly_chart(fig_scatter,use_container_width=True)
    st.markdown("""---""")

    fig2= px.pie(
        df_selection,
        names="bus_type",
        values="seats_available",
        title="Type of Buses wise Seat Availability",
        color_discrete_sequence=px.colors.sequential.Viridis,
        hole=0.4  # Adjust the hole size as needed
    )
    
    st.plotly_chart(fig2,use_container_width=True)


if menu=="Route Links":
    st.subheader("You selected Route Links")
    result1 = link()
    col = [i[0] for i in curr.description]
    data = pd.DataFrame(result1, columns= col)

    st.dataframe(data, column_config={"route_link": st.column_config.LinkColumn()})
    
    st.markdown("""---""")

    st.subheader("Popular Cities")

    popular_cities_data = get_popular_cities()
    popular_cities_df = pd.DataFrame(popular_cities_data, columns= [i[0] for i in curr.description])
    popular_cities_df = popular_cities_df.sort_values(by='route_name_count', ascending=False)

    # Create the line chart using Plotly Express
    fig = px.line(
        popular_cities_df,
        x='route_name',
        y='route_name_count',
        title='Popular Cities',
        markers=True  # Add markers for data points
    )

    # Customize the chart as needed (e.g., colors, labels, axis titles)
    fig.update_layout(
        xaxis_title='Route Name',
        yaxis_title='Route Name Count',
        xaxis_tickangle=-45  # Rotate x-axis labels for better readability
    )

    # Display the donut chart
    st.plotly_chart(fig,use_container_width=True)

if menu == "Customer Service":
    
    st.subheader("Write us your desired city which you couldn't find")
    name = st.text_input("Enter your Name")
    email = st.text_input("Enter your Email")
    origincity = st.text_input("Enter your origin city")
    destcity = st.text_input("Enter your destination city")
    bustype = st.text_input("Enter your desired bus type")
    if st.button("Submit"):
        result2 = users(name, email, origincity, destcity, bustype)
        st.success("Thank you for letting us know, check your email for the update on this!")
    
    
    st.subheader("Users desired cities which we will be updating soon")
    result = update()
    for row in result:
        st.write(row)
    st.markdown("""---""")
    
    st.caption("Rate your experience! (1 star: Needs Improvement - 5 stars: Excellent)")
    rating = st.radio("Choose your rating:", ("Needs Improvement", "Okay", "Good", "Very Good", "Excellent"))
    if st.button("Submit Feedback"):
        st.write(f"Thanks for your feedback! You selected {rating}.")
        store_feedback(rating)
    

    
