from .read_only_binary_stream import ReadOnlyBinaryStream
from typing import Union, Literal
import struct


class BinaryStream(ReadOnlyBinaryStream):
    _buffer: bytearray

    def __init__(
        self, buffer: Union[bytearray, bytes] = bytearray(), copy_buffer: bool = False
    ) -> None:
        if isinstance(buffer, bytes):
            buffer = bytearray(buffer)
        if copy_buffer:
            self._buffer = bytearray(buffer)
            self._owned_buffer = bytes(self._buffer)
            self._buffer_view = self._owned_buffer
        else:
            self._buffer = buffer
            self._owned_buffer = b""
            self._buffer_view = bytes(self._buffer)

        super().__init__(self._buffer_view, copy_buffer=False)
        self._copy_buffer = copy_buffer

    def update_view(self) -> None:
        if self._copy_buffer:
            self._owned_buffer = bytes(self._buffer)
            self._buffer_view = self._owned_buffer
        else:
            self._buffer_view = bytes(self._buffer)

    def size(self) -> int:
        return len(self._buffer)

    def reset(self) -> None:
        self._buffer.clear()
        self.update_view()
        self._read_pointer = 0
        self._has_overflowed = False

    def data(self) -> bytearray:
        return self._buffer

    def copy_buffer(self) -> bytes:
        return bytes(self._buffer)

    def get_and_release_data(self) -> bytes:
        data = bytes(self._buffer)
        self.reset()
        return data

    def _write(
        self, fmt: str, value: Union[int, float], big_endian: bool = False
    ) -> None:
        endian: Literal[">"] | Literal["<"] = ">" if big_endian else "<"
        packed = struct.pack(f"{endian}{fmt}", value)
        self._buffer.extend(packed)
        self.update_view()

    def write_bytes(self, origin: bytes, num: int) -> None:
        self._buffer.extend(origin[:num])
        self.update_view()

    def write_byte(self, value: int) -> None:
        self._write("B", value)

    def write_unsigned_char(self, value: int) -> None:
        self.write_byte(value)

    def write_unsigned_short(self, value: int) -> None:
        self._write("H", value)

    def write_unsigned_int(self, value: int) -> None:
        self._write("I", value)

    def write_unsigned_int64(self, value: int) -> None:
        self._write("Q", value)

    def write_bool(self, value: bool) -> None:
        self.write_byte(1 if value else 0)

    def write_double(self, value: float) -> None:
        self._write("d", value)

    def write_float(self, value: float) -> None:
        self._write("f", value)

    def write_signed_int(self, value: int) -> None:
        self._write("i", value)

    def write_signed_int64(self, value: int) -> None:
        self._write("q", value)

    def write_signed_short(self, value: int) -> None:
        self._write("h", value)

    def write_unsigned_varint(self, uvalue: int) -> None:
        while True:
            byte = uvalue & 0x7F
            uvalue >>= 7
            if uvalue != 0:
                byte |= 0x80
            self.write_byte(byte)
            if uvalue == 0:
                break

    def write_unsigned_varint64(self, uvalue: int) -> None:
        while True:
            byte = uvalue & 0x7F
            uvalue >>= 7
            if uvalue != 0:
                byte |= 0x80
            self.write_byte(byte)
            if uvalue == 0:
                break

    def write_varint(self, value: int) -> None:
        if value >= 0:
            self.write_unsigned_varint(2 * value)
        else:
            self.write_unsigned_varint(~(2 * value))

    def write_varint64(self, value: int) -> None:
        if value >= 0:
            self.write_unsigned_varint64(2 * value)
        else:
            self.write_unsigned_varint64(~(2 * value))

    def write_normalized_float(self, value: float) -> None:
        self.write_varint64(int(value * 2147483647.0))

    def write_signed_big_endian_int(self, value: int) -> None:
        self._write("i", value, big_endian=True)

    def write_string(self, value: str) -> None:
        data = value.encode("utf-8")
        self.write_unsigned_varint(len(data))
        self.write_bytes(data, len(data))

    def write_unsigned_int24(self, value: int) -> None:
        self.write_byte(value & 0xFF)
        self.write_byte((value >> 8) & 0xFF)
        self.write_byte((value >> 16) & 0xFF)

    def write_raw_bytes(self, raw_buffer: bytes) -> None:
        self._buffer.extend(raw_buffer)
        self.update_view()

    def write_stream(self, stream: ReadOnlyBinaryStream) -> None:
        self.write_raw_bytes(stream.get_left_buffer())
