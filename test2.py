import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd

st.set_page_config(page_title="Page Title", layout="wide")
# hide_menu_style="""
# <style>
# #MainMenu{visibility:hidden;}
# footer{visibility:hidden;}
# </style>
# """
# st.markdown(hide_menu_style,unsafe_allow_html=True)

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        header {z-index:-1}
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        body {top: 0;}

   
    </style>
""", unsafe_allow_html=True)

eprice,instore=st.tabs(["ePrice","InStore"])

with eprice:
    volume,accuracy,model_errors=st.tabs(["Volume","Accuracy","Model Errors"])

    # Volumne Code......................
    with volume:

        col1,col2=st.columns([1,1])
        with col1:
            st.subheader("Select Date Range")
            sub_col1,sub_col2,sub_col3,sub_col4=st.columns([1,1,1,1])
            sub_col1.date_input("Start Date")
            sub_col2.date_input("Last Date")
            accept_rate=56
            sub_col3.metric(label="Accept Rate", value=str(accept_rate)+" %")


            observations=70
            sub_col4.metric(label="Observations", value=str(observations)+" %")

            st.write("<h3><center>Accept Rate by Retailer</center></h3>",unsafe_allow_html=True)


            data = pd.DataFrame({
                'Category': ['A', 'B', 'C', 'D','E','F','G','H','I'],
                'LineValues': [10, 20, 15, 25,30,11,23,45,23],
                'BarValues': [200, 180, 210, 190, 210, 190,137,222,189]
            })

            # Create the line chart
            line = alt.Chart(data).mark_line(point=True).encode(
                x='Category',
                y='LineValues',
                color=alt.value('blue')
            ).properties(
                height=450  # Set the desired height of the chart (adjust as needed)
            )

            # Create the bar chart
            bar = alt.Chart(data).mark_bar().encode(
                x='Category',
                y='BarValues',
                color=alt.value('orange')
            ).properties(
                height=450  # Set the desired height of the chart (adjust as needed)
            )

            # Combine both charts
            chart = alt.layer( bar,line).resolve_scale(
                y='independent'
            )

            # Adjust the width of the chart
            # st.write(chart.properties(width=800))

            st.altair_chart(chart, use_container_width=True)



        with col2:


            st.write("<h3><center>Accept Rate Last 8 Weeks.</center></h3>",unsafe_allow_html=True)
            data = pd.DataFrame({
                'Category': ['A', 'B', 'C', 'D','E','F','G','H','I'],
                'LineValues': [10, 20, 15, 25,30,11,23,45,23]
            })

            # Create the line chart
            line = alt.Chart(data).mark_line(point=True).encode(
                x='Category',
                y='LineValues',
                color=alt.value('blue')
            ).properties(
                height=250  # Set the desired height of the chart (adjust as needed)
            )

            # Combine both charts
            chart = alt.layer(line).resolve_scale(
                x='independent'
            )

            # Display the chart with 100% available width
            st.altair_chart(chart, use_container_width=True)

            st.write("<h3><center>Accept Rate by Volatility.</center></h3>",unsafe_allow_html=True)            
            data = pd.DataFrame({
                'Category': ['A', 'B', 'C', 'D','E','F','G','H','I'],
                'LineValues': [45, 40, 32, 50,30,41,35,45,33],
                'BarValues': [200, 120, 70, 80, 78, 30,37,22,32]
            })

            # Create the line chart
            line = alt.Chart(data).mark_line(point=True).encode(
                x='Category',
                y='LineValues',
                color=alt.value('blue')
            ).properties(
                height=250  # Set the desired height of the chart (adjust as needed)
            )

            # Create the bar chart
            bar = alt.Chart(data).mark_bar().encode(
                x='Category',
                y='BarValues',
                color=alt.value('orange')
            ).properties(
                height=250  # Set the desired height of the chart (adjust as needed)
            )

            # Combine both charts
            chart = alt.layer( bar,line).resolve_scale(
                y='independent'
            )

            st.altair_chart(chart, use_container_width=True)

            st.write("<h3><center>Volatility</center></h3>",unsafe_allow_html=True)


    # Accuracy ..............................
    with accuracy:

        col1,col2=st.columns([1,1])
        with col1:

            # Select Date Widget.................
            st.subheader("Select Date Range")
            sub_col1,sub_col2=st.columns([1,1])
            with sub_col1:
                sub_col1.date_input("Start Date",key="accuracy_start_date")

            with sub_col2:
                st.date_input("Last Date",key="accuracy_last_date")

            # Output Vlaues......................

            sub_col1,sub_col2,sub_col3=st.columns([1,1,1])
            
            with sub_col1:
                total_accuracy=100
                st.metric(label="Accept Rate", value=str(total_accuracy)+" %")
            
            with sub_col2:
                accuracy_observations=7500
                st.metric(label="Observations",value=str(accuracy_observations)+" %")
            
            with sub_col3:
                false_positive=6
                st.metric(label="False Positives",value=str(false_positive)+" %")



    

            st.subheader('Dual Axis Chart in Streamlit')
            # Generate sample data
            x = np.linspace(0, 10, 100)
            y1 = np.sin(x)
            y2 = np.exp(x)

            fig, ax1 = plt.subplots()

            color = 'tab:red'
            ax1.set_xlabel('X axis')
            ax1.set_ylabel('Y1 - Sin', color=color)
            ax1.bar(x, y1, color=color)
            ax1.tick_params(axis='y', labelcolor=color)

            ax2 = ax1.twinx()
            color = 'tab:blue'
            ax2.set_ylabel('Y2 - Exp', color=color)
            ax2.plot(x, y2, color=color)
            ax2.tick_params(axis='y', labelcolor=color)

            st.pyplot(fig)


        with col2:

            st.subheader("Accept Rate Last 8 Weeks.")

            # Generate sample data
            x = np.linspace(0, 10, 100)
            y1 = np.sin(x)
            y2 = np.exp(x)

            # Create an interactive line chart using Streamlit
            st.line_chart(y1,height=200)
            st.subheader("Accept Rate by Volatility.")
            st.line_chart(y2,height=200)
            st.subheader("Volatility.")

        
        
        
        













