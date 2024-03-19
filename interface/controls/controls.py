import pyfirmata
import time

IGN = 4
SRT = 5
KSN = 7
PKL = 6
UNL = 8
LOC = 9
INL = 10
ACC = 11
global LocUL
global RunningFlag
global accS
global inlS
global pklS

RunningFlag = 0
accS = 0
inlS = 0
pklS = 0

try:
    board = pyfirmata.Arduino('/dev/ttyACM0')
    print("Communication Successfully started")


except:
    print("No Connection to Relay Controller")


else:

    board.digital[IGN].write(1)
    board.digital[SRT].write(1)
    board.digital[KSN].write(1)
    board.digital[PKL].write(1)
    board.digital[UNL].write(1)
    board.digital[LOC].write(1)
    board.digital[INL].write(1)
    board.digital[ACC].write(1)

    def StartCar():
        global RunningFlag
        board.digital[KSN].write(0)
        time.sleep(1)
        board.digital[IGN].write(0)
        time.sleep(1)
        board.digital[SRT].write(0)
        time.sleep(1)
        board.digital[SRT].write(1)
        time.sleep(1)
        board.digital[PKL].write(0)
        time.sleep(1)
        board.digital[ACC].write(0)
        RunningFlag = 1
        return RunningFlag

    def StopCar():
        board.digital[KSN].write(1)
        board.digital[IGN].write(1)
        board.digital[SRT].write(1)
        board.digital[PKL].write(1)
        board.digital[ACC].write(1)
        # add rpm code
        RunningFlag = 0
        return RunningFlag

    def UnlockCar():
        board.digital[UNL].write(0)
        time.sleep(0.5)
        board.digital[UNL].write(1)
        time.sleep(0.5)
        board.digital[UNL].write(0)
        time.sleep(0.5)
        board.digital[UNL].write(1)
        time.sleep(0.5)
        LocUL = "Unlocked"
        return LocUL

    def LockCar():
        board.digital[LOC].write(0)
        time.sleep(0.5)
        board.digital[LOC].write(1)
        time.sleep(0.5)
        board.digital[LOC].write(0)
        time.sleep(0.5)
        board.digital[LOC].write(1)
        time.sleep(0.5)
        LocUL = "Locked"
        return LocUL

    def acc():
        if accS == 0:
            board.digital[ACC].write(0)
            accS = 1
            return accS
        elif accS == 1:
            board.digital[ACC].write(1)
            accS = 0
            return accS

    def inl():
        if inlS == 0:
            board.digital[INL].write(0)
            inlS = 1
            return inlS
        elif inlS == 1:
            board.digital[INL].write(1)
            inlS = 0
            return inlS

    def pkl():
        global pklS
        if pklS == 0:
            board.digital[PKL].write(0)
            pklS = 1
            return pklS
        elif pklS == 1:
            board.digital[PKL].write(1)
            pklS = 0
            return pklS
