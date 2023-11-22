import json
import requests
from datetime import datetime
import os

def lambda_handler(event, context):
    try:
        # Extract data from the event
        plate = event.get('output', {}).get("plate", "")
        model = event.get('output', {}).get("model", "")
        customer_id = event.get('output', {}).get("customer_id", "")
        service_history = event.get('output', {}).get("service_history", "")
        
        # Get the current date in DD/MM/YYYY format
        current_date = datetime.now().strftime("%d/%m/%Y")
        # current_date = '11/11/2023'
        # print('date: ', current_date)

        # GraphQL mutation
        mutation = '''
            mutation {{
                createCard(
                    input: {{
                        pipe_id: "301640798"
                        fields_attributes: [
                            {{ field_id: "placa_1", field_value: "{}" }}
                            {{ field_id: "modelo", field_value: "{}" }}
                            {{ field_id: "data", field_value: "{}" }}
                            {{ field_id: "cliente", field_value: "{}" }}
                        ]
                    }}
                ) {{
                    clientMutationId
                    card {{
                        createdAt
                        id
                    }}
                }}
            }}
        '''.format(plate, model, current_date, customer_id)


        print(' plate: ', plate, ' model: ', model, ' current_date: ', current_date, ' customer_id: ', customer_id, ' history: ', service_history)
        # Your GraphQL endpoint URL
        graphql_endpoint = "https://api.pipefy.com/graphql"

        # Make the GraphQL mutation request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['PIPEFY_ACCESS_TOKEN']}"
            # Add any other headers if required
        }
        graphql_response = requests.post(graphql_endpoint, json={'query': mutation}, headers=headers)

        # Log the GraphQL response
        print('GraphQL Response:', graphql_response.json())

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'GraphQL mutation successful'})
        }
    except Exception as e:
        print('Error:', str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }

# Example usage:
# event = {'plate': 'PLATE_NUMBER', 'model': 'MODEL_DATA'}
# context = {}
# lambda_handler(event, context)
