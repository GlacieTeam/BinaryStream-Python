from .read_only_binary_stream import ReadOnlyBinaryStream
from typing import Union, Literal
import struct
import ctypes


class BinaryStream(ReadOnlyBinaryStream):
    _buffer: bytearray

    def __init__(self, buffer: bytearray = bytearray()) -> None:
        self._buffer = buffer
        super().__init__(self._buffer)

    def set_position(self, value: int) -> None:
        self._read_pointer: int = value

    def reset(self) -> None:
        self._buffer.clear()
        self._read_pointer = 0
        self._has_overflowed = False

    def get_and_release_data(self) -> bytes:
        data = bytes(self._buffer)
        self.reset()
        return data

    def _write(
        self, fmt: str, value: Union[int, float], bigEndian: bool = False
    ) -> None:
        endian: Literal[">"] | Literal["<"] = ">" if bigEndian else "<"
        self._buffer.extend(struct.pack(f"{endian}{fmt}", value))

    def write_bytes(self, origin: bytes, num: int) -> None:
        self._buffer.extend(origin[:num])

    def write_byte(self, value: int) -> None:
        self._write("B", ctypes.c_uint8(value).value)

    def write_unsigned_char(self, value: int) -> None:
        self.write_byte(ctypes.c_uint8(value).value)

    def write_unsigned_short(self, value: int) -> None:
        self._write("H", ctypes.c_uint16(value).value)

    def write_unsigned_int(self, value: int) -> None:
        self._write("I", ctypes.c_uint32(value).value)

    def write_unsigned_int64(self, value: int) -> None:
        self._write("Q", ctypes.c_uint64(value).value)

    def write_bool(self, value: bool) -> None:
        self.write_byte(ctypes.c_bool(value).value)

    def write_double(self, value: float) -> None:
        self._write("d", ctypes.c_double(value).value)

    def write_float(self, value: float) -> None:
        self._write("f", ctypes.c_float(value).value)

    def write_signed_int(self, value: int) -> None:
        self._write("i", ctypes.c_int32(value).value)

    def write_signed_int64(self, value: int) -> None:
        self._write("q", ctypes.c_int64(value).value)

    def write_signed_short(self, value: int) -> None:
        self._write("h", ctypes.c_int16(value).value)

    def write_unsigned_varint(self, uvalue: int) -> None:
        uvalue = ctypes.c_uint32(uvalue).value
        while True:
            byte = uvalue & 0x7F
            uvalue >>= 7
            if uvalue:
                byte |= 0x80
            self.write_byte(byte)
            if not uvalue:
                break

    def write_unsigned_varint64(self, uvalue: int) -> None:
        uvalue = ctypes.c_uint64(uvalue).value
        while True:
            byte: int = uvalue & 0x7F
            uvalue >>= 7
            if uvalue:
                byte |= 0x80
            self.write_byte(byte)
            if not uvalue:
                break

    def write_varint(self, value: int) -> None:
        value = ctypes.c_int32(value).value
        if value >= 0:
            self.write_unsigned_varint(2 * value)
        else:
            self.write_unsigned_varint(~(2 * value))

    def write_varint64(self, value: int) -> None:
        value = ctypes.c_int64(value).value
        self.write_unsigned_varint64(2 * value if value >= 0 else ~(2 * value))

    def write_normalized_float(self, value: float) -> None:
        value = int(ctypes.c_float(value).value * 2147483647.0)
        if value > 0x7FFFFFFF:
            value = value - 0x100000000
        elif value < -0x80000000:
            value = value + 0x100000000
        self.write_varint64(value & 0xFFFFFFFF)

    def write_signed_big_endian_int(self, value: int) -> None:
        value = ctypes.c_int32(value).value
        self._write("i", value, bigEndian=True)

    def write_string(self, value: str) -> None:
        data: bytes = value.encode("utf-8")
        self.write_unsigned_varint(len(data))
        self.write_bytes(data, len(data))

    def write_unsigned_int24(self, value: int) -> None:
        value = ctypes.c_uint32(value).value
        self._buffer.extend(value.to_bytes(3, "little"))
