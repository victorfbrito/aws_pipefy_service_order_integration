import requests
import json
import os

def lambda_handler(event, context):
    # Extract car plate value from the input
    car_plate = event.get('output', {}).get('plate', None)

    # Check if the car plate parameter is missing
    if car_plate is None:
        error_message = "Missing 'plate' parameter in the input."
        response = {
            'statusCode': 400,  # HTTP 400 Bad Request
            'body': json.dumps({'error': error_message})
        }
        return response

    # Make the GraphQL query using the car_plate value
    graphql_result = make_graphql_query(car_plate)


    return graphql_result

def get_custom_property(prop_list, prop_label):
    # Use a list comprehension to extract the "value" for "name": "Customer_ID"
    prop_value = next((field["value"] for field in prop_list if field.get("name") == prop_label), None)
    return prop_value

def make_graphql_query(car_plate):
    # Define the GraphQL query
    graphql_query = """
    {
      table_records(search: {title: "%s"}, table_id: "dqQmoS8u") {
        edges {
          node {
            id
            title
            done
			record_fields {
				name
				value
			}
            table {
              id
            }
            created_at
            created_by {
              id
            }
          }
        }
      }
    }
    """ % car_plate

    # Define the GraphQL endpoint URL
    graphql_endpoint = "https://api.pipefy.com/graphql"

    # Set up the HTTP headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['PIPEFY_ACCESS_TOKEN']}"
        # Add any other headers if required
    }

    # Make the HTTP POST request with the GraphQL query
    pipe_response = requests.post(graphql_endpoint, json={"query": graphql_query}, headers=headers)

    

    # Check if the request was successful (status code 200)
    if pipe_response.status_code == 200:
        # Parse and return the JSON response
        # print(response.json())
        if len(pipe_response.json()['data']['table_records']['edges']) > 0:
            output = {
                'registered': True,
                'plate': get_custom_property(pipe_response.json()['data']['table_records']['edges'][0]['node']['record_fields'], 'Plate'),
                'model': get_custom_property(pipe_response.json()['data']['table_records']['edges'][0]['node']['record_fields'], 'Vehicle_model'),
                'customer_id': get_custom_property(pipe_response.json()['data']['table_records']['edges'][0]['node']['record_fields'], 'Customer_ID'),
                'service_history': get_custom_property(pipe_response.json()['data']['table_records']['edges'][0]['node']['record_fields'], 'service_history'),
            }
            status_code = 200
        else:
            output = {
                'plate': car_plate,
                'registered': False
            }
            
        return {
            'response': {
                'statusCode': 200
            },
            'output': output
        }
    else:
        # Print the error message if the request was not successful
        print(f"GraphQL request failed with status code {response.status_code}: {response.text}")
        return None
