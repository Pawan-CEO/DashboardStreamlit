import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample data
data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y1': [10, 20, 15, 25, 30],
    'y2': [5, 15, 10, 20, 25]
})

# Display initial graphs
fig1, ax1 = plt.subplots()
ax1.plot(data['x'], data['y1'])
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.plot(data['x'], data['y2'])
st.pyplot(fig2)

# Define interaction
point_clicked = st.radio("Select a point on graph 1:", data['x'])

# Find the corresponding y value in the second graph
corresponding_y2 = data.loc[data['x'] == point_clicked, 'y2'].values[0]

# Update the second graph based on the selection in the first graph
fig2, ax2 = plt.subplots()
ax2.plot(data['x'], data['y2'])
ax2.axhline(y=corresponding_y2, color='r', linestyle='--')
st.pyplot(fig2)
