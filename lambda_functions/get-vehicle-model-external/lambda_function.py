import json
import requests
import time
import os

def lambda_handler(event, context):
    # Retrieve the plate number from the input event
    # plate_number = event.get('output', {}).get("plate")
    plate_number = event.get("plate")
    token = os.environ['APIPLACAS_ACCESS_TOKEN']
    
    if not plate_number:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Plate number not provided"})
        }

    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        # Make a request to the external API with the plate number
        api_url = f"https://wdapi2.com.br/consulta/{plate_number}/{token}"
        response = requests.get(api_url)
    
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
    
            # Extract relevant information
            modelo = data.get("MODELO", "")
            ano = data.get("ano", "")
    
            # Create the desired output format
            output_data = {
                "plate": plate_number,
                "model": f"{modelo} {ano}"
            }
            
            print("raw data: ", json.dumps(data))
    
            # Print the formatted output
            print("Formatted output:")
            print(json.dumps(output_data, indent=2))
    
            # You can now send the formatted output to the next step or perform additional processing
            # ...
    
            return {
                'response': {
                    "statusCode": 200
                },
                'output': output_data
            }
        else:
            # Retry the API call after a short delay
            retry_count += 1
            print(f"Retry {retry_count}/{max_retries}. Sleeping before retry...")
            time.sleep(2)  # You can adjust the sleep duration
    # If all retries fail, return an error response
    return {
        "statusCode": response.status_code,
        "body": json.dumps({"error": "Failed to retrieve data from external API after retries"})
    }