from .read_only_binary_stream import ReadOnlyBinaryStream
from typing import Union, Literal
from io import BytesIO
import struct


class BinaryStream(ReadOnlyBinaryStream):
    _write_buffer: BytesIO

    def __init__(
        self,
        buffer: Union[bytearray, bytes, BytesIO] = bytearray(),
        copy_buffer: bool = True,
    ) -> None:
        self._write_buffer = BytesIO()

        if isinstance(buffer, (bytes, bytearray)):
            self._write_buffer.write(buffer)
        elif isinstance(buffer, BytesIO):
            self._write_buffer = buffer
        super().__init__(self._write_buffer.getvalue(), copy_buffer=False)
        self._copy_buffer = copy_buffer

    def _update_view(self) -> None:
        self._buffer = self._write_buffer.getvalue()
        if self._copy_buffer:
            self._owned_buffer = bytes(self._buffer)
            self._buffer = self._owned_buffer

    def size(self) -> int:
        return len(self._write_buffer.getvalue())

    def reserve(self, size: int) -> None:
        if size > self._write_buffer.getbuffer().nbytes:
            self._write_buffer.getbuffer().release()
            data = self._write_buffer.getvalue()
            self._write_buffer = BytesIO()
            self._write_buffer.write(data)
            self._write_buffer.getbuffer().release()

    def reset(self) -> None:
        self._write_buffer = BytesIO()
        self._read_pointer = 0
        self._has_overflowed = False
        self._update_view()

    def data(self) -> bytes:
        return self._write_buffer.getvalue()

    def copy_buffer(self) -> bytes:
        return bytes(self._write_buffer.getvalue())

    def get_and_release_data(self) -> bytes:
        data = self._write_buffer.getvalue()
        self.reset()
        return data

    def _write(
        self, fmt: str, value: Union[int, float], big_endian: bool = False
    ) -> None:
        endian: Literal[">"] | Literal["<"] = ">" if big_endian else "<"
        packed = struct.pack(f"{endian}{fmt}", value)
        self._write_buffer.write(packed)
        self._update_view()

    def write_bytes(self, origin: bytes, num: int) -> None:
        self._write_buffer.write(origin[:num])
        self._update_view()

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
        self._write_buffer.write(raw_buffer)
        self._update_view()

    def write_stream(self, stream: ReadOnlyBinaryStream) -> None:
        self.write_raw_bytes(stream.get_left_buffer())
