import streamlit as st
import boto3

# Initialize the DynamoDB client
REGION = "us-east-1"
dynamodb = boto3.client('dynamodb', region_name=REGION)  # Replace 'your-region' with your AWS region

# Function to interact with DynamoDB
def create_reservation(data):
    try:
        dynamodb.put_item(
            TableName='BookAFlight',
            Item=data
        )
        return "Reservation created successfully!"
    except Exception as e:
        return f"Error creating reservation: {str(e)}"

def get_reservation(reservation_id, trip_id):
    try:
        response = dynamodb.get_item(
            TableName='BookAFlight',
            Key={
                'ReservationID': {'S': reservation_id},
                'TripID': {'S': trip_id}
            }
        )
        return response.get('Item')
    except Exception as e:
        return f"Error fetching reservation: {str(e)}"

# Streamlit app
st.title("Flight Reservation System")

# Select an action
action = st.selectbox("Select an action", ["Book a Flight", "View Reservation Details"])

if action == "Book a Flight":
    st.header("Book a Flight")
    reservation_id = st.text_input("Reservation ID")
    trip_id = st.text_input("Trip ID")
    passenger_name = st.text_input("Passenger Name")
    passenger_age = st.number_input("Passenger Age", min_value=0, value=18)
    passenger_gender = st.selectbox("Passenger Gender", ["Male", "Female", "Other"])
    flight_number = st.text_input("Flight Number")
    departure_airport = st.text_input("Departure Airport")
    arrival_airport = st.text_input("Arrival Airport")
    booking_status = st.selectbox("Booking Status", ["Confirmed", "Pending", "Canceled"])

    if st.button("Create Reservation"):
        data = {
            'ReservationID': {'S': reservation_id},
            'TripID': {'S': trip_id},
            'PassengerInfo': {
                'M': {
                    'PassengerName': {'S': passenger_name},
                    'PassengerAge': {'N': str(passenger_age)},
                    'PassengerGender': {'S': passenger_gender}
                }
            },
            'FlightDetails': {
                'M': {
                    'FlightNumber': {'S': flight_number},
                    'DepartureAirport': {'S': departure_airport},
                    'ArrivalAirport': {'S': arrival_airport}
                }
            },
            'BookingStatus': {'S': booking_status}
        }

        result = create_reservation(data)
        st.write(result)

if action == "View Reservation Details":
    st.header("View Reservation Details")
    reservation_id = st.text_input("Reservation ID")
    trip_id = st.text_input("Trip ID")

    if st.button("View Reservation"):
        reservation_data = get_reservation(reservation_id, trip_id)
        if reservation_data:
            passenger_info = reservation_data.get('PassengerInfo').get('M')
            flight_details = reservation_data.get('FlightDetails').get('M')
            booking_status = reservation_data.get('BookingStatus').get('S')

            st.write("Passenger Info:", passenger_info)
            st.write("Flight Details:", flight_details)
            st.write(f"Booking Status: {booking_status}")
        else:
            st.write("Reservation not found")
