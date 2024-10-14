# ---------------------------------------------------------------------------- #
#                                                                              #
# Module:       main.py                                                        #
# Author:       Aprende e Ingenia                                              #
# Created:      2/26/2024, 6:59:41 PM                                          #
# Description:  EXP project                                                    #
#                                                                              #
# ---------------------------------------------------------------------------- #

# vex:disable=repl

# Importación de bibliotecas
from vex import *

# Brain debería estar definido por defecto
brain = Brain()

# Configuración de motores
brain_inertial = Inertial()
left_drive = Motor(Ports.PORT1, True)
right_drive = Motor(Ports.PORT5, True)
drivetrain = SmartDrive(left_drive, right_drive, brain_inertial, 259.34, 320, 40, MM, 1)

# Mensaje en pantalla del Brain
brain.screen.print("Gesture control")

# Función para monitorear el puerto serial
def serial_monitor():
    try:
        s = open('/dev/serial1', 'rb')  # Abre el puerto serial para lectura binaria
    except:
        raise Exception('serial port not available')  # Lanza una excepción si el puerto serial no está disponible
    
    while True:
        data = s.read(1)  # Lee un byte de datos del puerto serial
        print(data)  # Imprime los datos leídos
        
        # Procesa los datos recibidos para controlar el robot
        if data == b'a' or data == b'A':
            brain.screen.print_at("forward", x=5, y=40)
            right_drive.spin(FORWARD, 50)
            left_drive.spin(REVERSE, 50)
        elif data == b'r' or data == b'R':
            brain.screen.print_at("reverse", x=5, y=40)
            right_drive.spin(REVERSE, 50)
            left_drive.spin(FORWARD, 50)
        elif data == b'd' or data == b'D':
            brain.screen.print_at("right  ", x=5, y=40)
            right_drive.spin(REVERSE, 50)
            left_drive.spin(REVERSE, 50)
        elif data == b'i' or data == b'I':
            brain.screen.print_at("left   ", x=5, y=40)
            right_drive.spin(FORWARD, 50)
            left_drive.spin(FORWARD, 50)
        elif data == b'p' or data == b'P':
            brain.screen.print_at("stop   ", x=5, y=40)
            right_drive.stop()
            left_drive.stop()

# Creación de un hilo para la función serial_monitor
t1 = Thread(serial_monitor)