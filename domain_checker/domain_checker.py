import argparse
import time
import os


import requests
from twilio.rest import Client



# Set up cli domain argument
parser = argparse.ArgumentParser(description="Check domain for availability")
parser.add_argument("domain", type=str, help="Domain name to be checked")
args = parser.parse_args()

# request go daddy api for domain status
api_key = "3mM44UbCEiXEQ8_NgdG5MNha9ebzUruDSshwk"
api_secret = "8hNzKXp4Awg3ZjvEDZvKrf"
req_headers = {
    "Authorization": f"sso-key {api_key}:{api_secret}",
    "accept": "application/json"
    
}

# Twilio API credentials
account_sid = 'ACb752b99411f2e5562c3d6b1fd47a64f6' 
auth_token = '52e95d0e5605e45f196eb77de267a610' 
client = Client(account_sid, auth_token) 
to_whatsapp_number = "+19708001277"


def send_message(check_domain, to_whatsapp_number):
    domain_purchase_url = f"https://www.godaddy.com/domainsearch/find?domainToCheck={check_domain}"

    message = client.messages.create( 
        from_='whatsapp:+14155238886',        
        to=f'whatsapp:{to_whatsapp_number}', 
        body=f'Your domain {check_domain} is now available for purchase. {domain_purchase_url}' 
    )

    print(f"Message was sent to {to_whatsapp_number}, message_id is ")


# assemble the request url with the given domain 
def get_req_url(check_domain):
    return  f"https://api.ote-godaddy.com/v1/domains/available?domain={check_domain}"


def check_domain_availability(check_domain):
    print(f"Checking availabilty of domain {check_domain}")
    req_url = get_req_url(check_domain)
    req = requests.get(req_url, headers=req_headers)

    #if the requestwas unsuccessful, notify the user and stop the app
    if req.status_code != 200:
        print(f"Could not get availability state of domain {check_domain} - Status code {req.status_code}")
        return 

    # check if the domain is available
    response = req.json()
    if response["available"] == True:
        print(f"Domain {check_domain} is available for purchase, sending message to {to_whatsapp_number}")
        # send whatsapp message if domain is free
        send_message(check_domain, to_whatsapp_number)

    else:
        print(
            f"{time.strftime('%Y-%m-%d')} - Domain {check_domain} is not available for purchase."
        )

check_domain_availability(args.domain)
