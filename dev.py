import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import datetime



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

#data input
data=pd.read_csv('data/output_updated.csv')


#Data Conversion
data["Date"]=pd.to_datetime(data['Date'])

# Convert 'DateColumn' to the desired date format ('yyyy-mm-dd')
data["Date"]=data["Date"].dt.strftime('%Y-%m-%d')




## Calculation

date_min_value=datetime.datetime.strptime(data["Date"].min(), '%Y-%m-%d').date()
date_max_value=datetime.datetime.strptime(data["Date"].max(), '%Y-%m-%d').date()
data_accept_rate=data['Result_code'].value_counts()
accept_rate=round(data_accept_rate["Accept"]/(data_accept_rate["Accept"]+data_accept_rate["Reject"])*100,2)



# Accept Rate   (Volume)

def on_date_change():
    temp_data=data.loc[(data["Date"] >= str(start_date)) & (data["Date"] <= str(last_date))]
    data_accept_rate=temp_data['Result_code'].value_counts()
    accept_rate=round(data_accept_rate["Accept"]/(data_accept_rate["Accept"]+data_accept_rate["Reject"])*100,2)
    st.session_state.load=1
    return accept_rate,temp_data

#first tab
eprice,instore=st.tabs(["ePrice","InStore"])

with eprice:

    #second tab
    volume,accuracy,model_errors=st.tabs(["Volume","Accuracy","Model Errors"])

    # Volumne Code......................
    with volume:

        col1,col2=st.columns([1,1])
        with col1:
            st.subheader("Select Date Range")
            sub_col1,sub_col2,sub_col3,sub_col4=st.columns([1,1,1,1])
            start_date=sub_col1.date_input("Start Date",value=date_min_value,min_value=date_min_value,max_value=date_max_value)
            last_date=sub_col2.date_input("Last Date",value=date_max_value,min_value=start_date,max_value=date_max_value)
            
            accept_rate,temp_data=on_date_change()
            
            if 'load' not in st.session_state:
                temp_data=data

            sub_col3.metric(label="Accept Rate", value=str(accept_rate)+" %")


            observations=temp_data.shape[0]
            sub_col4.metric(label="Observations", value=str(observations))

            st.write("<h3><center>Accept Rate by Retailer</center></h3>",unsafe_allow_html=True)

            banner_accept_count = temp_data[data['Result_code'] == 'Accept'].groupby('Banner').size()
            banner_total_count = temp_data.groupby('Banner').size()
            banner_scores = (banner_accept_count / banner_total_count * 100).round(2)


            # Create a DataFrame with 'Score' and 'Count' columns for each 'Banner'
            banner_scores_df = pd.DataFrame({
                'Volume': banner_total_count,
                'AcceptRate': banner_scores
            })

            banner_scores_df.reset_index(inplace=True)

          # Create the line chart
            line = alt.Chart(banner_scores_df).mark_line(point=True).encode(
                x='Banner',
                y='AcceptRate',
                color=alt.value('blue')
            ).properties(
                height=450  # Set the desired height of the chart (adjust as needed)
            )


            # Create the bar chart
            bar = alt.Chart(banner_scores_df).mark_bar().encode(
                x='Banner',
                y='Volume',
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
            # Generate data for 'Week' column (8 weeks)
            weeks = np.arange(1, 9)

            # Generate random 'Score' values between 50 and 99 for each week
            scores = np.random.randint(50, 100, size=8)

            # Create a DataFrame
            data = pd.DataFrame({'Week': weeks, 'Score': scores})

            # Create the line chart
            line = alt.Chart(data).mark_line(point=True).encode(
                x='Week',
                y='Score',
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
            # Generate data for 'Week' column (8 weeks)
            weeks = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

            # Generate random 'Score' values between 50 and 99 for each week
            scores = np.random.randint(50, 100, size=10)
            obs=np.random.randint(500,51000,size=10)
            # Create a DataFrame
            data = pd.DataFrame({'Week': weeks, 'Accept': scores,'Observation':obs})
                       


            # Create the line chart
            line = alt.Chart(data).mark_line(point=True).encode(
                x='Week',
                y='Accept',
                color=alt.value('blue')
            ).properties(
                height=250  # Set the desired height of the chart (adjust as needed)
            )

            # Create the bar chart
            bar = alt.Chart(data).mark_bar().encode(
                x='Week',
                y='Observation',
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


    # # Accuracy ..............................
    # with accuracy:

    #     col1,col2=st.columns([1,1])
    #     with col1:

    #         # Select Date Widget.................
    #         st.subheader("Select Date Range")
    #         sub_col1,sub_col2=st.columns([1,1])
    #         with sub_col1:
    #             sub_col1.date_input("Start Date",key="accuracy_start_date")

    #         with sub_col2:
    #             st.date_input("Last Date",key="accuracy_last_date")

    #         # Output Vlaues......................

    #         sub_col1,sub_col2,sub_col3=st.columns([1,1,1])
            
    #         with sub_col1:
    #             total_accuracy=100
    #             st.metric(label="Accept Rate", value=str(total_accuracy)+" %")
            
    #         with sub_col2:
    #             accuracy_observations=7500
    #             st.metric(label="Observations",value=str(accuracy_observations)+" %")
            
    #         with sub_col3:
    #             false_positive=6
    #             st.metric(label="False Positives",value=str(false_positive)+" %")



    

    #         st.subheader('Dual Axis Chart in Streamlit')
    #         # Generate sample data
    #         x = np.linspace(0, 10, 100)
    #         y1 = np.sin(x)
    #         y2 = np.exp(x)

    #         fig, ax1 = plt.subplots()

    #         color = 'tab:red'
    #         ax1.set_xlabel('X axis')
    #         ax1.set_ylabel('Y1 - Sin', color=color)
    #         ax1.bar(x, y1, color=color)
    #         ax1.tick_params(axis='y', labelcolor=color)

    #         ax2 = ax1.twinx()
    #         color = 'tab:blue'
    #         ax2.set_ylabel('Y2 - Exp', color=color)
    #         ax2.plot(x, y2, color=color)
    #         ax2.tick_params(axis='y', labelcolor=color)

    #         st.pyplot(fig)


    #     with col2:

    #         st.subheader("Accept Rate Last 8 Weeks.")

    #         # Generate sample data
    #         x = np.linspace(0, 10, 100)
    #         y1 = np.sin(x)
    #         y2 = np.exp(x)

    #         # Create an interactive line chart using Streamlit
    #         st.line_chart(y1,height=200)
    #         st.subheader("Accept Rate by Volatility.")
    #         st.line_chart(y2,height=200)
    #         st.subheader("Volatility.")

        
        
        
        













