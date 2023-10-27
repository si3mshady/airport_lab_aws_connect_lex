import streamlit as st
import boto3

REGION = "us-east-1"

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=REGION)

# Streamlit app
st.title("Flight Reservation System")

# Function to check if a reservation exists in the 'BookAFlight' table
def reservation_exists(reservation_id, trip_id):
    try:
        response = dynamodb.get_item(
            TableName='BookAFlight',
            Key={
                'ReservationID': {'S': reservation_id},
                'TripID': {'S': trip_id}
            }
        )
        return 'Item' in response
    except Exception as e:
        return False

# Function to delete a reservation from the 'BookAFlight' table
def cancel_reservation(reservation_id, trip_id):
    if reservation_exists(reservation_id, trip_id):
        try:
            dynamodb.delete_item(
                TableName='BookAFlight',
                Key={
                    'ReservationID': {'S': reservation_id},
                    'TripID': {'S': trip_id}
                }
            )
            return "Reservation canceled successfully!"
        except Exception as e:
            return f"Error canceling reservation: {str(e)}"
    else:
        return "Reservation does not exist."

# Select an action
actions = ["Book a Flight", "View Flight Status", "Cancel Flight Reservation"]
action = st.selectbox("Select an action", actions)

if action == "Book a Flight":
    st.header("Book a Flight")
    # Your booking logic here...

if action == "View Flight Status":
    st.header("View Flight Status")
    # Your view flight status logic here...

if action == "Cancel Flight Reservation":
    st.header("Cancel Flight Reservation")
    reservation_id = st.text_input("Reservation ID")
    trip_id = st.text_input("Trip ID")

    if st.button("Cancel Reservation"):
        result = cancel_reservation(reservation_id, trip_id)
        st.write(result)
