#Code to use the Kandy api with raspberry pi
#Earl Helms - earl@earlhelms.com - May 2016 - created for the Kandy Hackathon
#
#The code will send a text message when a button is pressed on the raspberry pi
#
#The code has been changed slightly from the version used in the hackathon, specifically
#the old hard coded account information and phone number was changed. The currently shown account information
#is incorrect and will not work.  The comments explain how to set it up correctly.
#
#This demo works with a button on the raspberry pi.  The button is connected to the GPIO 18 pin and a ground.  pinouts for the pi can be found online.
#if you don't have a button, you can simulate a button press by manually pressing two wires together (making a circuit between GPIO 18 and the ground)
#
#Best of luck to you

import requests
import json
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
Emergency = 1
NoEmergency = 2
CurrentButton = 3
OldButton = 4
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    time.sleep(0.2)
    input_state = GPIO.input(18)
    if input_state != False and OldButton != 4:
        CurrentButton = NoEmergency
    if input_state == False and OldButton != 4:
        CurrentButton = Emergency
    if CurrentButton == Emergency and OldButton != Emergency:
        print('Emergency')

	#!!!!!!!!!!!!!! 
	# For the next line Create account at developer.kandy.io you will need the key, domain_api_secret and user_id
	# !!!!!!!!!!!!!
        r = requests.get("https://api.kandy.io/v1.2/domains/users/accesstokens?key=DAK570a9ff045c444349d087a2e38232bc8&domain_api_secret=DAS0ac8b197ce304ce49dda4f2bbe26d2eb&user_id=carebutton")

        data = r.json()
        UserToken = data['result']['user_access_token']
        print(UserToken)

        print("part2.......")
        Url = "https://api.kandy.io/v1.2/users/devices?key=" + UserToken
        r = requests.get(Url)

        data = r.json()
        DeviceId = data['result']['devices'][0]['id']
        #print(data)
        print("--------")
        print(DeviceId)
        print("part3.......")
        Url = "https://api.kandy.io/v1.2/devices/smss?device_id=" + DeviceId + "&key=" + UserToken

	#!!!!!!!!!!!!!! 
	# For the next line - change the destination phone number
	# !!!!!!!!!!!!!
        DataString = {
            "message": {
                "source": "14075551212",
                "destination": "14075551212",
                "message": {
                    "text": "Grandma needs help - Box button pressed"
                }
            }
        }

        Headers = {
            "Content-Type":"application/json"
        }

        r = requests.post(Url, headers=Headers, data=json.dumps(DataString))

        #status = r[u'body'])[u'user_access_token']
        data = r.json()
        #DeviceId = data['result']['devices'][0]['id']
        #print(data)
        print("--------")
        print(data)
        print("--------")
        print(Url)

    if CurrentButton == NoEmergency and OldButton != NoEmergency:
        print('NoEmergency')
    OldButton = CurrentButton
