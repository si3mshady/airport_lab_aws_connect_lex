import streamlit as st
import boto3, os

# Initialize the DynamoDB client
REGION = "us-east-1"

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Initialize the DynamoDB client with or without AWS credentials
if aws_access_key and aws_secret_key:
    dynamodb = boto3.client(
        'dynamodb',
        region_name=REGION,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
else:
    dynamodb = boto3.client('dynamodb', region_name=REGION)


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

# Function to retrieve all data related to a reservation
def get_reservation_data(reservation_id, trip_id):
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
        return None

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


def get_flight_reservation(reservation_id, trip_id):
    try:
        response = dynamodb.get_item(
            TableName='BookAFlight',
            Key={
                'ReservationID': {'S': reservation_id},
                'TripID': {'S': trip_id}
            }
        )
        item = response.get('Item')
        if item:
            reservation_data = {
                'ReservationID': item.get('ReservationID').get('S'),
                'TripID': item.get('TripID').get('S'),
                'PassengerInfo': item.get('PassengerInfo').get('M'),
                'FlightDetails': item.get('FlightDetails').get('M'),
                'BookingStatus': item.get('BookingStatus').get('S')
            }
            return reservation_data
        else:
            return None
    except Exception as e:
        return None

# # Function to check if a reservation exists in the 'BookAFlight' table
# def reservation_exists(reservation_id, trip_id):
#     try:
#         response = dynamodb.get_item(
#             TableName='BookAFlight',
#             Key={
#                 'ReservationID': {'S': reservation_id},
#                 'TripID': {'S': trip_id}
#             }
#         )
#         return 'Item' in response
#     except Exception as e:
#         return False

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

def update_flight_status(flight_id, status):
    try:
        dynamodb.update_item(
            TableName='GetFlightStatus',
            Key={'FlightID': {'S': flight_id}},
            UpdateExpression='SET FlightStatus = :s',
            ExpressionAttributeValues={':s': {'S': status}}
        )
        return "Flight status updated successfully!"
    except Exception as e:
        return f"Error updating flight status: {str(e)}"

# Streamlit app
st.title("Flight Reservation System")

# Select an action
action = st.selectbox("Select an action", ["Book a Flight","View Reservation Details","Cancel Flight Reservation"])



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

        if booking_status == "Confirmed":
            # Update the flight status table
            update_result = update_flight_status(flight_number, "Booked")
            st.write(update_result)

if action == "View Reservation Details":
    st.header("View Reservation Details")
    reservation_id = st.text_input("Reservation ID")
    trip_id = st.text_input("Trip ID")

    if st.button("Retrieve Data"):
        reservation_data = get_reservation_data(reservation_id, trip_id)
        if reservation_data:
            st.subheader("Reservation Data:")
            passenger_info = reservation_data['PassengerInfo']['M']
            flight_details = reservation_data['FlightDetails']['M']
            st.write(f"Reservation ID: {reservation_data['ReservationID']['S']}")
            st.write(f"Trip ID: {reservation_data['TripID']['S']}")
            st.write(f"Booking Status: {reservation_data['BookingStatus']['S']}")
            st.subheader("Passenger Info:")
            st.write(f"Passenger Name: {passenger_info['PassengerName']['S']}")
            st.write(f"Passenger Age: {passenger_info['PassengerAge']['N']}")
            st.write(f"Passenger Gender: {passenger_info['PassengerGender']['S']}")
            st.subheader("Flight Details:")
            st.write(f"Flight Number: {flight_details['FlightNumber']['S']}")
            st.write(f"Departure Airport: {flight_details['DepartureAirport']['S']}")
            st.write(f"Arrival Airport: {flight_details['ArrivalAirport']['S']}")
        else:
            st.write("Reservation not found")


if action == "Cancel Flight Reservation":
    st.header("Cancel Flight Reservation")
    reservation_id = st.text_input("Reservation ID")
    trip_id = st.text_input("Trip ID")

    if st.button("Cancel Reservation"):
        result = cancel_reservation(reservation_id, trip_id)
        st.write(result)

