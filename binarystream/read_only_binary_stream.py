# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from typing import Optional, Union, Literal, cast
import struct


class ReadOnlyBinaryStream:
    """Provides read-only access to a binary data stream.

    This class implements various methods for reading primitive data types,
    variable-length integers, strings, and raw bytes from a binary stream.
    """

    _owned_buffer: bytes
    _buffer_view: bytes
    _read_pointer: int
    _has_overflowed: bool

    def __init__(
        self, buffer: Union[bytes, bytearray], copy_buffer: bool = False
    ) -> None:
        """Initializes a read-only binary stream.

        Args:
            buffer: The binary data to read from
            copy_buffer: Whether to create a copy of the input buffer
        """
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
        """Compares two streams for equality.

        Returns:
            True if both streams have identical buffers and read positions
        """
        if not isinstance(other, ReadOnlyBinaryStream):
            return False
        return (
            self._buffer_view == other._buffer_view
            and self._read_pointer == other._read_pointer
        )

    def size(self) -> int:
        """Gets the total size of the buffer.

        Returns:
            The total number of bytes in the stream
        """
        return len(self._buffer_view)

    def get_position(self) -> int:
        """Gets the current read position.

        Returns:
            The current position in the stream
        """
        return self._read_pointer

    def set_position(self, value: int) -> None:
        """Sets the current read position.

        Args:
            value: The new read position
        """
        if value > len(self._buffer_view):
            self._has_overflowed = True
        self._read_pointer = value

    def reset_position(self) -> None:
        """Resets the read position to the start of the stream."""
        self._read_pointer = 0
        self._has_overflowed = False

    def ignore_bytes(self, length: int) -> None:
        """Advances the read position by the specified number of bytes.

        Args:
            length: Number of bytes to skip
        """
        self.set_position(self._read_pointer + length)

    def get_left_buffer(self) -> bytes:
        """Gets the remaining unread portion of the buffer.

        Returns:
            The unread bytes from current position to end
        """
        return self._buffer_view[self._read_pointer :]

    def copy_data(self) -> bytes:
        """Creates a copy of the entire buffer.

        Returns:
            A copy of the buffer data
        """
        return bytes(self._buffer_view)

    def is_overflowed(self) -> bool:
        """Checks if the stream has overflowed.

        Returns:
            True if an overflow error occurred during reading
        """
        return self._has_overflowed

    def has_data_left(self) -> bool:
        """Checks if there is unread data remaining.

        Returns:
            True if there is more data to read
        """
        return self._read_pointer < len(self._buffer_view)

    def get_byte(self) -> int:
        """Reads a single byte from the stream.

        Returns:
            The byte value (0-255)
        """
        byte = self._read("B", 1)
        return cast(int, byte) if byte is not None else 0

    def get_unsigned_char(self) -> int:
        """Reads an unsigned char (1 byte).

        Returns:
            The byte value (0-255)
        """
        return self.get_byte()

    def get_unsigned_short(self) -> int:
        """Reads an unsigned short (2 bytes, little-endian).

        Returns:
            The 16-bit unsigned integer value
        """
        value = self._read("H", 2)
        return cast(int, value) if value is not None else 0

    def get_unsigned_int(self) -> int:
        """Reads an unsigned int (4 bytes, little-endian).

        Returns:
            The 32-bit unsigned integer value
        """
        value = self._read("I", 4)
        return cast(int, value) if value is not None else 0

    def get_unsigned_int64(self) -> int:
        """Reads an unsigned 64-bit integer (8 bytes, little-endian).

        Returns:
            The 64-bit unsigned integer value
        """
        value = self._read("Q", 8)
        return cast(int, value) if value is not None else 0

    def get_bool(self) -> bool:
        """Reads a boolean value (1 byte).

        Returns:
            True if byte is non-zero, False otherwise
        """
        return bool(self.get_byte())

    def get_double(self) -> float:
        """Reads a double-precision floating point number (8 bytes).

        Returns:
            The double value
        """
        value = self._read("d", 8)
        return cast(float, value) if value is not None else 0.0

    def get_float(self) -> float:
        """Reads a single-precision floating point number (4 bytes).

        Returns:
            The float value
        """
        value = self._read("f", 4)
        return cast(float, value) if value is not None else 0.0

    def get_signed_int(self) -> int:
        """Reads a signed int (4 bytes, little-endian).

        Returns:
            The 32-bit signed integer value
        """
        value = self._read("i", 4)
        return cast(int, value) if value is not None else 0

    def get_signed_int64(self) -> int:
        """Reads a signed 64-bit integer (8 bytes, little-endian).

        Returns:
            The 64-bit signed integer value
        """
        value = self._read("q", 8)
        return cast(int, value) if value is not None else 0

    def get_signed_short(self) -> int:
        """Reads a signed short (2 bytes, little-endian).

        Returns:
            The 16-bit signed integer value
        """
        value = self._read("h", 2)
        return cast(int, value) if value is not None else 0

    def get_unsigned_varint(self) -> int:
        """Reads an unsigned variable-length integer (1-5 bytes, little-endian).

        Returns:
            The decoded unsigned integer value
        """
        value = 0
        shift = 0
        while True:
            byte = self.get_byte()
            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
            if shift >= 64:
                break
        return value

    def get_unsigned_varint64(self) -> int:
        """Reads an unsigned 64-bit variable-length integer (1-10 bytes, little-endian).

        Returns:
            The decoded 64-bit unsigned integer value
        """
        value = 0
        shift = 0
        while True:
            byte = self.get_byte()
            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
            if shift >= 64:
                break
        return value

    def get_unsigned_big_varint(self) -> int:
        """Reads an unsigned big variable-length integer (little-endian).

        Returns:
            The decoded big unsigned integer value
        """
        value = 0
        shift = 0
        while True:
            byte = self.get_byte()
            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
        return value

    def get_varint(self) -> int:
        """Reads a signed variable-length integer (1-5 bytes, little-endian).

        Returns:
            The decoded signed integer value
        """
        decoded = self.get_unsigned_varint()
        return ~(decoded >> 1) if (decoded & 1) else decoded >> 1

    def get_varint64(self) -> int:
        """Reads a signed 64-bit variable-length integer (1-10 bytes, little-endian).

        Returns:
            The decoded 64-bit signed integer value
        """
        decoded = self.get_unsigned_varint64()
        return ~(decoded >> 1) if (decoded & 1) else decoded >> 1

    def get_big_varint(self) -> int:
        """Reads a signed big variable-length integer (little-endian).

        Returns:
            The decoded big signed integer value
        """
        decoded = self.get_unsigned_big_varint()
        return ~(decoded >> 1) if (decoded & 1) else decoded >> 1

    def get_normalized_float(self) -> float:
        """Reads a normalized float value.

        Returns:
            Float value normalized between -1.0 and 1.0
        """
        return self.get_varint64() / 2147483647.0

    def get_signed_big_endian_int(self) -> int:
        """Reads a big-endian signed integer (4 bytes).

        Returns:
            The 32-bit signed integer value
        """
        value = self._read("i", 4, big_endian=True)
        return cast(int, value) if value is not None else 0

    def get_raw_bytes(self, length: int) -> bytes:
        """Reads raw bytes from the stream.

        Args:
            length: Number of bytes to read

        Returns:
            The raw bytes read from the stream
        """
        if length == 0:
            return b""
        if self._read_pointer + length > len(self._buffer_view):
            self._has_overflowed = True
            return b""
        data = self._buffer_view[self._read_pointer : self._read_pointer + length]
        self._read_pointer += length
        return data

    def get_bytes(self) -> bytes:
        """Reads a raw bytes.

        Returns:
            The raw bytes value
        """
        length = self.get_unsigned_varint()
        return self.get_raw_bytes(length)

    def get_string(self) -> str:
        """Reads a UTF-8 encoded string.

        The string is prefixed with its length as a varint.

        Returns:
            The decoded UTF-8 string
        """
        data = self.get_bytes()
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return ""

    def get_unsigned_int24(self) -> int:
        """Reads a 24-bit unsigned integer (3 bytes, little-endian).

        Returns:
            The 24-bit unsigned integer value
        """
        if self._read_pointer + 3 > len(self._buffer_view):
            self._has_overflowed = True
            return 0
        data = self._buffer_view[self._read_pointer : self._read_pointer + 3]
        self._read_pointer += 3
        return int.from_bytes(data, byteorder="little", signed=False)
