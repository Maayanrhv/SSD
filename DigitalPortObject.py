import serial


# A class to enable access to the IMU portable device.
class DigitalPortObject:
    __serial_port_object = None

    def __init__(self,
                 port_number,
                 baud_rate,
                 parity,
                 num_of_bits,
                 stop_bit,
                 time_out_in_ms,
                 ):
        self.__serial_port_object = serial.Serial(port=port_number,
                                                  baudrate=baud_rate,
                                                  stopbits=stop_bit,
                                                  bytesize=num_of_bits,
                                                  timeout=time_out_in_ms)

    def Open(self):
        self.__serial_port_object.open()

    def SendMsg(self,
                msg: str):
        self.__serial_port_object.write(msg)

    def FlushIn(self):
        self.__serial_port_object.flushInput()

    def FlushOut(self):
        self.__serial_port_object.flushOutput()

    def FlushAll(self):
        self.__serial_port_object.flush()

    def IsBufferEmpty(self):
        return self.__serial_port_object.in_waiting == 0

    def ReadMsg(self,
                size):
        return self.__serial_port_object.read(size)

    def Close(self):
        self.__serial_port_object.close()
