import boto3

REGION = "us-east-1"

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=REGION)  # Replace 'your-region' with your AWS region

# Define table schemas
tables = [
    {
        'TableName': 'BookAFlight',
        'KeySchema': [
            {
                'AttributeName': 'ReservationID',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'TripID',
                'KeyType': 'RANGE'
            }
        ],
        'AttributeDefinitions': [
            {
                'AttributeName': 'ReservationID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'TripID',
                'AttributeType': 'S'
            }
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    },
    {
        'TableName': 'GetFlightStatus',
        'KeySchema': [
            {
                'AttributeName': 'FlightID',
                'KeyType': 'HASH'
            }
        ],
        'AttributeDefinitions': [
            {
                'AttributeName': 'FlightID',
                'AttributeType': 'S'
            }
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    },
    {
        'TableName': 'GetReservationDetails',
        'KeySchema': [
            {
                'AttributeName': 'ReservationID',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'TripID',
                'KeyType': 'RANGE'
            }
        ],
        'AttributeDefinitions': [
            {
                'AttributeName': 'ReservationID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'TripID',
                'AttributeType': 'S'
            }
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    },
    # Define other table schemas similarly for the remaining use cases
]

# Create tables
for table in tables:
    try:
        response = dynamodb.create_table(**table)
        print(f"Table {table['TableName']} created. Status: {response['TableDescription']['TableStatus']}")
    except Exception as e:
        print(f"Error creating table {table['TableName']}: {str(e)}")
