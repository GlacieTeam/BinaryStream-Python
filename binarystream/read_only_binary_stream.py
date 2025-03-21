from typing import Optional, Union, Literal, cast
import struct


class ReadOnlyBinaryStream:
    _buffer_view: bytes
    _read_pointer: int
    _has_overflowed: bool

    def __init__(self, buffer: bytearray = bytearray()) -> None:
        self._buffer_view = bytes(buffer)
        self._read_pointer = 0
        self._has_overflowed = False

    def _swap_endian(self, value: int, fmt: str) -> int:
        return struct.unpack(f">{fmt}", struct.pack(f"<{fmt}", value))[0]

    def _read(
        self, fmt: str, size: int, big_endian: bool = False
    ) -> Optional[Union[int, float]]:
        if self._has_overflowed:
            return None
        if self._read_pointer + size > len(self._buffer_view):
            self._has_overflowed = True
            return None
        data = self._buffer_view[self._read_pointer : self._read_pointer + size]
        self._read_pointer += size
        endian: Literal[">"] | Literal["<"] = ">" if big_endian else "<"
        try:
            value: Union[int, float] = struct.unpack(f"{endian}{fmt}", data)[0]
            return value
        except struct.error:
            return None

    def get_position(self) -> int:
        return self._read_pointer

    def get_left_buffer(self) -> bytes:
        return bytes(self._buffer_view[self._read_pointer :])

    def is_overflowed(self) -> bool:
        return self._has_overflowed

    def has_data_left(self) -> bool:
        return self._read_pointer < len(self._buffer_view)

    def get_bytes(self, target: bytearray, num: int) -> bool:
        if self._has_overflowed or self._read_pointer + num > len(self._buffer_view):
            self._has_overflowed = True
            return False
        target[:] = self._buffer_view[self._read_pointer : self._read_pointer + num]
        self._read_pointer += num
        return True

    def get_byte(self) -> int:
        return cast(int, self._read("B", 1)) or 0

    def get_unsigned_char(self) -> int:
        return self.get_byte()

    def get_unsigned_short(self) -> int:
        return cast(int, self._read("H", 2)) or 0

    def get_unsigned_int(self) -> int:
        return cast(int, self._read("I", 4)) or 0

    def get_unsigned_int64(self) -> int:
        return cast(int, self._read("Q", 8)) or 0

    def get_bool(self) -> bool:
        return bool(self.get_byte())

    def get_double(self) -> float:
        return self._read("d", 8) or 0.0

    def get_float(self) -> float:
        return self._read("f", 4) or 0.0

    def get_signed_int(self) -> int:
        return cast(int, self._read("i", 4)) or 0

    def get_signed_int64(self) -> int:
        return cast(int, self._read("q", 8)) or 0

    def get_signed_short(self) -> int:
        return cast(int, self._read("h", 2)) or 0

    def get_unsigned_varint(self) -> int:
        value = 0
        shift = 0
        while True:
            byte: int = self.get_byte()
            value |= (byte & 0x7F) << shift
            if not byte & 0x80:
                break
            shift += 7
        return value

    def get_unsigned_varint64(self) -> int:
        value = 0
        shift = 0
        while True:
            byte: int = self.get_byte()
            value |= (byte & 0x7F) << shift
            if not byte & 0x80:
                break
            shift += 7
            if shift >= 64:
                raise ValueError("VarInt too large")
        return value

    def get_varint(self) -> int:
        decoded = self.get_unsigned_varint()
        return ~(decoded >> 1) if (decoded & 1) else decoded >> 1

    def get_varint64(self) -> int:
        decoded = self.get_unsigned_varint64()
        return ~(decoded >> 1) if (decoded & 1) else decoded >> 1

    def get_normalized_float(self) -> float:
        return self.get_varint64() / 2147483647.0

    def get_signed_big_endian_int(self) -> int:
        return cast(int, self._read("i", 4, big_endian=True)) or 0

    def get_string(self) -> str:
        length: int = self.get_unsigned_varint()
        if length == 0:
            return ""
        if self._read_pointer + length > len(self._buffer_view):
            self._has_overflowed = True
            return ""
        data: bytearray = self._buffer_view[
            self._read_pointer : self._read_pointer + length
        ]
        self._read_pointer += length
        return data.decode("utf-8")

    def get_unsigned_int24(self) -> int:
        if self._read_pointer + 3 > len(self._buffer_view):
            self._has_overflowed = True
            return 0
        data: bytearray = self._buffer_view[self._read_pointer : self._read_pointer + 3]
        self._read_pointer += 3
        return int.from_bytes(data, byteorder="little", signed=False)
