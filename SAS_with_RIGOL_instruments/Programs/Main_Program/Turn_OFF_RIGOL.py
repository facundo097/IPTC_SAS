import RIGOL_lib as RIGOL
import pyvisa

rm = pyvisa.ResourceManager()
supply = rm.open_resource(rm.list_resources()[1])
load = rm.open_resource(rm.list_resources()[0])
dc_power = RIGOL.power_supply(supply, "DC Power Supply")
dc_load = RIGOL.load(load, "DC Electronic Load")

dc_load.set_function("RES")

dc_power.set_voltage_current(1, 0, 0)
dc_power.set_voltage_current(2, 0, 0)
dc_power.set_voltage_current(3, 0, 0)
dc_load.set_resistance(0.1)

dc_power.turn_off_channel(1)
dc_power.turn_off_channel(2)
dc_power.turn_off_channel(3)
dc_load.turn_off_load()