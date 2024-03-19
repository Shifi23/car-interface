import obd


def getV():
    connection = obd.OBD() # same constructor as 'obd.OBD()'

    return ((connection.query(obd.commands.ELM_VOLTAGE)).value) # non-blocking, returns immediately

def getR():
    connection = obd.OBD() # same constructor as 'obd.OBD()'

    return ((connection.query(obd.commands.RPM)).value) # non-blocking, returns immediately