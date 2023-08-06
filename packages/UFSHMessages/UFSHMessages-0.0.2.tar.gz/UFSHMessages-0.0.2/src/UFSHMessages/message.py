from schema import Schema, SchemaFactory, schema_map
import struct

class MessageType:
    Manifest = "MAN"
    Set = "SET"

class Message:

    def __init__(self, type=None, device=None):
        self.type: str = type
        self.device: int = device
        self.schema_id: int = None
        self.schema: Schema = None

    _s = "3sBH"
    _s_size = struct.calcsize(_s)

    def pack(self) -> bytes:
        d = struct.pack(self._s, self.type.encode('ascii'), self.device, self.schema_id)
        d += self.schema.pack()
        return d

    def unpack(self, data: bytes) -> None:
        type_tmp: bytes = None
        (type_tmp, self.device, self.schema_id) = struct.unpack(self._s, data[:struct.calcsize(self._s)])
        self.type = type_tmp.decode("ASCII")
        self.schema = SchemaFactory.schema_from_message(self)
        self.schema.unpack(data[struct.calcsize(self._s):])

    def set_schema(self, schema: Schema):
        self.schema_id = schema.schema_id
        self.schema = schema

    def __str__(self) -> str:
        return ''.join([
            f"Type: {self.type}\n",
            f"Device: {self.device}\n",
            f"SchemaID: {self.schema_id}\n",
        ])