import typing
import struct


class ReadOnlyBinaryStream:
    mOwnedBuffer: bytearray | None
    mBufferView: bytearray
    mReadPointer: int
    mHasOverflowed: bool

    def __init__(
        self, buffer: typing.ByteString = b"", copyBuffer: bool = False
    ) -> None:
        if copyBuffer:
            self.mOwnedBuffer = bytearray(buffer)
            self.mBufferView = self.mOwnedBuffer
        else:
            self.mOwnedBuffer = None
            self.mBufferView = (
                buffer if isinstance(buffer, bytearray) else bytearray(buffer)
            )
        self.mReadPointer = 0
        self.mHasOverflowed = False

    def swapEndian(self, value: int, fmt: str) -> int:
        return struct.unpack(f">{fmt}", struct.pack(f"<{fmt}", value))[0]

    def read(
        self, fmt: str, size: int, bigEndian: bool = False
    ) -> typing.Optional[typing.Union[int, float]]:
        if self.mHasOverflowed:
            return None
        if self.mReadPointer + size > len(self.mBufferView):
            self.mHasOverflowed = True
            return None
        data: memoryview[int] = memoryview(self.mBufferView)[
            self.mReadPointer : self.mReadPointer + size
        ]
        self.mReadPointer += size
        endian: typing.Literal[">"] | typing.Literal["<"] = ">" if bigEndian else "<"
        try:
            value: typing.Union[int, float] = struct.unpack(
                f"{endian}{fmt}", data.tobytes()
            )[0]
            return value
        except struct.error:
            return None

    def getPosition(self) -> int:
        return self.mReadPointer

    def getLeftBuffer(self) -> bytes:
        return bytes(self.mBufferView[self.mReadPointer :])

    def isOverflowed(self) -> bool:
        return self.mHasOverflowed

    def hasDataLeft(self) -> bool:
        return self.mReadPointer < len(self.mBufferView)

    def getBytes(self, target: bytearray, num: int) -> bool:
        if self.mHasOverflowed or self.mReadPointer + num > len(self.mBufferView):
            self.mHasOverflowed = True
            return False
        target[:] = self.mBufferView[self.mReadPointer : self.mReadPointer + num]
        self.mReadPointer += num
        return True

    def getByte(self) -> int:
        return typing.cast(int, self.read("B", 1)) or 0

    def getUnsignedChar(self) -> int:
        return self.getByte()

    def getUnsignedShort(self) -> int:
        return typing.cast(int, self.read("H", 2)) or 0

    def getUnsignedInt(self) -> int:
        return typing.cast(int, self.read("I", 4)) or 0

    def getUnsignedInt64(self) -> int:
        return typing.cast(int, self.read("Q", 8)) or 0

    def getBool(self) -> bool:
        return True if self.getByte() else False

    def getDouble(self) -> float:
        return self.read("d", 8) or 0.0

    def getFloat(self) -> float:
        return self.read("f", 4) or 0.0

    def getSignedInt(self) -> int:
        return typing.cast(int, self.read("i", 4)) or 0

    def getSignedInt64(self) -> int:
        return typing.cast(int, self.read("q", 8)) or 0

    def getSignedShort(self) -> int:
        return typing.cast(int, self.read("h", 2)) or 0

    def getUnsignedVarInt(self) -> int:
        value = 0
        shift = 0
        while True:
            byte: int = self.getByte()
            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
        return value

    def getUnsignedVarInt64(self) -> int:
        value = 0
        shift = 0
        while True:
            byte: int = self.getByte()
            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
            if shift >= 64:
                raise ValueError("VarInt too large")
        return value

    def getVarInt(self) -> int:
        decoded = self.getUnsignedVarInt()
        return ~(decoded >> 1) if (decoded & 1) else decoded >> 1

    def getVarInt64(self) -> int:
        decoded = self.getUnsignedVarInt64()
        return ~(decoded >> 1) if (decoded & 1) else decoded >> 1

    def getNormalizedFloat(self) -> float:
        return self.getVarInt64() / 2147483647.0

    def getSignedBigEndianInt(self) -> int:
        return typing.cast(int, self.read("i", 4, bigEndian=True)) or 0

    def getString(self) -> str:
        length: int = self.getUnsignedVarInt()
        if length == 0:
            return ""
        if self.mReadPointer + length > len(self.mBufferView):
            self.mHasOverflowed = True
            return ""
        data: bytearray = self.mBufferView[
            self.mReadPointer : self.mReadPointer + length
        ]
        self.mReadPointer += length
        return data.decode("utf-8")

    def getUnsignedInt24(self) -> int:
        if self.mReadPointer + 3 > len(self.mBufferView):
            self.mHasOverflowed = True
            return 0
        data: bytearray = self.mBufferView[self.mReadPointer : self.mReadPointer + 3]
        self.mReadPointer += 3
        return int.from_bytes(data, byteorder="little", signed=False)
