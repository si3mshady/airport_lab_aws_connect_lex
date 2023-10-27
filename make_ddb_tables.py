def setup():
    import boto3
    import os

    REGION = "us-east-1"

    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if aws_access_key and aws_secret_key:
        dynamodb = boto3.client(
            'dynamodb',
            region_name=REGION,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
    else:
        dynamodb = boto3.client('dynamodb', region_name=REGION)

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
