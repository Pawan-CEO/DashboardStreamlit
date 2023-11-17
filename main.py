import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import datetime
import random

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


#Temp Basis changes
list_of_state=['CA', 'MA', 'NY', 'GA', 'VA', 'NC', 'PA', 'MD', 'NJ', 'IL', 'WA', 'FL', 'LA', 'PR', 'QC', 'BC', 'WI', 'KS', 'TX', 'TN', 'MI', 'AZ', 'OR', 'MO', 'OH', 'MS', 'CT', 'AL', 'MN', 'IN', 'KY', 'SC', 'AR', 'IA', 'OK', 'DE', 'WV', 'SD', 'DC', 'NH', 'NV', 'NE', 'RI', 'ND', 'CO', 'ME', 'UT', 'NM', 'VT', 'AK']
data['State'] = random.choices(list_of_state, k=len(data))


#Data Conversion
data["Date"]=pd.to_datetime(data['Date'])

# Convert 'DateColumn' to the desired date format ('yyyy-mm-dd')
data["Date"]=data["Date"].dt.strftime('%Y-%m-%d')




## Calculation

date_min_value=datetime.datetime.strptime(data["Date"].min(), '%Y-%m-%d').date()
date_max_value=datetime.datetime.strptime(data["Date"].max(), '%Y-%m-%d').date()
data_accept_rate=data['Result_code'].value_counts()
accept_rate=round(data_accept_rate["Accept"]/(data_accept_rate["Accept"]+data_accept_rate["Reject"])*100,2)

#-------------------------------------------- second data

data_validation=pd.read_csv("data/Validation_data2.csv")

#Data Conversion
data_validation["Date"]=pd.to_datetime(data_validation['Date'])

# Convert 'DateColumn' to the desired date format ('yyyy-mm-dd')
data_validation["Date"]=data_validation["Date"].dt.strftime('%Y-%m-%d')



## Calculation

date_min_value_accuracy=datetime.datetime.strptime(data_validation["Date"].min(), '%Y-%m-%d').date()
date_max_value_accuracy=datetime.datetime.strptime(data_validation["Date"].max(), '%Y-%m-%d').date()
data_accept_rate_accuracy=data_validation['Result_code'].value_counts()
accept_rate_accuracy=round(data_accept_rate_accuracy["Accept"]/(data_accept_rate_accuracy["Accept"]+data_accept_rate_accuracy["Reject"])*100,2)

# Accept Rate   (Volume)

def on_date_change():
    temp_data=data.loc[(data["Date"] >= str(start_date)) & (data["Date"] <= str(last_date))]
    data_accept_rate=temp_data['Result_code'].value_counts()
    accept_rate=round(data_accept_rate["Accept"]/(data_accept_rate["Accept"]+data_accept_rate["Reject"])*100,2)
    st.session_state.load=1
    return accept_rate,temp_data

def on_date_change_accuracy():
    temp_data=data_validation.loc[(data_validation["Date"] >= str(accuracy_start_date)) & (data_validation["Date"] <= str(accuracy_last_date))]
    data_accept_rate=temp_data['Result_code'].value_counts()
    accept_rate=round(data_accept_rate["Accept"]/(data_accept_rate["Accept"]+data_accept_rate["Reject"])*100,2)
    st.session_state.accuracy_load=1
    return accept_rate,temp_data

def on_date_change_model_error():
    temp_data=data_validation.loc[(data_validation["Date"] >= str(model_errors_start_date)) & (data_validation["Date"] <= str(model_errors_last_date))]
    data_accept_rate=temp_data['Result_code'].value_counts()
    accept_rate=round(data_accept_rate["Accept"]/(data_accept_rate["Accept"]+data_accept_rate["Reject"])*100,2)
    st.session_state.model_errors_load=1
    return accept_rate,temp_data

def on_date_change_rejected_prevalent_items():
    temp_data=data_validation.loc[(data_validation["Date"] >= str(model_errors_start_date)) & (data_validation["Date"] <= str(model_errors_last_date))]
    data_accept_rate=temp_data['Result_code'].value_counts()
    accept_rate=round(data_accept_rate["Accept"]/(data_accept_rate["Accept"]+data_accept_rate["Reject"])*100,2)
    st.session_state.model_errors_load=1
    return accept_rate,temp_data


#first tab
eprice,instore=st.tabs(["ePrice","InStore"])

with eprice:

    #second tab
    volume,accuracy,model_errors,rejected_prevalent_items=st.tabs(["Volume","Model Accuracy","Model Errors","Rejected Prevalent Items"])

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
# Graph 1
            st.write("<br>",unsafe_allow_html=True)
            st.write("<h3><center>Accept Rate by Retailer</center></h3>",unsafe_allow_html=True)

            banner_accept_count = temp_data[data['Result_code'] == 'Accept'].groupby('Banner').size()
            banner_total_count = temp_data.groupby('Banner').size()
            banner_scores = (banner_accept_count / banner_total_count * 100).round(2)


            # Create a DataFrame with 'Score' and 'Count' columns for each 'Banner'
            banner_scores_df = pd.DataFrame({
                'Total Volume': banner_total_count,
                'Accept Rate': banner_scores
            })

            banner_scores_df['Accept Rate'] = banner_scores_df['Accept Rate'] / 100
            banner_scores_df.reset_index(inplace=True)


            sort_order = banner_scores_df.sort_values(by="Total Volume", ascending=False)['Banner'].tolist()


            line = alt.Chart(banner_scores_df).mark_line(point=True).encode(
                x=alt.X('Banner',sort=sort_order),
                y=alt.Y('Accept Rate:Q', axis=alt.Axis(format=' %')),  # Use the format parameter to add %
                color=alt.value('blue')
            ).properties(
                height=450  # Set the desired height of the chart (adjust as needed)
            )

            # Create the bar chart
            bar = alt.Chart(banner_scores_df).mark_bar().encode(
                x=alt.X('Banner',sort=sort_order),
                y=alt.Y('Total Volume'),
                color=alt.value('orange')
            ).properties(
                height=450  # Set the desired height of the chart (adjust as needed)
            )

            # Combine both charts
            chart = alt.layer( bar,line).resolve_scale(
                y='independent'
            )

            # Adjust the width of the chart
            st.altair_chart(chart, use_container_width=True)



        with col2:


            st.write("<h3><center>Accept Rate Last 8 Weeks.</center></h3>",unsafe_allow_html=True)
            # Generate data for 'Week' column (8 weeks)
            weeks = ['Week 1','Week 2','Week 3','Week 4','Week 5','Week 6','Week 7','Week 8']

            # Generate random 'Score' values between 50 and 99 for each week
            scores = np.random.randint(50, 100, size=8)

            # Create a DataFrame
            data_2 = pd.DataFrame({'Week': weeks, 'Score': scores})

            # Create the line chart
            line = alt.Chart(data_2).mark_line(point=True).encode(
                x=alt.X('Week',axis=alt.Axis(labelAngle=0)),
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


#..............................

            st.write("<h3><center>Accept Rate by State.</center></h3>",unsafe_allow_html=True) 
            # Generate data for 'Week' column (8 weeks)
            state_accept_count = temp_data[data['Result_code'] == 'Accept'].groupby('State').size()
            state_total_count = temp_data.groupby('State').size()
            state_scores = (state_accept_count / state_total_count * 100).round(2)


            # Create a DataFrame with 'Score' and 'Count' columns for each 'Banner'
            state_scores_df = pd.DataFrame({
                'Total Volume': state_total_count,
                'Accept Rate': state_scores
            })

            state_scores_df['Accept Rate'] = state_scores_df['Accept Rate'] / 100
            state_scores_df.reset_index(inplace=True)

    
            sort_order = state_scores_df.sort_values(by="Total Volume", ascending=False)['State'].tolist()


            line = alt.Chart(state_scores_df).mark_line(point=True).encode(
                x=alt.X('State',sort=sort_order),
                y=alt.Y('Accept Rate:Q', axis=alt.Axis(format=' %')),  # Use the format parameter to add %
                color=alt.value('blue')
            ).properties(
                height=450  # Set the desired height of the chart (adjust as needed)
            )

            # Create the bar chart
            bar = alt.Chart(state_scores_df).mark_bar().encode(
                x=alt.X('State',sort=sort_order),
                y=alt.Y('Total Volume'),
                color=alt.value('orange')
            ).properties(
                height=450  # Set the desired height of the chart (adjust as needed)
            )

            # Combine both charts
            chart = alt.layer( bar,line).resolve_scale(
                y='independent'
            )

            # Adjust the width of the chart
            st.altair_chart(chart, use_container_width=True)

#.....................................................
    # Accuracy ..............................
    with accuracy:
        
        col1,col2=st.columns([1,1])
        with col1:
            st.subheader("Select Date Range")
            sub_col1,sub_col2=st.columns([1,1])
            accuracy_start_date=sub_col1.date_input("Start Date",key="accuracy_start_date",value=date_min_value_accuracy,min_value=date_min_value_accuracy,max_value=date_max_value_accuracy)
            accuracy_last_date=sub_col2.date_input("Last Date",key="accuracy_last_date",value=date_max_value_accuracy,min_value=accuracy_start_date,max_value=date_max_value_accuracy)
            accuracy_accept_rate,accuracy_temp_data=on_date_change_accuracy()
            st.write("<br><hr>",unsafe_allow_html=True)
            
            sub_col11,sub_col22,sub_col33,sub_col44=st.columns([1,1,1,1])
            
            if 'accuracy_load' not in st.session_state:
                accuracy_temp_data=data_validation


            sub_col11.metric(label="Accept Rate", value=str(accuracy_accept_rate)+" %")


            accuracy_observations=accuracy_temp_data.shape[0]
            sub_col22.metric(label="Observations", value=str(accuracy_observations))
            # False Positive

            


            accuracy_false_positives= accuracy_temp_data.loc[(accuracy_temp_data["Result_code"]=="Accept") & (accuracy_temp_data["Manual Review"]=="Disagree")].shape[0]

            sub_col33.metric(label="False Positives", value=str(accuracy_false_positives))

            
            # False Negative

            accuracy_false_negatives=accuracy_temp_data.loc[(accuracy_temp_data["Result_code"]=="Reject") & (accuracy_temp_data["Manual Review"]=="Disagree")].shape[0]
            sub_col44.metric(label="False Negatives", value=str(accuracy_false_negatives))
            st.write("<br><hr>",unsafe_allow_html=True)

            st.write("<h3><center>Accept Rate by Retailer</center></h3>",unsafe_allow_html=True)

            banner_accept_count = accuracy_temp_data[accuracy_temp_data['Result_code'] == 'Accept'].groupby('BannerOwner').size()
            banner_total_count = accuracy_temp_data.groupby('BannerOwner').size()
            banner_scores = (banner_accept_count / banner_total_count * 100).round(2)


            # Create a DataFrame with 'Score' and 'Count' columns for each 'BannerOwner'
            banner_scores_df = pd.DataFrame({
                'Total Volume': banner_total_count,
                'Accept Rate': banner_scores
            })

            banner_scores_df.reset_index(inplace=True)

          # Create the line chart
            line = alt.Chart(banner_scores_df).mark_line(point=True).encode(
                x='BannerOwner',
                y='Accept Rate',
                color=alt.value('blue')
            ).properties(
                height=450  # Set the desired height of the chart (adjust as needed)
            )


            # Create the bar chart
            bar = alt.Chart(banner_scores_df).mark_bar().encode(
                x='BannerOwner',
                y='Total Volume',
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

#.......................................................            

    with model_errors:

            st.subheader("Select Date Range")
            sub_col111,sub_col222,sub_col333,sub_col444,sub_col555=st.columns([1,1,1,1,1])
            model_errors_start_date=sub_col111.date_input("Start Date",key="model_errors_start_date",value=date_min_value_accuracy,min_value=date_min_value_accuracy,max_value=date_max_value_accuracy)
            model_errors_last_date=sub_col222.date_input("Last Date",key="model_errors_last_date",value=date_max_value_accuracy,min_value=model_errors_start_date,max_value=date_max_value_accuracy)
            
            model_errors_accept_rate,model_errors_temp_data=on_date_change_model_error()
            

            if 'model_errors_load' not in st.session_state:
                model_errors_temp_data=data_validation

            model_error_false_positive_rate=(model_errors_temp_data.loc[(model_errors_temp_data["Result_code"]=="Accept") & (model_errors_temp_data["Manual Review"]=="Disagree")].shape[0])/100

            sub_col333.metric(label="False Positive Rate", value=str(model_error_false_positive_rate)+" %")

            model_errors_false_negative_rate=(model_errors_temp_data.loc[(model_errors_temp_data["Result_code"]=="Reject") & (model_errors_temp_data["Manual Review"]=="Disagree")].shape[0])/100
            sub_col444.metric(label="False Negative Rate", value=str(model_errors_false_negative_rate)+ " %")

            accuracy_false_positives=model_errors_temp_data.shape[0]
            sub_col555.metric(label="Observations", value=str(accuracy_false_positives))

            st.write("<hr>",unsafe_allow_html=True)

            col1,col2,col3=st.columns([3,8,3])

            with col1:
                pass

            with col2:
                st.dataframe(model_errors_temp_data[['BannerOwner','Scrape_Description','RegPrice']][:20].reset_index(drop=True),height=500)

            with col3:
                pass

#.....................................................
    with rejected_prevalent_items:

            st.subheader("Select Date Range")
            sub_col111,sub_col222,blank_111,sub_col333,sub_col444,sub_col555,sub_col666=st.columns([1,1,1,1,1,1,1])
            rejected_prevalent_items_start_date=sub_col111.date_input("Start Date",key="rejected_prevalent_items_start_date",value=date_min_value_accuracy,min_value=date_min_value_accuracy,max_value=date_max_value_accuracy)
            rejected_prevalent_items_last_date=sub_col222.date_input("Last Date",key="rejected_prevalent_items_last_date",value=date_max_value_accuracy,min_value=date_min_value_accuracy,max_value=date_max_value_accuracy)
            
            rejected_prevalent_items_accept_rate,rejected_prevalent_items_temp_data=on_date_change_model_error()
            

            if 'rejected_prevalent_items_load' not in st.session_state:
                rejected_prevalent_items_temp_data=data_validation

            rejected_prevalent_items_weeks_price=4

            sub_col333.metric(label="Weeks at Price", value=str(rejected_prevalent_items_weeks_price))

            rejected_prevalent_items_item_observations=100
            sub_col444.metric(label="Item Observations", value=str(rejected_prevalent_items_item_observations))

            rejected_prevalent_items_price_observations=50
            sub_col555.metric(label="Price Observations", value=str(accuracy_false_positives))

            rejected_prevalent_items_price_prevalence=50
            sub_col666.metric(label="Price Prevalence", value=str(rejected_prevalent_items_price_prevalence)+" %")
            st.write("<hr>",unsafe_allow_html=True)

            col1,col2,col3=st.columns([3,8,3])

            with col1:
                pass

            with col2:
                st.dataframe(model_errors_temp_data[['BannerOwner','Scrape_Description','RegPrice']][:20],height=500)

            with col3:
                pass


