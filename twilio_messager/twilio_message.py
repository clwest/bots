from twilio.rest import Client 

account_sid = 'ACb752b99411f2e5562c3d6b1fd47a64f6' 
auth_token = '52e95d0e5605e45f196eb77de267a610' 
client = Client(account_sid, auth_token) 

message = client.messages.create( 
        from_='whatsapp:+14155238886',  
        body='Your Twilio code is 1238432',      
        to='whatsapp:+19708001277' 
    ) 

print(message.sid)