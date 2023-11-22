import json
import boto3

def lambda_handler(event, context):
    # Extract information from the S3 event
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    # Read the content of the JSON file from S3
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
    content = response['Body'].read().decode('utf-8')

    # Parse the JSON content and extract car_plate
    data = json.loads(content)
    car_plate = data.get('car_plate')

    if car_plate is None:
        print("Error: 'car_plate' not found in the uploaded JSON.")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing or invalid car_plate in the uploaded JSON'})
        }

    # Include car_plate in the input for Step Functions
    stepfunctions = boto3.client('stepfunctions')
    state_machine_arn = 'arn:aws:states:sa-east-1:595636811863:stateMachine:CustomerCheckinFlow'
    input_data = {
        'car_plate': car_plate
    }

    try:
        # Start the Step Functions execution
        stepfunctions.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(input_data)
        )

        print(f"Step Functions execution started for car plate: {car_plate}")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Step Functions execution started'})
        }

    except Exception as e:
        print('Error starting Step Functions execution:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }
        
        