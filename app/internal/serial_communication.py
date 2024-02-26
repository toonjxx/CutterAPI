import serial
from typing import Optional

class CT150_Serial:
    def __init__(self, port: str = '/dev/ttyUSB0', baudrate: int = 9600, timeout: int = 1):
        
        # Set the default values for the serial port
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser: Optional[serial.Serial] = None


    def open_device(self) -> bool:
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Device {self.port} opened successfully")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def close_device(self) -> bool:
        try:
            self.ser.close()
            print(f"Device {self.port} closed successfully")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


    def read_register(self, register_code: str) -> bool:
        write_command = b'\x04\x31\x31' + register_code.encode() + b'\x05'
        try:
            self.ser.write(write_command)
            # read the data
            frame = self.ser.read_until(expected=b'\x04')
            print(frame)

        except Exception as e:
            print(f"Error: {e}")
            return False

    
    def write_frame_convert(self, command: str) -> bytes:
        return self.write_start_of_frame + command.encode() + self.write_end_of_frame
    
    def read_frame_convert(self, frame: bytes) -> str:
        frame = frame.split(self.read_start_of_frame)[1]
        frame = frame.split(self.read_end_of_frame)[0]
        return frame.decode()

    def write_device(self, command: str) -> bool:
        command = self.write_frame_convert(command)
        try:
            self.ser.write(command.encode())
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def read_device(self) -> str:
        try:
            data = self.ser.read_until(self.read_end_of_frame)
            return self.read_frame_convert(data)
            
        except Exception as e:
            print(f"Error: {e}")
            return "Error reading from device"
    

    
