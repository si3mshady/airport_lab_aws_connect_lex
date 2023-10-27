import boto3

REGION = "us-east-1"

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=REGION)

# Function to get all information for a flight reservation
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

# Example usage:
reservation_id = '12345'
trip_id = 'TRIP123'
reservation_info = get_flight_reservation(reservation_id, trip_id)
if reservation_info:
    print("Reservation Information:")
    print(reservation_info)
else:
    print("Reservation not found.")
