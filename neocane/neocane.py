import smbus
import time


INPUT  = 'in'
OUTPUT = 'out'
HIGH   = '1'
LOW    = '0'



class TemperatureBrick(object):

    LM75_ADDRESS          = 0x48
    LM75_TEMP_REGISTER    = 0
    LM75_CONF_REGISTER    = 1
    LM75_THYST_REGISTER   = 2
    LM75_TOS_REGISTER     = 3
    LM75_CONF_SHUTDOWN    = 0
    LM75_CONF_OS_COMP_INT = 1
    LM75_CONF_OS_POL      = 2
    LM75_CONF_OS_F_QUE    = 3

    def __init__(self, mode=LM75_CONF_OS_COMP_INT, address=LM75_ADDRESS, busnum=1):
        self._mode = mode
        self._address = address
        self._bus = smbus.SMBus(busnum)

    def regdata2float (self, regdata):
        return (regdata / 32.0) / 8.0

    def toFah(self, temp):
        return (temp * (9.0/5.0)) + 32.0

    def getTemperature(self):
        raw = self._bus.read_word_data(self._address, self.LM75_TEMP_REGISTER) & 0xFFFF
        raw = ((raw << 8) & 0xFF00) + (raw >> 8)
        return self.regdata2float(raw)




class LightBrick(object):

    I2C_ADDR = 0x29

    def __init__(self, address=I2C_ADDR, busnum=1):
        self._address = address
        self._bus = smbus.SMBus(busnum)

        self._bus.write_byte_data(self._address, 0x00 | 0x80, 0x03)
        self._bus.write_byte_data(self._address, 0x01 | 0x80, 0x02)

        time.sleep(0.5)


    def getFullSpectrum(self):
        data = self._bus.read_i2c_block_data(self._address, 0x0C | 0x80, 2)
        data1 = self._bus.read_i2c_block_data(self._address, 0x0E | 0x80, 2)

        # Convert the data
        ch0 = data[1] * 256 + data[0]
        ch1 = data1[1] * 256 + data1[0]

        return ch0


    def getInfraredSpectrum(self):
        data = self._bus.read_i2c_block_data(self._address, 0x0C | 0x80, 2)
        data1 = self._bus.read_i2c_block_data(self._address, 0x0E | 0x80, 2)

        # Convert the data
        ch0 = data[1] * 256 + data[0]
        ch1 = data1[1] * 256 + data1[0]

        return ch1


    def getVisibleSpectrum(self):
        data = self._bus.read_i2c_block_data(self._address, 0x0C | 0x80, 2)
        data1 = self._bus.read_i2c_block_data(self._address, 0x0E | 0x80, 2)

        # Convert the data
        ch0 = data[1] * 256 + data[0]
        ch1 = data1[1] * 256 + data1[0]

        return ch0 - ch1

    def getLight(self):
        return getVisibleSpectrum()



class BarometricBrick(object):

    BAROMETRIC_BRIC_I2C_ADDRESS = 0x60

    def __init__(self, address=BAROMETRIC_BRIC_I2C_ADDRESS, busnum=1):
        self._address = address
        self._bus = smbus.SMBus(busnum)


    def getAltitude(self):
        self._bus.write_byte_data(self._address, 0x26, 0xB9)
        self._bus.write_byte_data(self._address, 0x13, 0x07)
        self._bus.write_byte_data(self._address, 0x26, 0xB9)

        time.sleep(0.1)

        data = self._bus.read_i2c_block_data(self._address, 0x00, 6)

        # Convert the data to 20-bits
        tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        altitude = tHeight / 16.0

        return altitude


    def getTemperature(self):
        self._bus.write_byte_data(self._address, 0x26, 0xB9)
        self._bus.write_byte_data(self._address, 0x13, 0x07)
        self._bus.write_byte_data(self._address, 0x26, 0xB9)

        time.sleep(0.1)

        data = self._bus.read_i2c_block_data(self._address, 0x00, 6)

        # Convert the data to 20-bits
        temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
        cTemp = temp / 16.0
        #fTemp = cTemp * 1.8 + 32

        return cTemp


    def getPressure(self):
        self._bus.write_byte_data(self._address, 0x26, 0x39)

        time.sleep(0.1)

        data = self._bus.read_i2c_block_data(self._address, 0x00, 4)

        # Convert the data to 20-bits
        pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        pressure = (pres / 4.0) / 1000

        return pressure


class Accelerometer(object):

    def __init__(self):
        self.base_path = None    
    

class Magnetometer(object):

    def __init__(self):
        self.base_path = None  


class Gyroscope(object):

    def __init__(self):
        self.base_path = None  


class Gpio(object):

    INPUT  = 'in'
    OUTPUT = 'out'
    HIGH   = '1'
    LOW    = '0'

    gpios = [ "178", "179", "104", "143", "142", "141", "140", "149", #J4in
              "105", "148", "146", "147", "100", "102", #J6 in
              "106", "107", "180", "181", "172", "173", "182", "124", #J4 out
               "25",  "22",  "14",  "15",  "16",  "17",  "18",  "19",  "20",  "21",
              "203", "202", "177", "176", "175", "174",
              "119", "124", "127", "116",   "7",   "6",   "5",   "4"]

    gpios_J4_in  = { '0'  : 178, '1'  : 179, '2'  : 104, '3'  : 143, '4'  : 142, '5'  : 141, '6'  : 140, '7'  : 149 }
    gpios_J4_out = { '16' : 106, '17' : 107, '18' : 180, '19' : 181, '20' : 172, '21' : 173, '22' : 182, '23' : 124 }
    gpios_J6_in  = { '8'  : 105, '9'  : 148, '10' : 146, '11' : 147, '12' : 100, '13' : 102 }
    gpios_J6_out = { '24' : 25,  '25' : 22,  '26' : 14,  '27' : 15,  '28' : 16,  '29' : 17,  '30' : 18,  '31' : 19, '32' : 20, '33' : 21 }
    gpios_J5_out = { '34' : 203, '35' : 202, '36' : 177, '37' : 176, '38' : 175, '39' : 174 }
    gpios_J7_out = { '40' : 119, '41' : 124, '42' : 127, '43' : 116, '44' : 7,   '45' : 6,   '46' : 5,   '47' : 4 }

    _gpios_dict = dict()
    _gpios_dict.update(gpios_J4_in)
    _gpios_dict.update(gpios_J4_out)
    _gpios_dict.update(gpios_J6_in)
    _gpios_dict.update(gpios_J6_out)
    _gpios_dict.update(gpios_J5_out)
    _gpios_dict.update(gpios_J7_out)

    DEFAULT_BASE_PATH = "/sys/class/gpio"

    def __init__(self):
        self.base_path = self.DEFAULT_BASE_PATH
        self.gpios_dict = self._gpios_dict

    def export_gpio(self, pin):
        gpio = str( self.gpios_dict[str(pin)] )
        try:
          with open( self.base_path + "/export" , "w") as re:
            re.write( str(gpio) )
        except Exception as e:
          print( e )
        return 0


    def unexport_gpio(self, pin):
        gpio = str(self.gpios_dict[ str(pin) ])
        try:
          with open( self.base_path + "/unexport" , "w") as re:
            re.write( str(gpio) )
        except Exception as e:
          print( e )
        return 0


    def export_all_gpios(self):
        for pin in self.gpios_dict.keys():
            self.export_gpio( pin )


    def unexport_all_gpios(self):
        for pin in self.gpios_dict.keys():
            self.unexport_gpio( pin )


    def pinMode(self, pin, direction):
      gpio = str(self.gpios_dict[ str(pin) ])
      try:
        with open(self.base_path + "/gpio" + gpio + "/direction", "w") as re:
          re.write( str(direction) )
      except Exception as e:
        print( e )

      return 0


    def digitalWrite(self, pin, value):
      gpio = str(self.gpios_dict[ str(pin) ])
      try:
        with open(self.base_path + "/gpio" + gpio + "/value", "w") as re:
          re.write( str(value) )
      except Exception as e:
        print( e )

      return 0


    def digitalRead(self, pin):
      value = None
      try:
        with open(self.base_path + "/gpio" + gpio + "/value", "r") as re:
          value = re.read( )
      except Exception as e:
        print( e )

      return value


class Pwm(object):

    default_pwm_base_path = "/sys/class/pwm/"
    pwm_pins = [3, 4, 5, 6, 7, 9, 11, 10] # from pwm_1 to 8
    pwm_dict = {"3" : (0, 0), "4" : (0, 1), "5" : (0, 2), "6" : (0, 3), "7" : (1, 0), "9" : (1, 1), "11" : (1, 2), "10" : (1, 3)  }

    def __init__(self, _pwm_base_path=default_pwm_base_path):
        self.pwm_base_path = _pwm_base_path

    def setBasePath(self, _path):
        self.pwm_base_path = _path

    def export_pwm(self, pin):
        assert pin in pwm_pins

        bank, num = self.pwm_dict[ str(pin) ]
        try:
            with open(self.pwm_base_path + "/export", "w") as pwm:
                pwm.write(str( bank * 4 + num ))
        except Exception as e:
            print(e)

        return 0


    def unexport_pwm(self, pin):
        assert pin in pwm_pins

        bank, num = self.pwm_dict[ str(pin) ]
        try:
            with open(self.pwm_base_path + "/unexport", "w") as pwm:
                pwm.write(str( bank * 4 + num ))
        except Exception as e:
            print(e)

        return 0


    def analogWrite(self, pin, duty_cycle, period=100 , enable=1):
        bank, num = self.pwm_dict[ str(pin) ]

        try:
            with open(self.pwm_base_path + "pwmchip"+ bank +"/pwm"+ num +"/period", "w") as pwm:
                pwm.write( str(period) )
        except Exception as e:
            print(e)

        try:
            with open(self.pwm_base_path + "pwmchip"+ bank +"/pwm"+ num +"/duty_cycle", "w") as pwm:
                pwm.write( str(duty_cycle) )
        except Exception as e:
            print(e)

        try:
            with open(self.pwm_base_path + "pwmchip"+ bank +"/pwm"+ num +"/enable", "w") as pwm:
                pwm.write("1")
                pwm.flush()
        except Exception as e:
            print(e)


class Analogs(object):

    PATH_ADC_HOST      = '/sys/bus/iio/devices/'
    PATH_ADC_CONTAINER = '/var/adc/'
    PATH_ADC           = PATH_ADC_HOST
    ADC_FOLDER         = PATH_ADC

    A0 = ADC_FOLDER + 'iio:device0/' + 'in_voltage0_raw'
    A1 = ADC_FOLDER + 'iio:device0/' + 'in_voltage1_raw'
    A2 = ADC_FOLDER + 'iio:device0/' + 'in_voltage2_raw'
    A3 = ADC_FOLDER + 'iio:device0/' + 'in_voltage3_raw'
    A4 = ADC_FOLDER + 'iio:device1/' + 'in_voltage0_raw'
    A5 = ADC_FOLDER + 'iio:device1/' + 'in_voltage1_raw'

    DEFAULT_BURST_SIZE = 1024;

    def __init__(self, _base_path=PATH_ADC, _burst_size = DEFAULT_BURST_SIZE):
        self.path = _base_path
        self.burst_size = _burst_size
        A0 = self.path + 'iio:device0/' + 'in_voltage0_raw'
        A1 = self.path + 'iio:device0/' + 'in_voltage1_raw'
        A2 = self.path + 'iio:device0/' + 'in_voltage2_raw'
        A3 = self.path + 'iio:device0/' + 'in_voltage3_raw'
        A4 = self.path + 'iio:device1/' + 'in_voltage0_raw'
        A5 = self.path + 'iio:device1/' + 'in_voltage1_raw'

    def setBasePath(self, _basePath):
        self.path = _basePath
        A0 = self.path + 'iio:device0/' + 'in_voltage0_raw'
        A1 = self.path + 'iio:device0/' + 'in_voltage1_raw'
        A2 = self.path + 'iio:device0/' + 'in_voltage2_raw'
        A3 = self.path + 'iio:device0/' + 'in_voltage3_raw'
        A4 = self.path + 'iio:device1/' + 'in_voltage0_raw'
        A5 = self.path + 'iio:device1/' + 'in_voltage1_raw'

    def readAdc(self, pinPath):
        assert pinPath in (
            self.A0, self.A1, self.A2, self.A3, self.A4, self.A5
        )

        f = open(pinPath, 'r')
        data = int(f.read())
        f.close()
        return data

    def readBurst(self, pinPath, size=None):
        if size == None:
            size = self.burst_size

        data = list()
        for i in range( 0, int(size) ):
            data.append( readAdc(pinPath) )
        return data

    def analogRead(self, pin):
        return self.readAdc(pin)


class Accelerometer(object):

    def __init__(self):
        print("accelerometer")

    def getData(self):
        print("get data")

    def setFrequency(self):
        print("set freq")

    def enable(self):
        print("en")

    def disable(self):
        print("dis")


class Magnetometer(object):

    def __init__(self):
        print("magnetometer")

    def getData(self):
        print("get data")

    def setFrequency(self):
        print("set freq")

    def enable(self):
        print("en")

    def disable(self):
        print("dis")


class Gyroscope(object):

    def __init__(self):
        print("gyroscope")

    def getData(self):
        print("get data")

    def setFrequency(self):
        print("set freq")

    def enable(self):
        print("en")

    def disable(self):
        print("dis")



GPIO = 'GPIO'
PWM = 'PWM'


class UdooNeo( object ):

    def __init__(self):
        self.light_brick = LightBrick()
        self.temperature_brick = TemperatureBrick()
        self.barometric_brick = BarometricBrick()
        self.gpio = Gpio()
        self.pwm = Pwm()
        self.analog = Analogs()
        self.accelerometer = Accelerometer()
        self.magnetometer = Magnetometer()
        self.gyroscope = Gyroscope()
        print( "Neo lib initialized..." )


    def export(self, pin, mode):

        if mode == 'GPIO':
            gpio.export_gpio(pin)
        elif mode == 'PWM':
            pwm.export_pwm(pin)

        return 0

    def unexport(self, pin):
        gpio.unexport(pin)
        pwm.unexport(pin)

        return 0


    def getBoardId(self):
        try:
            with open("/sys/fsl_otp/HW_OCOTP_CFG0", "r") as reader:
                id0 = reader.read()
            with open("/sys/fsl_otp/HW_OCOTP_CFG1", "r") as reader:
                id1 = reader.read()

            id = "fds-" + str(id1[2:10]) + str(id0[2:10])
        except Exception as e:
            print(e)
            id = "fds-unknown"

        return id
