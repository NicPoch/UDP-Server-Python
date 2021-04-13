"""
El objeto paquete que se va a usar para tranferir datos
"""
class Packet:
    """
    data: los datos a transferir
    chacksum: el checksum para validar
    """
    def __init__(self,data=None,check=None,flag="RQ"):
        self.data=data
        self.check=check
        self.flag=flag