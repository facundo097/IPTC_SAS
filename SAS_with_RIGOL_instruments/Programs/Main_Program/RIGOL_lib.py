import pyvisa
import time

def list_resources():
    rm = pyvisa.ResourceManager()
    # List all connected resources
    print("Resources detected: {}".format(rm.list_resources()))

# functions for power supply
class power_supply:
    def __init__(self, instrument, name=None):
        self.instrument = instrument
        self.name = name
        self.delay_enable = False
        self.mode = "2W"

        instrument.write("*IDN?")
        time.sleep(0.02)
        id = instrument.read()

        if "SPD1305X" in id:
            instrument.write_termination = '\n'
            instrument.read_termination = '\n'
            self.delay_enable = True

    # turn on channel
    def turn_on_channel(self, channel: int):
        if self.delay_enable:
            self.instrument.write("OUTP CH{:n},ON".format(channel))
            time.sleep(0.02)
            return "ON"
        else:
            self.instrument.write(":OUTPUT CH{:n},ON".format(channel))
            return self.instrument.query(":OUTP? CH{}".format(channel))

    # turn off channel
    def turn_off_channel(self, channel: int):
        if self.delay_enable:
            self.instrument.write("OUTP CH{:n},OFF".format(channel))
            time.sleep(0.02)
            return "OFF"
        self.instrument.write(":OUTPUT CH{:n},OFF".format(channel))
        return self.instrument.query(":OUTP? CH{}".format(channel))

    def set_voltage_current(self, channel: int, voltage: float, current: float):
        if self.delay_enable:
            self.instrument.write("CH{}:VOLT {}".format(channel, voltage))
            time.sleep(0.02)
            self.instrument.write("CH{}:CURR {}".format(channel, current))
            time.sleep(0.02)
            self.instrument.write("CH{}:VOLT?".format(channel))
            time.sleep(0.02)
            voltMeas = self.instrument.read()
            time.sleep(0.02)
            self.instrument.write("CH{}:CURR?".format(channel))
            time.sleep(0.02)
            currMeas = self.instrument.read()
            time.sleep(0.02)
            return "CH1:30V/5A," + voltMeas + "," + currMeas
        else:
            self.instrument.write(":APPLY CH{},{},{}".format(channel, voltage, current))
            return self.instrument.query("APPLY? CH{}".format(channel))

    # measure everything (in order returns: voltage, current and power)
    def measure_all(self, channel: int):
        if self.delay_enable:
            self.instrument.write("MEAS:VOLT? CH1")
            time.sleep(0.02)
            voltage = float(self.instrument.read())
            time.sleep(0.02)
            self.instrument.write("MEAS:CURR? CH1")
            time.sleep(0.02)
            current = float(self.instrument.read())
            time.sleep(0.02)
            self.instrument.write("MEAS:POWE? CH1")
            time.sleep(0.02)
            power = float(self.instrument.read())
            time.sleep(0.02)
            return voltage, current, power
        else:
            measurement = self.instrument.query(":MEASURE:ALL?").split(",")
            measurement[-1] = measurement[-1][:-1]
            voltage = measurement[0]
            current = measurement[1]
            power = measurement[2]
            return float(voltage), float(current), float(power)

    def toggle_4w(self):
        if self.delay_enable:
            if self.mode == "2W":
                self.mode = "4W"
                self.instrument.write("MODE:SET {}".format(self.mode))
                time.sleep(0.5)
                return "4W"
            elif self.mode == "4W":
                self.mode = "2W"
                self.instrument.write("MODE:SET {}".format(self.mode))
                time.sleep(0.5)
                return "2W"
        else:
            if self.mode == "2W":
                self.mode = "4W"
                self.instrument.write(":OUT:SENS CH1,ON")
                return "4W"
            elif self.mode == "4W":
                self.mode = "2W"
                self.instrument.write(":OUT:SENS CH1,OFF")
                return "2W"



# functions for the electronic load
class load:
    def __init__(self, instrument, name=None):
        self.load = instrument
        self.name = name

    # set function : RES, CURR, VOLT, POW
    def set_function(self, funcion: str):
        self.load.write(":SOUR:FUNC {}".format(funcion))
        return self.load.query(":SOUR:FUNC?")


    def measure_all(self):
        V = float(self.load.query("MEAS:VOLT?"))
        time.sleep(0.02)
        I = float(self.load.query("MEAS:CURR?"))
        time.sleep(0.02)
        R = float(self.load.query('MEAS:RES?'))
        return V, I, R

    # measure resistance
    def measure_resistance(self):
        R = self.load.query('MEAS:RES?')
        return float(R)

    # turn on load
    def turn_on_load(self):
        self.load.write(":SOUR:INP:STAT 1")
        return self.load.query(":SOUR:INP:STAT?")

    # turn off load
    def turn_off_load(self):
        self.load.write(":SOUR:INP:STAT 0")
        return self.load.query(":SOUR:INP:STAT?")

    # set current only if you are on CC
    def set_current(self, current: float):
        self.load.write(":SOUR:CURR:LEV:IMM {}".format(current))
        return self.load.query(":SOUR:CURR:LEV:IMM?")

    # set voltage only if you are on CV
    def set_voltage(self, voltage: float):
        self.load.write(":SOUR:VOLT:LEV:IMM {}".format(voltage))
        return self.load.query(":SOUR:VOLT:LEV:IMM?")

    # set resistance only if you are on CR
    def set_resistance(self, resistance: float):
        self.load.write(":SOUR:RES:LEV:IMM {}".format(resistance))
        return self.load.query(":SOUR:RES:LEV:IMM?")

    # set resistance only if you are on CP (need to verify function)
    def set_power(self, power: float):
        self.load.write(":SOUR:POW:LEV:IMM {}".format(power))
        return self.load.query(":SOUR:POW:LEV:IMM?")

    def set_resistance_range(self, range: str):
        # Set the resistance range
        #resistance_range_command = f":RESistance:RANGe MINimum"
        if range == "min":
            resistance_range_command = ":RESistance:RANGe 15"
        else:
            resistance_range_command = ":RESistance:RANGe 15000"
        self.load.write(resistance_range_command)
        return self.load.query(":SOUR:RES:RANG?")

def CalculateResistance(Vsens, Isens):
    if Isens != 0 :
        return Vsens/Isens
    else :
        print("Error: I = 0")
        return 0

