"""
192.168.10.42
"""

import socket
import logging
import sys
#from eos.Raspi import adc_utils
import adc_utils
import time

try:
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    import board
    import busio
except Exception:
    pass

logging.basicConfig(level=logging.INFO)

HEADERSIZE = 10


def main(mode=None, *args, **kwargs):
    """
    Am I client or Server?
    If running the script on the Raspberry PI, run with -s. Else run with -c-
    """
    
    print(mode)
    if mode:
        if mode == "client" or mode == "-c":
            return client("-c")
        elif mode == "server" or mode == "-s":
            return server()
        else:
            logging.debug("Invalid parameter %s. Run with -c or -s" % mode)
    else:
        try:
            arg = sys.argv[1]
        except Exception:
            logging.debug(
                "Invalid parameter %s. Run with -c (client) or -s (server) instead"
                % sys.argv[1]
            )
            sys.exit(1)
        if arg == "client" or arg == "-c":
            return client()
        elif arg == "server" or arg == "-s":
            return server()
        else:
            logging.debug(
                "Invalid parameter %s. Run with -c (client) or -s (server) instead"
                % sys.argv[1]
            )
            sys.exit(1)


def client(*args, **kwargs):
    """
    Measurement PC. Connect to Raspberry PI server and query data taking.
    Data taking is triggered by sending anything to the Raspberry Pi (including empty
    string). Raspberry PI returns channel name, adc value and converted voltage.
    If no data received, terminates after timeout.

    TODO: Query for specific channel, set gain, set mode, set single ended / differential,
    timeout handling.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("192.168.10.42", 50000))
    sock.settimeout(20)

    logging.debug("Query data taking")
    adc_utils.send(tcp_socket=sock, HEADERSIZE=10, data="Query data taking")
    time.sleep(0.1)
    data = adc_utils.receive(tcp_socket=sock, HEADERSIZE=10)
    print(data)
    time.sleep(0.1)
    if len(data) >= 0:
        logging.debug("Received data")
        logging.debug(data)
        return data
        sock.close()


def server(*args, **kwargs):
    """
    Raspberry pi with IP address 192.168.10.42 and ADS115 ADC connected.
    Possible addresses for ADC instances are 0x48, 0x49, 0x4a and 0x4b depending
    on ADDR wiring. For 5V VDD set gain to 2 / 3, for 3.3V VDD set gain to 1.
    Set gain to 2 if measured voltage is guaranteed to be below 2 V.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 50000))
    sock.listen(1)
    # sock.settimeout(120)

    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the ADC object using the I2C bus
    ads = ADS.ADS1115(i2c, address=0x48)
    bds = ADS.ADS1115(i2c, address=0x49)
    cds = ADS.ADS1115(i2c, address=0x4A)

    ads.gain, bds.gain, cds.gain = 1, 1, 1

    a = [
        AnalogIn(ads, ADS.P0),
        AnalogIn(ads, ADS.P1),
        AnalogIn(ads, ADS.P2),
        AnalogIn(ads, ADS.P3),
    ]
    b = [
        AnalogIn(bds, ADS.P0),
        AnalogIn(bds, ADS.P1),
        AnalogIn(bds, ADS.P2),
        AnalogIn(bds, ADS.P3),
    ]
    c = [
        AnalogIn(cds, ADS.P0),
        AnalogIn(cds, ADS.P1),
        AnalogIn(cds, ADS.P2),
        AnalogIn(cds, ADS.P3),
    ]

    def measurement(channel):
        value, voltage = [], []
        for i in range(1):  # taking average of 10 measurements
            value.append(channel.value), voltage.append(channel.voltage)
        return [value, voltage]

    time.sleep(0.2)

    while True:
        clientsocket, address = sock.accept()
        print(f"Connection from {address} has been established.")
        timeout = time.time() + 2
        while time.time() < timeout:
            query = adc_utils.query(tcp_socket=clientsocket, HEADERSIZE=HEADERSIZE)
            if query:
                logging.info("Readout queried")
                meas = [
                    measurement(a[0]),
                    measurement(a[1]),
                    measurement(a[2]),
                    measurement(a[3]),
                    measurement(b[0]),
                    measurement(b[1]),
                    measurement(b[2]),
                    measurement(b[3]),
                    measurement(c[0]),
                    measurement(c[1]),
                    measurement(c[2]),
                    measurement(c[3]),
                ]
                adc_utils.send(
                    tcp_socket=clientsocket, HEADERSIZE=HEADERSIZE, data=meas
                )
                logging.info("Data transmitted.")
                timeout = time.time() + 0.2
            if not query:
                if time.time() > timeout:
                    clientsocket.close()
                    break


if __name__ == "__main__":
    print(main("-c"))
