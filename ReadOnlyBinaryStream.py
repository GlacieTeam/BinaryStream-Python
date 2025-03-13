import ctypes


class ReadOnlyBinaryStream:
    mOwnedBuffer: bytearray
    mBufferView: memoryview
    mReadPointer: int
    mHasOverflowed: bool

    def __init__(
        self, buffer: bytearray = bytearray(), copyBuffer: bool = False
    ) -> None:
        if copyBuffer:
            self.mOwnedBuffer = buffer
            self.mBufferView = memoryview(self.mOwnedBuffer)
        else:
            self.mOwnedBuffer = bytearray()
            self.mBufferView = memoryview(buffer)
        self.mHasOverflowed = False
        self.mReadPointer = 0

    def getByte(self) -> ctypes.c_ubyte:
        if not self.mHasOverflowed:
            pointer = self.mReadPointer
            self.mReadPointer += 1
            if self.mReadPointer <= self.mBufferView.nbytes:
                return ctypes.c_ubyte(self.mBufferView[pointer])
        self.mHasOverflowed = True
        return ctypes.c_ubyte(0)

    def getUnsignedChar(self) -> ctypes.c_ubyte:
        return self.getByte()

    def getBool(self) -> bool:
        return bool(self.getByte().value)

    ## TODO

    def getUnsignedVarInt(self) -> ctypes.c_uint32:
        value = 0
        shift = 0
        next_byte = 0
        while True:
            next_byte = self.getByte().value
            value |= (next_byte & 0x7F) << shift
            shift += 7
            if not (next_byte & 0x80):
                break
        return ctypes.c_uint32(value)

    def getVarInt(self) -> ctypes.c_int32:
        decoded_value = self.getUnsignedVarInt().value
        if (decoded_value & 1) != 0:
            return ctypes.c_int32(~(decoded_value >> 1))
        else:
            return ctypes.c_int32(decoded_value >> 1)

    def getUnsignedVarInt64(self) -> ctypes.c_uint64:
        value = 0
        shift = 0
        next_byte = 0
        while True:
            next_byte = self.getByte().value
            value |= (next_byte & 0x7F) << shift
            shift += 7
            if not (next_byte & 0x80):
                break
        return ctypes.c_uint64(value)

    def getVarInt64(self) -> ctypes.c_int64:
        decoded_value = self.getUnsignedVarInt64().value
        if (decoded_value & 1) != 0:
            return ctypes.c_int64(~(decoded_value >> 1))
        else:
            return ctypes.c_int64(decoded_value >> 1)
