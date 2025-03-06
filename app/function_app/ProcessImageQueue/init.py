import logging
import json
import azure.functions as func
import requests

def main(msg: func.QueueMessage) -> None:
    logging.info('Queue trigger function processed a message.')
    
    try:
        # Decode and parse the JSON message.
        message_body = msg.get_body().decode('utf-8')
        logging.info(f'Message content: {message_body}')
        message = json.loads(message_body)
        
        # Expecting the message to contain a "blob_url" field.
        blob_url = message.get("blob_url")
        if not blob_url:
            logging.error("No blob_url found in the message.")
            return
        
        # Prepare the payload to call your Python API.
        api_payload = {"image_url": blob_url}
        # Replace with your actual Python API endpoint URL.
        python_api_endpoint = "http://your-python-api-endpoint/image/process"

        # Call the Python API.
        response = requests.post(python_api_endpoint, json=api_payload)
        response.raise_for_status()  # Raise an exception for HTTP errors.
        logging.info(f"Python API processed the image successfully. Response: {response.text}")
    
    except Exception as e:
        logging.error(f"Error processing the queue message: {str(e)}")
        # Depending on your needs, you might let the error bubble up to trigger a retry.
