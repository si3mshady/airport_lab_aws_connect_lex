import streamlit as st
import boto3


REGION = "us-east-1"
# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=REGION)  # Replace 'your-region' with your AWS region

# Function to interact with DynamoDB
def get_flight_status(flight_id):
    try:
        response = dynamodb.get_item(
            TableName='GetFlightStatus',
            Key={'FlightID': {'S': flight_id}}
        )
        return response.get('Item')
    except Exception as e:
        return f"Error fetching flight status: {str(e)}"

# Streamlit app
st.title("Flight Status Viewer")

# Select an action
action = st.selectbox("Select an action", ["View Flight Status"])

if action == "View Flight Status":
    st.header("View Flight Status")
    flight_id = st.text_input("Flight ID")

    if st.button("Get Flight Status"):
        flight_status_data = get_flight_status(flight_id)
        if flight_status_data:
            flight_status = flight_status_data.get('FlightStatus').get('S')
            st.write(f"Flight Status for {flight_id}: {flight_status}")
        else:
            st.write(f"Flight {flight_id} not found")
