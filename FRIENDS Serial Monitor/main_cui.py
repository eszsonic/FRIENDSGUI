from serialcompy import SerialCom


if __name__ == "__main__":
    com = SerialCom(baudrate=115200, timeout=0.1, writemode=True)
    com.start_serialcom()
