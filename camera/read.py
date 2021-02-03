import serial, sys
import numpy as np
import cv2

width  = 160
height = 120
arduino = None
framecount = 0
bindex, buffer = 0, []

def clip(x):
    if x > 255: return 255
    elif x < 0: return 0
    else:       return x

def YUVtoRGB(Y: int, U: int, V: int):
    B = 1.164*(Y - 16) + 2.018*(U - 128)
    G = 1.164*(Y - 16) - 0.813*(V - 128) - 0.391*(U - 128)
    R = 1.164*(Y - 16) + 1.596*(V - 128)

    return [R, G, B]

# def YUVtoRGB(Y: int, U: int, V: int):
#     C = lambda x: x - 16
#     D = lambda x: x - 128
#     E = lambda x: x - 128

#     R = clip((298 * C(Y) +              409 * E(V) + 128) >> 8)
#     G = clip((298 * C(Y) - 100 * D(U) - 208 * E(V) + 128) >> 8)
#     B = clip((298 * C(Y) + 516 * D(U)              + 128) >> 8)

#     return [R, G, B]

# def YUVtoRGB(Y: int, U: int, V: int):
#     C = lambda x: x - 128
#     D = lambda x: x - 128
#     E = lambda x: x - 128

#     R = Y + 1.4075 * C(V)
#     G = Y - 0.3455 * D(U) - (0.7169 * E(V))
#     B = Y + 1.7790 * D(U)

#     return [R, G, B]
def catchSignal(string):
    # Get three chars
    skipped = 3
    char0, char1, char2 = getData()[0], getData()[0], getData()[0]
    while True:
        # Get data based on the data in the buffer
        try:
            # print(char0.decode() + char1.decode() + char2.decode(), end="")
            if chr(char0) == string[0] and chr(char1) == string[1] and chr(char2) == string[2]:
                # if string == "ROW":
                    # print()
                    # print(skipped)
                return True
        except Exception:
            pass

        skipped += 1
        char0, char1, char2 = char1, char2, getData()[0]


def getData(amount: int = 1):
    # value = b''
    # while value == b'':
    # Always process incoming data first
    global buffer
    dataChunk, data = arduino.inWaiting(), []

    # If our buffer is empty or we request for more data than available, wait for data
    while len(buffer) < amount or dataChunk != 0:
        # Get data
        buffer += arduino.read(dataChunk)

        # Store data
        dataChunk = arduino.inWaiting()

    # print(buffer)

    # Access the correct byte based on the index
    while amount > 0:
        data.append(buffer.pop(0))
        amount -= 1

    return data


def readFrame(image):
    print("Waiting for frame...      ", end="\r", flush=True)
    catchSignal("FRM")
    global framecount
    log = f"Receiving frame {framecount}, "
    framecount += 1

    rowcount = 0

    for h in range(0, height):
        # Wait for the arduino to send a "ROW"
        catchSignal("ROW")
        rowcount += 1
        print(f"Row {rowcount}", end="\r", flush=True)
        # progress = int((h * 100) / height) + 1
        # print(log + f"{progress}%", end="\r", flush=True)


        for w in range(0, width, 2):
            # state, data = parseData(4)
            data = getData(4)
            print(f"[{data[0]:<3}, {data[1]:<3}, {data[2]:<3}, {data[3]:<3}], frame {framecount}", end="\r", flush=True)
            # print(f"data index {bindex}", end="\r", flush=True)
            # if state == "ROW":
            #     print("Arduino finished earlier than us")
            # if state == "FRM":
            #     print("A new frame should have been started")
            #     return

            image[h][w] =     YUVtoRGB(data[0], data[1], data[3])
            image[h][w + 1] = YUVtoRGB(data[2], data[1], data[3])
            # image[h][w] =     [data[0], data[1], data[3]]
            # image[h][w + 1] = [data[2], data[1], data[3]]

            # print(f"\rrow {h:<3} col {w:<3}", end="", flush=True)
    # print("Finished frame.")

    return image

try:
    image = np.zeros((height, width, 3), dtype=np.uint8)
    with serial.Serial('/dev/cu.usbserial-14120',
                       1000000,
                       bytesize=serial.EIGHTBITS,
                       timeout=0) as arduino:
    # with serial.Serial('/dev/cu.usbserial-A50285BI', 115200, timeout=1) as arduino:
        # while arduino.read() != b'Y': pass

        while True:
            image = readFrame(image)
            # img_out = cv2.cvtColor(image, cv2.COLOR_YUV2RGB_Y422)
            # cv2.imshow('image', cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR))
            # y,u,v = cv2.split(image)
            # cv2.imshow('Y', y)
            # cv2.imshow('U', u)
            # cv2.imshow('V', v)
            cv2.imshow('image', image)

            cv2.waitKey(1)

except KeyboardInterrupt:
    print("")