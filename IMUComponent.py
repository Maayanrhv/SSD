from DigitalPortObject import DigitalPortObject
import time
import base64


# A class to read the data that's streaming from the IMU device
class IMUComponent(DigitalPortObject):
    __LEGAL_PACKET_LENGTH: int = 31

    def __init__(self,
                 port_num: int,
                 baud_rate,
                 parity: str,
                 num_of_bits: int,
                 stop_bit: int,
                 time_out_in_ms: int):
        init = True
        self.gyroSF = 2000
        self.accSF = 25600
        self.timeout_rs485 = time_out_in_ms
        self.comm_port = port_num
        self.in_buffer_size = 4096
        self.out_buffer_size = 1024
        self.baud_rate = baud_rate
        self.parity = parity
        self.num_of_bits = num_of_bits
        self.stop_bit = stop_bit
        self.digital_port_audio = DigitalPortObject(port_number=port_num,
                                                    baud_rate=baud_rate,
                                                    parity=parity,
                                                    num_of_bits=num_of_bits,
                                                    stop_bit=stop_bit,
                                                    time_out_in_ms=time_out_in_ms)
        pass

    def __IsGoodPacket__(self,
                         packet: str):
        if len(packet) != self.__LEGAL_PACKET_LENGTH:
            return False

        if packet[0:3] != '$15'.encode():
            return False

        if packet[-1] != ord('#'):
            return False

        'The data is from byte 3 to the end - 1'
        packet_data = packet[3:-2:1]

        check_sum = sum([c for c in packet_data])
        if check_sum > 255:
            check_sum = check_sum % 256

        if check_sum != packet[-2]:
            return False

        return True

    def __ParsePacket__(self,
                        packet: str):

        str_num = [0, 0, 0, 0]
        res = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        res_index = 0
        for i in range(3, self.__LEGAL_PACKET_LENGTH - 2, 3):
            str_num[0] = hex(packet[i])[2::1]
            str_num[1] = hex(packet[i + 1])[2::1]
            str_num[2] = hex(packet[i + 2])[2::1]
            str_num[3] = '00'
            if len(str_num[1]) == 1:
                str_num[1] = '0' + str_num[1]
            if len(str_num[2]) == 1:
                str_num[1] = '0' + str_num[2]

            num_str = str_num[0] + str_num[1] + str_num[2] + str_num[3]
            res[res_index] = self.__IEEE754ToDecimal__(num_str)
            '''todo:temperature read'''
            '''if i == 8:
                a = num_str[1:3:1]'''
            res_index = res_index + 1

        return res

    def __IEEE754ToDecimal__(self,
                             ieee: str):
        ieee_bin = ''

        for i in range(0, len(ieee), 1):
            s = ieee[i]
            ieee_bin = ieee_bin + self.__HexToBinary__(s.upper())

        sign_str = ieee_bin[0]
        exp_str = ieee_bin[1:9:1]
        mantis_str = ieee_bin[9:32:1]
        exp = 0
        mantis = 0

        sign = 1
        if sign_str == '1':
            sign = -1

        for i in range(0, len(exp_str) - 1, 1):
            if exp_str[i] == '1':
                exp = exp + 2 ** (len(exp_str) - (i + 1))

        for i in range(0, len(mantis_str) - 1, 1):
            if mantis_str[i] == '1':
                mantis = mantis + 2 ** (-(i + 1))

        p = exp - 127

        return sign * (1 + mantis) * (2 ** p)

    def __HexToBinary__(self, hex: str):
        switcher = {
            '0': '0000',
            '1': '0001',
            '2': '0010',
            '3': '0011,',
            '4': '0100',
            '5': '0101',
            '6': '0110',
            '7': '0111',
            '8': '1000',
            '9': '1001',
            'A': '1010',
            'B': '1011',
            'C': '1100',
            'D': '1101',
            'E': '1110',
            'F': '1111',
        }

        return switcher.get(hex, "nothing")

    def __FindPacket__(self,
                       msg: str,
                       curret_packet: str):
        packet = ['', '']

        if len(curret_packet) == self.__LEGAL_PACKET_LENGTH:
            packet[0] = curret_packet
            packet[1] = msg
            return packet
        elif len(curret_packet) > self.__LEGAL_PACKET_LENGTH:
            packet[0] = curret_packet[0:self.__LEGAL_PACKET_LENGTH:1]
            packet[1] = msg
            return packet

        packet[0] = ''
        packet[1] = ''

        if len(curret_packet) > 0:
            packet[0] = curret_packet + msg[0:min(len(msg), self.__LEGAL_PACKET_LENGTH - len(curret_packet)):1]
            packet[1] = msg[self.__LEGAL_PACKET_LENGTH - len(curret_packet)::1]
            return packet

        for i in range(0, len(msg) - 1, 1):
            if msg[i] == ord('$'):
                packet[0] = msg[i:i + min(self.__LEGAL_PACKET_LENGTH, len(msg) - 1):1]
                packet[1] = msg[i:i + len(packet[0]):1]
                return packet

        return packet

    def ReadFromRS485(self,
                      num_of_packets: int):
        t1 = int(round(time.time() * 1000))
        t2 = 0
        num_of_zero_arrays = 0
        self.digital_port_audio.FlushAll()
        all_res = [0] * 10
        msg = self.__ReadMsg__()
        single_packet = ['', '']
        num_of_reads = 0
        single_packet[0] = ''
        finish_reading_packets = False
        total_reads = 0

        while (not finish_reading_packets) and (
                num_of_reads != num_of_packets and len(msg) != 0 and (t2 - t1) < num_of_packets * 2):
            '''finish the current msg'''
            while (not finish_reading_packets) and (len(msg) != 0 and (t2 - t1) < num_of_packets * 2):
                single_packet = self.__FindPacket__(msg=msg,
                                                    curret_packet=single_packet[0])
                msg = single_packet[1]
                if self.__IsGoodPacket__(single_packet[0]):
                    res = self.__ParsePacket__(single_packet[0])

                    if self.__IsAllArrayZero__(res):
                        num_of_zero_arrays = num_of_zero_arrays + 1
                    else:
                        for i in range(0, 8, 1):
                            all_res[i] = all_res[i] + res[i]

                        num_of_reads = num_of_reads + 1
                        if num_of_reads == num_of_packets:
                            finish_reading_packets = True
                t2 = int(round(time.time() * 1000))
            msg = self.__ReadMsg__()

        if finish_reading_packets:
            if num_of_reads > 0:
                for i in range(0, 8, 1):
                    all_res[i] = all_res[i] / num_of_reads

        all_res[9] = num_of_reads
        total_reads = total_reads + num_of_reads
        '''DoEvents'''
        return all_res

    def __IsAllArrayZero__(self,
                           arr):
        for i in range(0, len(arr) - 1, 1):
            if arr[i] == 0:
                return True
        return False

    def __ReadMsg__(self):
        t1 = int(round(time.time() * 1000))
        t2 = 0
        readMsg = ''

        while ((t2 - t1) <= self.timeout_rs485) and self.digital_port_audio.IsBufferEmpty():
            t2 = int(round(time.time() * 1000))
        if not self.digital_port_audio.IsBufferEmpty():
            readMsg = self.digital_port_audio.ReadMsg(100)
        else:
            readMsg = ''
        return readMsg

    def GetPacket(self):
        gyro_packet = self.ReadFromRS485(10)
        gy = gyro_packet[0] / self.gyroSF
        gz = gyro_packet[1] / self.gyroSF
        gx = gyro_packet[2] / self.gyroSF
        ay = gyro_packet[4] / self.accSF
        az = gyro_packet[5] / self.accSF
        ax = gyro_packet[6] / self.accSF

        return [gy, gz, gx, ay, az, ax]

    def MakeOperational(self):
        self.digital_port_audio.SendMsg('$00051#'.encode())
