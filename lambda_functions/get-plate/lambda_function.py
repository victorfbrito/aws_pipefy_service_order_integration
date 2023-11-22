import json

def lambda_handler(event, context):
    # Extract car plate value from the Step Functions input
    car_plate = event.get('car_plate', None)

    # Check if the car plate parameter is missing
    if car_plate is None:
        error_message = "Missing 'car_plate' parameter in the Step Functions input."
        response = {
            'statusCode': 400,  # HTTP 400 Bad Request
            'body': json.dumps({'error': error_message})
        }
        return response

    # Print the car plate value for debugging
    print(f"Received car plate: {car_plate}")

    # Include car_plate in the response
    response = {
        'statusCode': 200
    }

    # Include car_plate in the output of the Lambda function
    output = {
        'plate': car_plate
    }

    # Return the response and the output
    return {
        'response': response,
        'output': output
    }
