import json
import requests
import os

def lambda_handler(event, context):
    # Extract car plate value from the input
    car_plate = event.get('output', {}).get('plate', None)
    
    # Replace this with your actual GraphQL endpoint
    graphql_endpoint = "https://api.pipefy.com/graphql"

    # Object IDs to search for
    object_ids = [
        {"id": "310877028", "name": "Ordem de serviço"},
        {"id": "310877029", "name": "Serviço em andamento"},
        {"id": "310877030", "name": "Serviço pausado"}
    ]

    # Set up the HTTP headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['PIPEFY_ACCESS_TOKEN']}"
        # Add any other headers if required
    }
    
    # Placeholder for the result
    result = {}
    
    # Initiate variable for result
    has_active_service = False

    # Perform GraphQL queries for each object ID
    for obj in object_ids:
        status_id = obj["id"]
        graphql_query = f'{{ phase(id: {status_id}) {{ cards(search: {{ title: "{car_plate}" }}) {{ edges {{ node {{ id title }} }} }} }} }}'
        print(graphql_query)
        # Make the GraphQL query
        response = requests.post(graphql_endpoint, json={"query": graphql_query}, headers = headers)

        # Check if the query was successful (status code 200)
        print('query: ',response.status_code)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Check if the 'edges' array is not empty
            if data.get("data", {}).get("phase", {}).get("cards", {}).get("edges", []):
                has_active_service = True
                break
        else:
            # Handle the case when the GraphQL query fails
            has_active_service = "Query failed"
            break

    # Prepare the response in the specified format
    response = {'statusCode': 200}
    output = {'has-active-service': has_active_service, 'plate': car_plate}

    return {
        'response': response,
        'output': output
    }