# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from typing import Optional, Union, Literal, cast
import struct


class ReadOnlyBinaryStream:
    _owned_buffer: bytes
    _buffer_view: bytes
    _read_pointer: int
    _has_overflowed: bool

    def __init__(
        self, buffer: Union[bytes, bytearray], copy_buffer: bool = False
    ) -> None:
        if isinstance(buffer, bytearray):
            buffer = bytes(buffer)
        if copy_buffer:
            self._owned_buffer = bytes(buffer)
            self._buffer_view = self._owned_buffer
        else:
            self._owned_buffer = b""
            self._buffer_view = buffer

        self._read_pointer = 0
        self._has_overflowed = False

    def _swap_endian(self, value: int, fmt: str) -> int:
        return struct.unpack(f">{fmt}", struct.pack(f"<{fmt}", value))[0]

    def _read_bytes(self, size: int) -> Optional[bytes]:
        if self._has_overflowed:
            return None
        if self._read_pointer + size > len(self._buffer_view):
            self._has_overflowed = True
            return None

        data = self._buffer_view[self._read_pointer : self._read_pointer + size]
        self._read_pointer += size
        return data

    def _read(
        self, fmt: str, size: int, big_endian: bool = False
    ) -> Optional[Union[int, float]]:
        data = self._read_bytes(size)
        if data is None:
            return None

        endian: Literal[">"] | Literal["<"] = ">" if big_endian else "<"
        try:
            value: Union[int, float] = struct.unpack(f"{endian}{fmt}", data)[0]
            return value
        except struct.error:
            return None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ReadOnlyBinaryStream):
            return False
        return (
            self._buffer_view == other._buffer_view
            and self._read_pointer == other._read_pointer
        )

    def size(self) -> int:
        return len(self._buffer_view)

    def get_position(self) -> int:
        return self._read_pointer

    def set_position(self, value: int) -> None:
        if value > len(self._buffer_view):
            self._has_overflowed = True
        self._read_pointer = value

    def reset_position(self) -> None:
        self._read_pointer = 0
        self._has_overflowed = False

    def ignore_bytes(self, length: int) -> None:
        self.set_position(self._read_pointer + length)

    def get_left_buffer(self) -> bytes:
        return self._buffer_view[self._read_pointer :]

    def view(self) -> bytes:
        return self._buffer_view

    def copy_data(self) -> bytes:
        return bytes(self._buffer_view)

    def is_overflowed(self) -> bool:
        return self._has_overflowed

    def has_data_left(self) -> bool:
        return self._read_pointer < len(self._buffer_view)

    def get_bytes(self, target: bytearray, num: int) -> bool:
        if self._has_overflowed or self._read_pointer + num > len(self._buffer_view):
            self._has_overflowed = True
            return False

        target[:num] = self._buffer_view[self._read_pointer : self._read_pointer + num]
        self._read_pointer += num
        return True

    def get_byte(self) -> int:
        byte = self._read("B", 1)
        return cast(int, byte) if byte is not None else 0

    def get_unsigned_char(self) -> int:
        return self.get_byte()

    def get_unsigned_short(self) -> int:
        value = self._read("H", 2)
        return cast(int, value) if value is not None else 0

    def get_unsigned_int(self) -> int:
        value = self._read("I", 4)
        return cast(int, value) if value is not None else 0

    def get_unsigned_int64(self) -> int:
        value = self._read("Q", 8)
        return cast(int, value) if value is not None else 0

    def get_bool(self) -> bool:
        return bool(self.get_byte())

    def get_double(self) -> float:
        value = self._read("d", 8)
        return cast(float, value) if value is not None else 0.0

    def get_float(self) -> float:
        value = self._read("f", 4)
        return cast(float, value) if value is not None else 0.0

    def get_signed_int(self) -> int:
        value = self._read("i", 4)
        return cast(int, value) if value is not None else 0

    def get_signed_int64(self) -> int:
        value = self._read("q", 8)
        return cast(int, value) if value is not None else 0

    def get_signed_short(self) -> int:
        value = self._read("h", 2)
        return cast(int, value) if value is not None else 0

    def get_unsigned_varint(self) -> int:
        value = 0
        shift = 0
        while True:
            byte = self.get_byte()
            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
        return value

    def get_unsigned_varint64(self) -> int:
        value = 0
        shift = 0
        while True:
            byte = self.get_byte()
            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
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
        value = self._read("i", 4, big_endian=True)
        return cast(int, value) if value is not None else 0

    def get_string(self) -> str:
        length = self.get_unsigned_varint()
        if length == 0:
            return ""

        if self._read_pointer + length > len(self._buffer_view):
            self._has_overflowed = True
            return ""

        data = self._buffer_view[self._read_pointer : self._read_pointer + length]
        self._read_pointer += length
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return ""

    def get_unsigned_int24(self) -> int:
        if self._read_pointer + 3 > len(self._buffer_view):
            self._has_overflowed = True
            return 0

        data = self._buffer_view[self._read_pointer : self._read_pointer + 3]
        self._read_pointer += 3
        return int.from_bytes(data, byteorder="little", signed=False)

    def get_raw_bytes(self, length: int) -> bytes:
        if length == 0:
            return b""

        if self._read_pointer + length > len(self._buffer_view):
            self._has_overflowed = True
            return b""

        data = self._buffer_view[self._read_pointer : self._read_pointer + length]
        self._read_pointer += length
        return data
