import bluetooth
import logging
import time
import sys
# Pairing is necessary for mac address spoofing
# bluetoothctl scan on pair
# logs at journalctl -b -u keyless.service -f


target_address = "5C:17:CF:D4:EE:6B"  # shuhrats phone
# target_address = "88:66:5A:C7:3F:DA"  # shuhrats ipad
lastState = "away"  # host down
sleepTime = 2


while True:
    try:
        btsocket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        btsocket.connect((target_address, 3))
        if btsocket.send("init") and lastState == "away":
            logger.info("device found %s" % (target_address))
            logger.info("Unlocking car...")
            UnlockCar()
            flashpkl()
            logger.info("unlock")
            lastState = "connected"
            btsocket.close()
        time.sleep(sleepTime)

    # terrible way to check error, but e.errno didn't work
    except bluetooth.btcommon.BluetoothError as e:
        if lastState == "connected" and "112" in str(e):
            logger.info("Locking car...")
            LockCar()
            flashpkl()
            logger.info("lock")
            lastState = "away"
        time.sleep(sleepTime)

    # killing program
    except KeyboardInterrupt:
        btsocket.close()
        logger.info("program terminated")
        time.sleep(sleepTime)
        sys.exit(1)

    # all other exceptions
    except:
        LockCar()
        flashpkl()
        logger.info("lock")
        btsocket.close()