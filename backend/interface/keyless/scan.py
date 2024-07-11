import asyncio
from bleak import BleakScanner
import requests

# Define the MAC address of your phone's Bluetooth device
PHONE_DEVICE_ADDRESS = "5C:17:CF:D4:EE:6B"  # Replace with your phone's address

scanning_enabled = False

# Define your lock and unlock functions (replace with actual functions)
async def lock_car():
    print("Locking car doors...")
    # Implement your logic to lock the car doors here

async def unlock_car():
    print("Unlocking car doors...")
    # Implement your logic to unlock the car doors here

async def scan_for_phone():
    global scanning_enabled
    scanner = BleakScanner()
    locked = True

    while scanning_enabled:
        devices = await scanner.discover()
        phone_nearby = False
        phone_nearby = any(device.address == PHONE_DEVICE_ADDRESS for device in devices)

        
        if phone_nearby and locked:
            await unlock_car()
            locked = False

        elif not phone_nearby and not locked:
            await lock_car()
            locked = True
        
        await asyncio.sleep(2)  # Adjust the scanning interval as needed

async def start_scan():
    global scanning_enabled
    if not scanning_enabled:
        scanning_enabled = True
        await scan_for_phone()

async def stop_scan():
    global scanning_enabled
    scanning_enabled = False
