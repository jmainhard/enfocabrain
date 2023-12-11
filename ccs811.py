import time
import busio
import adafruit_ccs811
import board
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

TOKEN_CCS811 = os.getenv("TOKEN")

# Configure ThingsBoard connection
THINGSBOARD_API_URL = f"http://iot.ceisufro.cl:8080/api/v1/{TOKEN_CCS811}/telemetry"
HEADERS = {"Content-Type": "application/json"}

# Configure CCS811 sensor
i2c = busio.I2C(board.SCL, board.SDA)
ccs = adafruit_ccs811.CCS811(i2c)

while not ccs.data_ready:
    pass

while True:
    co2_ppm = ccs.eco2
    tvoc_ppb = ccs.tvoc

    print("CO2: {} ppm, TVOC: {} ppb".format(co2_ppm, tvoc_ppb))

    # Build the JSON payload to send to ThingsBoard
    payload = {"co2": co2_ppm, "tvoc": tvoc_ppb}

    # Make the HTTP POST request to ThingsBoard
    try:
        response = requests.post(THINGSBOARD_API_URL, headers=HEADERS, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Data successfully sent to ThingsBoard.")
        else:
            print(
                "Error sending data to ThingsBoard. Status code: ",
                response.status_code,
            )

    except Exception as e:
        print("Error making the HTTP request:", e)

    time.sleep(1)
