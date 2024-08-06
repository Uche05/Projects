#please ignore it results in an error I tried🤷‍♂️😓😭
'''import joblib
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Load the trained RandomForest model and encoders
rf_classifier = joblib.load(r"C:\Users\uchek\Downloads\rf_classifier.pkl")
label_encoder_noc = joblib.load(r"C:\Users\uchek\Downloads\label_encoder_noc.pkl")
label_encoder_discipline = joblib.load(r"C:\Users\uchek\Downloads\label_encoder_discipline.pkl")
label_encoder_event = joblib.load(r"C:\Users\uchek\Downloads\label_encoder_event.pkl")

# Load the dataset containing unique events/sports
events_data = pd.read_csv(r"C:\Users\uchek\Downloads\events.csv")

# Verify the column names
print(events_data.columns)

# Assume the correct column name is 'Event' for this example (update based on your file)
correct_column_name = 'sport'  # Replace 'Event' with the correct column name after verifying

# Get unique sports/events
unique_sports = events_data[correct_column_name].unique()

# Function to decode labels
def decode_labels(encoded_values, encoder):
    decoded_values = encoder.inverse_transform(encoded_values)
    return decoded_values

# Initialize the Dash app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Olympic Sports Prediction Dashboard"),
    dcc.Dropdown(
        id='sport-dropdown',
        options=[{'label': sport, 'value': sport} for sport in unique_sports],
        value=unique_sports[0]
    ),
    dcc.Graph(id='prediction-graph'),
    html.Div(id='debug-output')  # Add a div for debug output
])

# Callback to update the graph based on the selected sport
@app.callback(
    [Output('prediction-graph', 'figure'),
     Output('debug-output', 'children')],  # Add debug output to callback
    Input('sport-dropdown', 'value')
)
def update_graph(selected_sport):
    try:
        # Define the new data (example values, adjust as needed)
        new_data = pd.DataFrame({
            'Gold': [2],  # Example values, should be adjusted based on your use case
            'Silver': [1],
            'Bronze': [2],
            'Rank by Total': [1],
            'Female': [3],
            'Male': [4],
            'Total_Medals': [5],
            'Discipline': [selected_sport],  # Using the current sport
            'Event': [selected_sport]
        })

        # Apply encoding to new data
        new_data['Discipline_encoded'] = label_encoder_discipline.transform(new_data['Discipline'])
        new_data['Event_encoded'] = label_encoder_event.transform(new_data['Event'])

        # Prepare the feature set for prediction
        features = ['Gold', 'Silver', 'Bronze', 'Rank by Total', 'Female', 'Male', 'Total_Medals', 'Discipline_encoded', 'Event_encoded']
        X_new = new_data[features]

        # Predict the rank
        new_data['Predicted_Rank'] = rf_classifier.predict(X_new)

        # Decode the encoded columns for display
        new_data['Discipline'] = decode_labels(new_data['Discipline_encoded'], label_encoder_discipline)
        new_data['Event'] = decode_labels(new_data['Event_encoded'], label_encoder_event)

        # Create a plotly figure
        fig = px.bar(new_data, x='Discipline', y='Predicted_Rank', title=f"Predicted Rank for {selected_sport}")

        # Debugging information
        debug_info = f"Input data: {new_data.to_dict()}"

        return fig, debug_info

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return {}, error_message

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
