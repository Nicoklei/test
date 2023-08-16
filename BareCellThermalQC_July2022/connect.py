from basil.dut import Dut
import time

dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
dut.init()
d = dut["PowerSupply"]

d.set_channel(1)
#d.set_current(3)
#a = d.get_current()
#print(a)

#time.sleep(0.1)
#d.set_voltage(5)
#a = d.get_voltage()
#print(a)

d.on()

for i in range(5):
    time.sleep(1)
    d.set_voltage(i)
    time.sleep(0.5)
    a = d.get_voltage()
    time.sleep(0.1)
    b = d.get_current()
    print(a,b)
    time.sleep(1)

d.off()