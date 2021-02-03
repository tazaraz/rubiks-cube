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
