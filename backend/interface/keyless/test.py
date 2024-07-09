import asyncio

from bleak import BleakScanner, BleakClient

import asyncio
from bleak import BleakScanner

async def main():
    device = await BleakScanner.find_device_by_address("5C:17:CF:D4:EE:6B", timeout=5)
    # for d in devices:
    #     p = d.details["props"]
    #     if "Name" in p:
    #         if p["Name"] == "OnePlus 8T+ 5G":
    #             mydevice = d
    #         print(p["Name"])

    # print(mydevice.details, mydevice.address)
    print(device.details)
    


asyncio.run(main())
