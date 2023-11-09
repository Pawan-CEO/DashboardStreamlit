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

def on_date_change_accuracy():
    temp_data=data.loc[(data["Date"] >= str(accuracy_start_date)) & (data["Date"] <= str(accuracy_last_date))]
    data_accept_rate=temp_data['Result_code'].value_counts()
    accept_rate=round(data_accept_rate["Accept"]/(data_accept_rate["Accept"]+data_accept_rate["Reject"])*100,2)
    st.session_state.accuracy_load=1
    return accept_rate,temp_data

def on_date_change_model_error():
    temp_data=data.loc[(data["Date"] >= str(model_errors_start_date)) & (data["Date"] <= str(model_errors_last_date))]
    data_accept_rate=temp_data['Result_code'].value_counts()
    accept_rate=round(data_accept_rate["Accept"]/(data_accept_rate["Accept"]+data_accept_rate["Reject"])*100,2)
    st.session_state.model_errors_load=1
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
            
            st.write("<br>",unsafe_allow_html=True)
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
            data_2 = pd.DataFrame({'Week': weeks, 'Score': scores})

            # Create the line chart
            line = alt.Chart(data_2).mark_line(point=True).encode(
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
            data_3 = pd.DataFrame({'Week': weeks, 'Accept': scores,'Observation':obs})
                       


            # Create the line chart
            line = alt.Chart(data_3).mark_line(point=True).encode(
                x='Week',
                y='Accept',
                color=alt.value('blue')
            ).properties(
                height=250  # Set the desired height of the chart (adjust as needed)
            )

            # Create the bar chart
            bar = alt.Chart(data_3).mark_bar().encode(
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


    # Accuracy ..............................
    with accuracy:
        

        col1,col2=st.columns([1,1])
        with col1:
            st.subheader("Select Date Range")
            sub_col1,sub_col2=st.columns([1,1])
            accuracy_start_date=sub_col1.date_input("Start Date",key="accuracy_start_date",value=date_min_value,min_value=date_min_value,max_value=date_max_value)
            accuracy_last_date=sub_col2.date_input("Last Date",key="accuracy_last_date",value=date_max_value,min_value=accuracy_start_date,max_value=date_max_value)
            
            accuracy_accept_rate,accuracy_temp_data=on_date_change_accuracy()
            
            st.write("<br><hr>",unsafe_allow_html=True)
            
            sub_col11,sub_col22,sub_col33=st.columns([1,1,1])
            
            if 'accuracy_load' not in st.session_state:
                temp_data=data

            sub_col11.metric(label="Accept Rate", value=str(accuracy_accept_rate)+" %")


            accuracy_observations=temp_data.shape[0]
            sub_col22.metric(label="Observations", value=str(accuracy_observations))

            accuracy_false_positives=10
            sub_col33.metric(label="False Positives", value=str(accuracy_false_positives))

            st.write("<br><hr>",unsafe_allow_html=True)

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
            data_21 = pd.DataFrame({'Week': weeks, 'Score': scores})

            # Create the line chart
            line = alt.Chart(data_21).mark_line(point=True).encode(
                x='Week',
                y='Score',
                color=alt.value('blue')
            ).properties(
                height=200  # Set the desired height of the chart (adjust as needed)
            )

            # Combine both charts
            chart = alt.layer(line).resolve_scale(
                x='independent'
            )

            # Display the chart with 100% available width
            st.altair_chart(chart, use_container_width=True)


            v_col1,v_col2=st.columns([1,1])
            with v_col1:

                st.write("<h4><center>Accept Rate by Volatility.</center></h4>",unsafe_allow_html=True) 

                # Generate data for 'Week' column (8 weeks)
                weeks = ["0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1"]
                # Generate random 'Score' values between 50 and 99 for each week
                scores = np.random.randint(50, 100, size=10)
                obs=np.random.randint(500,51000,size=10)
                # Create a DataFrame
                data_31 = pd.DataFrame({'Week': weeks, 'Accept': scores,'Observation':obs})
                        


                # Create the line chart
                line = alt.Chart(data_31).mark_line(point=True).encode(
                    y='Week',
                    x='Accept',
                    color=alt.value('blue')
                ).properties(
                    height=700  # Set the desired height of the chart (adjust as needed)
                )

                # Combine both charts
                chart = alt.layer(line).resolve_scale(
                    x='independent'
                )

                st.altair_chart(chart, use_container_width=True)

            with v_col2:
                st.write("<h4><center>Accuracy by Price from Mean</center></h4>",unsafe_allow_html=True)

                weeks = ["0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1"]

                # Generate random 'Score' values between 50 and 99 for each week
                scores = np.random.randint(50, 100, size=10)
                obs=np.random.randint(500,51000,size=10)
                # Create a DataFrame
                data_003 = pd.DataFrame({'Week': weeks, 'Accept': scores,'Observation':obs})
                        


                # Create the line chart
                line = alt.Chart(data_003).mark_line(point=True).encode(
                    y='Week',
                    x='Accept',
                    color=alt.value('blue')
                ).properties(
                    height=700  # Set the desired height of the chart (adjust as needed)
                )

                # Create the bar chart
                bar = alt.Chart(data_003).mark_bar().encode(
                    y='Week',
                    x='Observation',
                    color=alt.value('orange')
                ).properties(
                    height=700  # Set the desired height of the chart (adjust as needed)
                )

                # Combine both charts
                chart = alt.layer( bar,line).resolve_scale(
                    y='independent'
                )

                st.altair_chart(chart, use_container_width=True)

                

    with model_errors:

            st.subheader("Select Date Range")
            sub_col111,sub_col222,sub_col333,sub_col444,sub_col555=st.columns([1,1,1,1,1])
            model_errors_start_date=sub_col111.date_input("Start Date",key="model_errors_start_date",value=date_min_value,min_value=date_min_value,max_value=date_max_value)
            model_errors_last_date=sub_col222.date_input("Last Date",key="model_errors_last_date",value=date_max_value,min_value=accuracy_start_date,max_value=date_max_value)
            
            model_errors_accept_rate,model_errors_temp_data=on_date_change_model_error()
            

            if 'model_errors_load' not in st.session_state:
                temp_data=data

            sub_col333.metric(label="Accept Rate", value=str(accuracy_accept_rate)+" %")


            accuracy_observations=temp_data.shape[0]
            sub_col444.metric(label="Observations", value=str(accuracy_observations))

            accuracy_false_positives=10
            sub_col555.metric(label="False Positives", value=str(accuracy_false_positives))

            st.write("<hr>",unsafe_allow_html=True)

            col1,col2=st.columns([1,1])
            with col1:
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


                st.dataframe(data[:20],height=500)



