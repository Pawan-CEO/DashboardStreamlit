import streamlit as st
import pandas as pd
import altair as alt

# Sample data creation (replace this with your data)
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
)

# Create the bar chart
bar = alt.Chart(data).mark_bar().encode(
    x='Category',
    y='BarValues',
    color=alt.value('orange')
)

# Combine both charts
chart = alt.layer( bar,line).resolve_scale(
    y='independent'
)

# Adjust the width of the chart
# st.write(chart.properties(width=800))


# Display the chart with 100% available width
st.altair_chart(chart, use_container_width=True)
# Display the combined chart
# st.write(chart)
