import IMUComponent

imu_component = IMUComponent.IMUComponent(port_num='COM4',
                                          baud_rate=921600,
                                          parity='None',
                                          num_of_bits=8,
                                          stop_bit=1,
                                          time_out_in_ms=100)

imu_component.MakeOperational()

while True:
    '''time.sleep(1)'''
    vec = imu_component.GetPacket()
    '''print('Get Packet')'''
    print(vec[0])
