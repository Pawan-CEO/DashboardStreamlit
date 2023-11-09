import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

eprice,instore=st.tabs(["ePrice","InStore"])

with eprice:
    volume,accuracy,model_errors=st.tabs(["Volume","Accuracy","Model Errors"])

    with volume:

        col1,col2,col3=st.columns([1,1,2])
        with col1:
            st.subheader("Select Date Range")
            sub_col1,sub_col2=st.columns([1,1])
            sub_col1.date_input("Start Date")
            sub_col2.date_input("Last Date")

        with col2:
            sub_col1,sub_col2=st.columns([1,1])
            st.subheader("pawan")
        
        
        


        graph_col1,graph_col2=st.columns([1,1])
        
        with graph_col1:
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

        with graph_col2:
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









