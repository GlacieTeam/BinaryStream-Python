from ReadOnlyBinaryStream import ReadOnlyBinaryStream
import ctypes


class BinaryStream(ReadOnlyBinaryStream):
    mBuffer: bytearray

    def __init__(
        self, buffer: bytearray = bytearray(), copyBuffer: bool = False
    ) -> None:
        super().__init__(bytes(buffer), copyBuffer)
        self.mBuffer = buffer

    def getAndReleaseData(self) -> bytearray:
        return self.mBuffer

    def writeByte(self, val: ctypes.c_ubyte) -> None:
        self.mBuffer.append(val.value)

    ## TODO

    def writeUnsignedVarInt(self, val: ctypes.c_uint32) -> None:
        uvalue = val.value
        next_byte = 0
        while True:
            next_byte = uvalue & 0x7F
            uvalue >>= 7
            if uvalue:
                next_byte |= 0x80
            self.writeByte(ctypes.c_ubyte(next_byte))
            if not uvalue:
                break

    def writeVarInt(self, val: ctypes.c_int32) -> None:
        if val.value >= 0:
            self.writeUnsignedVarInt(ctypes.c_uint32(2 * val.value))
        else:
            self.writeUnsignedVarInt(ctypes.c_uint32(~(2 * val.value)))

    def writeUnsignedVarInt64(self, val: ctypes.c_uint64) -> None:
        uvalue = val.value
        next_byte = 0
        while True:
            next_byte = uvalue & 0x7F
            uvalue >>= 7
            if uvalue:
                next_byte |= 0x80
            self.writeByte(ctypes.c_ubyte(next_byte))
            if not uvalue:
                break

    def writeVarInt64(self, val: ctypes.c_int64) -> None:
        if val.value >= 0:
            self.writeUnsignedVarInt64(ctypes.c_uint64(2 * val.value))
        else:
            self.writeUnsignedVarInt64(ctypes.c_uint64(~(2 * val.value)))
