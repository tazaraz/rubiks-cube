import serial
import numpy as np
from PIL import Image

width  = 160
height = 120

# with serial.Serial('/dev/cu.usbserial-A50285BI', 2000000, timeout=1) as arduino:
with serial.Serial('/dev/cu.usbserial-A50285BI', 115200, timeout=1) as arduino:
    image = np.zeros((width,height,3), dtype=np.uint8 )
    while arduino.read() != b'Y': pass

    while True:
        for w in range(1, width):
            for h in range(1, height):
                data = []
                for i in range (3):
                    color = arduino.read()
                    while color == b'':
                        color = arduino.read()

                    data.append(int(arduino.read().hex(), 16))

                print(data, end="", flush=True)
                image[w][h] = data

        img = Image.fromarray(image)
        img.show()
