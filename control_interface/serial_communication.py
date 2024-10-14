import serial  # Importa la biblioteca serial para comunicación serial

class SerialCommunication:
    def __init__(self):
        pass
        # self.com = serial.Serial("COM9", 115200, write_timeout=10)
        # Inicialización del objeto serial para comunicación, actualmente comentado

    def sending_data(self, command: str) -> None:
        # Método para enviar datos a través de la comunicación serial


        # Enviar comando a través de la comunicación serial
        #self.com.write(command.encode('ascii'))  # Envía el comando codificado en ASCII

        #TODO:  Enviar comando a pygame 

        print(f'SENDING DATA: {command}')  # Imprime en consola el comando que se enviaría
        pass  # No realiza ninguna acción actualmente en el código