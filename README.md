# EnfocaBrain

EnfocaBrain is a data collection system for electroencephalography (EEG) power spectrum, NeuroSky eSense (Attention and Meditation) with MindWave Mobile 2 and environmental data with CCS811 sensor.

## Requirements
- Raspberry Pi (e.g. 4 Model B)
- CCS811 Sensor
    - [Connect CCS811 Sensor to raspberry](https://learn.adafruit.com/adafruit-ccs811-air-quality-sensor/python-circuitpython#python-computer-wiring-2998333)
- Neurosky Mindwave Mobile 2
    - PyBluez and python-dotenv (to run Mindwave Script alone)
    - [python-mindwave-mobile](https://github.com/robintibor/python-mindwave-mobile) installed as a module
- ThingsBoard (optional)

## Installation
Clone the repo.
    
    git clone https://github.com/jmainhard/enfocabrain.git

Make a virtual environment to install Adafruit CircuitPython and read data from Raspberry I2C.

    python3 -m venv venv
    source venv/bin/activate

Install packages from requirements.

    pip install -r requirements.txt

Configure device token on `.env`. You can copy an example from `.env.example`

Also you can make sure that I2C is connected using `i2cdetect`

    i2cdetect -y 1

This will display a grid of addresses with the addresses of all connected I2C devices.
If your device is connected and powered on, you should see its address in this grid.
If you don't see your device's address, this indicates that there is a problem with the connection, power, or address of the device.


## Usage
To start enfocabrain automatically when the RP is booted write this to `/etc/rc.local` (replace the path with the actual one where you cloned the repo)

    sleep 10
    python3 /home/equipo1/enfocabrain/read_mindwave_mobile.py  > /home/equipo1/enfocabrain/mindwave.log 2>&1 &
    /home/equipo1/enfocabrain/.venv/bin/python3 /home/equipo1/enfocabrain/main.py > /home/equipo1/enfocabrain/main.log 2>&1 &

Alternatively you can run the python scripts manually.

For reading from the mindwave mobile 2, first turn it on and then run:

    python read_mindwave_mobile.py

For reading data from CCS811 start `ccs811.py` from the previosuly built virtual environment.

    (venv) python cccs811.py


## Contribute

Pull requests are accepted. For major changes, please open an issue first.

Please format your code with Python Black Formatter.