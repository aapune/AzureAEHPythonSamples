import time
import urllib.parse
import hmac
import hashlib
import base64
import requests

def generate_sas_token(namespace, eventhub, sas_key_name, sas_key):
    uri = f"https://{namespace}.servicebus.windows.net/{eventhub}"
    encoded_uri = urllib.parse.quote_plus(uri)
    expiry = int(time.time() + 3600)  # Token valid for 1 hour
    string_to_sign = f"{encoded_uri}\n{expiry}"
    signature = base64.b64encode(hmac.new(sas_key.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
    sas_token = f"SharedAccessSignature sr={encoded_uri}&sig={urllib.parse.quote_plus(signature)}&se={expiry}&skn={sas_key_name}"
    return sas_token

# Replace with your actual values
namespace = 'aniehtest'
eventhub = 'testeh'
sas_key_name = 'testpolicy'


# Generate SAS token
sas_token = generate_sas_token(namespace, eventhub, sas_key_name, "sas")

# Prepare the URL and headers for the request
url = f"https://{namespace}.servicebus.windows.net/{eventhub}/messages"
headers = {
    'Authorization': sas_token,
    'Content-Type': 'application/json'
}

# The event data you want to send
event_data = {
    "message": "Hello, !"
}

# Send the event to the Event Hub
response = requests.post(url, json=event_data, headers=headers)

if response.status_code == 201:
    print("Event sent successfully")
else:
    print(f"Failed to send event: {response.status_code}, {response.text}")
