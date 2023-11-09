# import pandas as pd
# from difflib import get_close_matches

# # Sample data (replace this with your actual data)
# data_a = {
#     'EntityGLN': [
        
#         '0860010218204',
#         '0810123500000',
#         '0810223455600'
#         # ... (other EntityGLN values)
#     ]
# }

# data_b = {
#     'UPCPrefix': [
#         '8600',
#         '81012350',
#         '8600102182',
#         # ... (other UPCPrefix values)
#     ],
#     'PrefixString': [
#         '6978757',
#         '081012350',
#         '08600102182',
#         # ... (other PrefixString values)
#     ],
#     'CompanyName': [
#         'tst comp',
#         '香港路特科技有限公司',
#         '长沙高乐科技有限公司',
#         # ... (other CompanyName values)
#     ]
# }

# # Create DataFrames from the sample data
# df_a = pd.DataFrame(data_a)
# df_b = pd.DataFrame(data_b)

# # Function to find best match and update DataFrame A
# def find_best_match(row):
#     matches = get_close_matches(row['EntityGLN'], df_b['UPCPrefix'], n=1, cutoff=0.6)
#     if matches:
#         best_match = df_b[df_b['UPCPrefix'] == matches[0]]
#         return pd.Series(best_match.iloc[0])
#     else:
#         return pd.Series({})

# # Apply function to DataFrame A
# updated_df = df_a.apply(find_best_match, axis=1)

# # Update DataFrame A with the values from the best match in DataFrame B
# df_a = df_a.combine_first(updated_df)

# # Display the updated DataFrame A
# print(df_a)




##ss
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Sample DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'San Francisco', 'Los Angeles']
}
df = pd.DataFrame(data)

@app.route('/')
def index():
    html_content = render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
    
    # Save the rendered HTML content to a file
    with open('rendered_data.html', 'w') as file:
        file.write(html_content)

    return html_content

if __name__ == '__main__':
    app.run(debug=True)
