from config import ConfigControllableRange, ConfigData, ConfigFactory, ConfigID, ConfigNamedBinary, config_map
import struct

class InacceptableConfigException(Exception):
    def __init__(self):
        super().__init__("Schema does not accept a config of this type")

class SchemaID:
    #No schema can never be sent since the value is unsigned. This is for internal use only.
    #The protocol should ALWAYS send a schema!
    NoSchema = -1
    Config = 0
    GenericBinary = 1
    GenericRange = 2

class Schema:
    schema_id = SchemaID.NoSchema

    def __init__(self):
        self.name = "New Device"
        self.value = None

    def pack(self) -> bytes:
        raise NotImplementedError()

    def unpack(self, data: bytes) -> None:
        raise NotImplementedError()

    def configure(self, config: ConfigData):
        raise NotImplementedError("This schema is not configurable")

    def __str__(self):
        return f"SchemaID: {self.schema_id} - {self.__class__.__name__}\nName: {self.name}\nValue:{self.value}\n"

class Config(Schema):
    schema_id = SchemaID.Config
    _s = "hh32s"

    def __init__(self):
        self.schema_type = 0
        self.config_type = 0
        self.config: ConfigData = None
        self.name = "Config"

    def pack(self):
        d = struct.pack(self._s, self.schema_type, self.config_type, self.name.encode('ascii'))
        if self.config_type != 0:
            d += self.config.pack()
        return d
    
    def unpack(self, data: bytes):
        # Unpack the config
        tmpname: bytes = None
        (self.schema_id, self.config_type, tmpname) = struct.unpack(self._s, data[:struct.calcsize(self._s)])
        self.name = tmpname.decode('ASCII')
        if self.config_type != 0:
            self.config = ConfigFactory.config_from_id(self.config_type)
            self.config.unpack(data[struct.calcsize(self._s):])

    def create_schema(self) -> Schema:
        # Create the appropriate schema
        schema = SchemaFactory.schema_from_id(self.schema_id)
        # Configure the schema.
        if(self.config_type != 0):
            schema.configure(self.config)

        if(self.name):
            schema.name = self.name

        return schema

    def set_config(self, config: ConfigData):
        self.config_type = config.config_id
        self.config = config

    def __str__(self):
        base = super().__str__()
        return '\n'.join([
            base,
            "Config INFO:",
            f"Schema Type: {self.schema_type} - {schema_map[self.schema_type.__class__.__name__]}",
            f"Config ID: {self.config_type} - {config_map[self.config_type].__class__.__name__}"
        ])

class GenericBinary(Schema):
    schema_id = SchemaID.GenericBinary

    def __init__(self):
        super().__init__()
        self.name = "New Switch"
        self.on_label = "On"
        self.off_label = "Off"
        self.value = None

    def configure(self, config: ConfigNamedBinary):
        if config.config_id != ConfigNamedBinary.config_id:
            raise InacceptableConfigException()

        self.on_label = config.on_name
        self.off_label = config.off_name

    def __str__(self):
        base = super().__str__()
        return '\n'.join([
            base,
            f"On Label: {self.on_label}",
            f"Off label: {self.off_label}"
        ])


class GenericRange(Schema):
    schema_id = SchemaID.GenericRange
    def __init__(self):
        super().__init__()
        self.name = "New Range"
        self.value = None
        # These values are not transferred with the schema, but are provided by the config.
        self.min = 0
        self.max = 100

    def configure(self, config: ConfigControllableRange):
        if not config.config_id == ConfigControllableRange.config_id:
            raise InacceptableConfigException()

        (self.min, self.max) = (config.min, config.max)

    def __str__(self):
        base = super().__str__()
        return '\n'.join([
            f"Min: {self.min}",
            f"Max: {self.max}"
        ])

class SchemaFactory:
    @staticmethod
    def schema_from_id(id: int) -> Schema:
        return schema_map[id]()

    @staticmethod
    def schema_from_message(message) -> Schema:
        return schema_map[message.schema_id]()

schema_map = {
    SchemaID.Config: Config,
    SchemaID.GenericBinary: GenericBinary,
    SchemaID.GenericRange: GenericRange
}