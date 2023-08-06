import struct

class ConfigID:
    NoneConfig = 0
    ConfigControllableRange = 1
    ConfigNamedBinary = 2

class ConfigData:
    """
    The base config data class to be extended with correct functionality.
    The base config class is also mapped to the non config for "safe" handling
    of attempting to unpack the none config.
    """
    config_id = ConfigID.NoneConfig
    
    def unpack(self, data: bytes):
        raise NotImplementedError("The none config cannot be unpacked")

    def pack(self):
        raise NotImplementedError("The none config cannot be packed")

class ConfigControllableRange(ConfigData):
    config_id = ConfigID.ConfigControllableRange

    def __init__(self) -> None:
        self.min = 0
        self.max = 100
    
    def pack(self):
        return struct.pack("hh", self.min, self.max)

    def unpack(self, data: bytes):
        structure = "hh"
        (self.min, self.max) = struct.unpack(structure, data[:struct.calcsize(structure)])

class ConfigNamedBinary(ConfigData):

    def __init__(self) -> None:
        self.on_name: str = None
        self.off_name: str = None

    def pack(self):
        return struct.pack("32s32s", self.on_name.encode('ascii'), self.off_name.encode('ascii'))

    def unpack(self, data: bytes):
        tmp_on: bytes = None
        tmp_off: bytes = None
        structure = "32s32s"
        (tmp_on, tmp_off) = struct.unpack(structure, data[:struct.calcsize(structure)])
        on_name = tmp_on.decode('ascii').rstrip('\x00')
        off_name = tmp_off.decode('ascii').rstrip('\x00')

class ConfigFactory:
    @staticmethod
    def config_from_id(id: int) -> ConfigData:
        return config_map[id]()

config_map = {
    ConfigID.NoneConfig: ConfigData,
    ConfigID.ConfigControllableRange: ConfigControllableRange,
    ConfigID.ConfigNamedBinary: ConfigNamedBinary
}