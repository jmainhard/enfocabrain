import time
from mindwavemobile.MindwaveDataPoints import RawDataPoint, EEGPowersDataPoint, AttentionDataPoint, MeditationDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
import requests
import textwrap
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

TOKEN_MINDWAVE = os.getenv("TOKEN")

# Configuración de la conexión ThingBoard
THINGBOARD_API_URL = f"http://iot.ceisufro.cl:8080/api/v1/{TOKEN_MINDWAVE}/telemetry"
HEADERS = {"Content-Type": "application/json"}

def send_to_thingsboard(data):
    # Realiza la solicitud HTTP POST a ThingBoard
    try:
        response = requests.post(THINGBOARD_API_URL, headers=HEADERS, json=data)

        # Verifica si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            print("Datos enviados exitosamente a ThingsBoard.")
        else:
            print("Error al enviar datos a ThingBoard. Código de estado:", response.status_code)

    except Exception as e:
        print("Error al realizar la solicitud HTTP:", e)

if __name__ == '__main__':
    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()
    
    if mindwaveDataPointReader.isConnected():
        while True:
            dataPoint = mindwaveDataPointReader.readNextDataPoint()

            # Procesa los datos del sensor MindWave Mobile
            if not dataPoint.__class__ is RawDataPoint:
                payload = {}
                if dataPoint.__class__ is EEGPowersDataPoint:
                    payload = {
                        "delta": dataPoint.delta,
                        "theta": dataPoint.theta,
                        "lowAlpha": dataPoint.lowAlpha,
                        "highAlpha": dataPoint.highAlpha,
                        "lowBeta": dataPoint.lowBeta,
                        "highBeta": dataPoint.highBeta,
                        "lowGamma": dataPoint.lowGamma,
                        "midGamma": dataPoint.midGamma
                    }
                if (dataPoint.__class__ is AttentionDataPoint):
                    payload = { "attentionValue": dataPoint.attentionValue }
                if (dataPoint.__class__ is MeditationDataPoint):
                    payload = { "meditationValue": dataPoint.meditationValue }
                send_to_thingsboard(payload)
                print(dataPoint)
                time.sleep(1)  # Ajusta el intervalo según tus necesidades
    else:
        print(textwrap.dedent("""\
            Exiting because the program could not connect
            to the Mindwave Mobile device.""").replace("\n", ""))

