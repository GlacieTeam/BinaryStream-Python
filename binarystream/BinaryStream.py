from .ReadOnlyBinaryStream import ReadOnlyBinaryStream
from typing import Union, Literal
import struct
import ctypes


class BinaryStream(ReadOnlyBinaryStream):
    mBuffer: bytearray

    def __init__(self, buffer: bytearray = bytearray()) -> None:
        self.mBuffer = buffer
        super().__init__(self.mBuffer)

    def setPosition(self, value: int) -> None:
        self.mReadPointer: int = value

    def reset(self) -> None:
        self.mBuffer.clear()
        self.mReadPointer = 0
        self.mHasOverflowed = False

    def getAndReleaseData(self) -> bytes:
        data = bytes(self.mBuffer)
        self.reset()
        return data

    def write(
        self, fmt: str, value: Union[int, float], bigEndian: bool = False
    ) -> None:
        endian: Literal[">"] | Literal["<"] = ">" if bigEndian else "<"
        self.mBuffer.extend(struct.pack(f"{endian}{fmt}", value))

    def writeBytes(self, origin: bytes, num: int) -> None:
        self.mBuffer.extend(origin[:num])

    def writeByte(self, value: int) -> None:
        self.write("B", ctypes.c_uint8(value).value)

    def writeUnsignedChar(self, value: int) -> None:
        self.writeByte(ctypes.c_uint8(value).value)

    def writeUnsignedShort(self, value: int) -> None:
        self.write("H", ctypes.c_uint16(value).value)

    def writeUnsignedInt(self, value: int) -> None:
        self.write("I", ctypes.c_uint32(value).value)

    def writeUnsignedInt64(self, value: int) -> None:
        self.write("Q", ctypes.c_uint64(value).value)

    def writeBool(self, value: bool) -> None:
        self.writeByte(ctypes.c_bool(value).value)

    def writeDouble(self, value: float) -> None:
        self.write("d", ctypes.c_double(value).value)

    def writeFloat(self, value: float) -> None:
        self.write("f", ctypes.c_float(value).value)

    def writeSignedInt(self, value: int) -> None:
        self.write("i", ctypes.c_int32(value).value)

    def writeSignedInt64(self, value: int) -> None:
        self.write("q", ctypes.c_int64(value).value)

    def writeSignedShort(self, value: int) -> None:
        self.write("h", ctypes.c_int16(value).value)

    def writeUnsignedVarInt(self, uvalue: int) -> None:
        uvalue = ctypes.c_uint32(uvalue).value
        while True:
            byte = uvalue & 0x7F
            uvalue >>= 7
            if uvalue:
                byte |= 0x80
            self.writeByte(byte)
            if not uvalue:
                break

    def writeUnsignedVarInt64(self, uvalue: int) -> None:
        uvalue = ctypes.c_uint64(uvalue).value
        while True:
            byte: int = uvalue & 0x7F
            uvalue >>= 7
            if uvalue:
                byte |= 0x80
            self.writeByte(byte)
            if not uvalue:
                break

    def writeVarInt(self, value: int) -> None:
        value = ctypes.c_int32(value).value
        if value >= 0:
            self.writeUnsignedVarInt(2 * value)
        else:
            self.writeUnsignedVarInt(~(2 * value))

    def writeVarInt64(self, value: int) -> None:
        value = ctypes.c_int64(value).value
        self.writeUnsignedVarInt64(2 * value if value >= 0 else ~(2 * value))

    def writeNormalizedFloat(self, value: float) -> None:
        value = int(ctypes.c_float(value).value * 2147483647.0)
        if value > 0x7FFFFFFF:
            value = value - 0x100000000
        elif value < -0x80000000:
            value = value + 0x100000000
        self.writeVarInt64(value & 0xFFFFFFFF)

    def writeSignedBigEndianInt(self, value: int) -> None:
        value = ctypes.c_int32(value).value
        self.write("i", value, bigEndian=True)

    def writeString(self, value: str) -> None:
        data: bytes = value.encode("utf-8")
        self.writeUnsignedVarInt(len(data))
        self.writeBytes(data, len(data))

    def writeUnsignedInt24(self, value: int) -> None:
        value = ctypes.c_uint32(value).value
        self.mBuffer.extend(value.to_bytes(3, "little"))
