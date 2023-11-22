import json
import requests
import os

def lambda_handler(event, context):
    try:

        # Extract relevant information
        plate_number = event.get('output', {}).get("plate", {})
        model_data = event.get('output', {}).get("model", {})
        
        print('data: ', plate_number + model_data)
        # GraphQL mutation
        mutation = '''
            mutation {
                createTableRecord(
                    input: {
                        table_id: "dqQmoS8u"
                        fields_attributes: [
                            { field_id: "vehicle_model", field_value: "%s" }
                            { field_id: "plate", field_value: "%s" }
                        ]
                    }
                ) {
                    clientMutationId
                    table_record {
                        created_at
                        done
                        id
                    }
                }
            }
        ''' % (model_data, plate_number)
        
        # Your GraphQL endpoint URL
        graphql_endpoint = "https://api.pipefy.com/graphql"
        
        # Make the GraphQL mutation request
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {os.environ['PIPEFY_ACCESS_TOKEN']}"
        }
        graphql_response = requests.post(graphql_endpoint, json={'query': mutation}, headers=headers)
        
        # Log the GraphQL response
        print('GraphQL Response:', graphql_response.json())
        
        return {
            'response': { 
                'statusCode': 200,
                'body': json.dumps({'message': 'GraphQL mutation successful'})
            },
            'output': {
                "plate": plate_number,
                "model": model_data
            }
        }
    except Exception as e:
        print('Error:', str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }

