import obd
from obd import OBDStatus

#globals

voltage = 0
rpm = 0
speed = 0
coolant_temp = 0
intake_temp = 0
mass_airflow_rate = 0
throttle_position = 0
engine_load = 0
dtc = None


class ObdManager:
    def __init__(self):
        # obd.logger.setLevel(obd.logging.DEBUG)
        self.connection = obd.OBD("/dev/rfcomm0", baudrate=38400)
        if self.connection.status() == OBDStatus.CAR_CONNECTED:
            self.connection.close()
            self.start_async_connection()
    
    def start_async_connection(self):

        self.connection = obd.Async(portstr="/dev/rfcomm0", baudrate=38400, delay_cmds=0)

        self.connection.watch(obd.commands.ELM_VOLTAGE, callback=self.update_voltage)
        self.connection.watch(obd.commands.RPM, callback=self.update_rpm)
        self.connection.watch(obd.commands.SPEED, callback=self.update_speed)
        self.connection.watch(obd.commands.COOLANT_TEMP, callback=self.update_coolant_temp)
        self.connection.watch(obd.commands.INTAKE_TEMP,callback=self.update_intake_temp)
        self.connection.watch(obd.commands.MAF, callback=self.update_mass_airflow_rate)
        self.connection.watch(obd.commands.THROTTLE_POS, callback=self.update_throttle_position)
        self.connection.watch(obd.commands.ENGINE_LOAD, callback=self.update_engine_load)
        self.connection.watch(obd.commands.GET_DTC, callback=self.update_dtc)

        self.connection.start()
    
    def clear_DTC(self):
        self.stop_async_connection()
        self.connection = obd.OBD("/dev/rfcomm0", baudrate=38400)
        self.connection.query(obd.commands.CLEAR_DTC)


    def update_ignition_off_voltage(self):
        global voltage
        voltage = (self.connection.query(obd.commands.ELM_VOLTAGE)).value.magnitude

    def update_voltage(self, r):
        global voltage
        voltage = r.value.magnitude

    def update_rpm(self, r):
        global rpm
        rpm = r.value.magnitude
    
    def update_speed(self, r):
        global speed
        speed = r.value.to("mph")
        speed = speed.magnitude
    
    def update_coolant_temp(self, r):
        global coolant_temp
        coolant_temp = r.value.magnitude
    
    def update_intake_temp(self, r):
        global intake_temp
        intake_temp = r.value.magnitude
    
    def update_mass_airflow_rate(self, r):
        global mass_airflow_rate
        mass_airflow_rate = r.value.magnitude
    
    def update_throttle_position(self, r):
        global throttle_position
        throttle_position = r.value.magnitude
    
    def update_engine_load(self, r):
        global engine_load
        engine_load = r.value.magnitude
    
    def update_dtc(self, r):
        global dtc
        dtc = r.value

    def stop_async_connection(self):
        self.connection.stop()
        self.connection.close()

    def __exit__(self):
        self.connection.close()

