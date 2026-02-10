from pycommander_cli import Commander

pc = Commander(serial_number="440343139", target_device="EFR32MG24", debug_speed=1000)
pc.device.recover()
# print(pc.getVersionString())

# print(pc.device.info())

# print(pc.device.pageerase(ranges=[(0x08000000, 0x08000010), (0x08002000, 0x08002100)]))

# print(pc.device.reset())


from pathlib import Path
from pycommander_cli import Adapter

adapter = Adapter(serial_number="440343139", target_device="EFR32MG24")
print(adapter.info())
print(adapter.target.info())


# print(adapter.target.getCTUNE())

# print(adapter.target.setCTUNE(100))
# print(adapter.target.getCTUNE())

# print(adapter.target.setCTUNE())
# print(adapter.target.getCTUNE())

# print(adapter.target.setCTUNE(92))
# print(adapter.target.getCTUNE())

# print(adapter.target.setCTUNE(92, force=True))
# print(adapter.target.getCTUNE())

# print(adapter.device())