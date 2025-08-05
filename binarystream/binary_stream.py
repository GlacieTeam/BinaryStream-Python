# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from binarystream.read_only_binary_stream import ReadOnlyBinaryStream
from typing import Union, Literal
import struct


class BinaryStream(ReadOnlyBinaryStream):
    """Provides read/write access to a binary data stream.

    This class extends ReadOnlyBinaryStream with methods for writing
    various data types to the stream.
    """

    _buffer: bytearray

    def __init__(
        self, buffer: Union[bytearray, bytes] = bytearray(), copy_buffer: bool = False
    ) -> None:
        """Initializes a binary stream.

        Args:
            buffer: The buffer to read from/write to
            copy_buffer: Whether to create a copy of the input buffer
        """
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

    def _update_view(self) -> None:
        if self._copy_buffer:
            self._owned_buffer = bytes(self._buffer)
            self._buffer_view = self._owned_buffer
        else:
            self._buffer_view = bytes(self._buffer)

    def _write(
        self, fmt: str, value: Union[int, float], big_endian: bool = False
    ) -> None:
        endian: Literal[">"] | Literal["<"] = ">" if big_endian else "<"
        packed = struct.pack(f"{endian}{fmt}", value)
        self._buffer.extend(packed)
        self._update_view()

    def size(self) -> int:
        """Gets the current size of the mutable buffer.

        Returns:
            Number of bytes in the stream buffer
        """
        return len(self._buffer)

    def reset(self) -> None:
        """Clears the stream buffer and resets read state."""
        self._buffer.clear()
        self._update_view()
        self._read_pointer = 0
        self._has_overflowed = False

    def data(self) -> bytearray:
        """Gets direct access to the mutable byte buffer.

        Returns:
            The underlying bytearray containing stream data
        """
        return self._buffer

    def copy_buffer(self) -> bytes:
        """Gets direct access to the mutable byte buffer.

        Returns:
            The underlying bytearray containing stream data
        """
        return bytes(self._buffer)

    def get_and_release_data(self) -> bytes:
        """Retrieves and clears the current buffer contents.

        Returns:
            Current stream data as bytes
        """
        data = bytes(self._buffer)
        self.reset()
        return data

    def write_byte(self, value: int) -> None:
        """Writes a single byte to the stream.

        Args:
            value: Byte value to write (0-255)
        """
        self._write("B", value)

    def write_unsigned_char(self, value: int) -> None:
        """Writes an unsigned char (1 byte).

        Args:
            value: Byte value to write (0-255)
        """
        self.write_byte(value)

    def write_unsigned_short(self, value: int) -> None:
        """Writes an unsigned short (2 bytes, little-endian).

        Args:
            value: 16-bit unsigned integer to write
        """
        self._write("H", value)

    def write_unsigned_int(self, value: int) -> None:
        """Writes an unsigned int (4 bytes, little-endian).

        Args:
            value: 32-bit unsigned integer to write
        """
        self._write("I", value)

    def write_unsigned_int64(self, value: int) -> None:
        """Writes an unsigned 64-bit integer (8 bytes, little-endian).

        Args:
            value: 64-bit unsigned integer to write
        """
        self._write("Q", value)

    def write_bool(self, value: bool) -> None:
        """Writes a boolean value (1 byte).

        Args:
            value: Boolean value to write
        """
        self.write_byte(1 if value else 0)

    def write_double(self, value: float) -> None:
        """Writes a double-precision floating point number (8 bytes).

        Args:
            value: Double value to write
        """
        self._write("d", value)

    def write_float(self, value: float) -> None:
        """Writes a single-precision floating point number (4 bytes).

        Args:
            value: Float value to write
        """
        self._write("f", value)

    def write_signed_int(self, value: int) -> None:
        """Writes a signed int (4 bytes, little-endian).

        Args:
            value: 32-bit signed integer to write
        """
        self._write("i", value)

    def write_signed_int64(self, value: int) -> None:
        """Writes a signed 64-bit integer (8 bytes, little-endian).

        Args:
            value: 64-bit signed integer to write
        """
        self._write("q", value)

    def write_signed_short(self, value: int) -> None:
        """Writes a signed short (2 bytes, little-endian).

        Args:
            value: 16-bit signed integer to write
        """
        self._write("h", value)

    def write_unsigned_varint(self, uvalue: int) -> None:
        """Writes an unsigned variable-length integer (1-5 bytes, little-endian).

        Args:
            uvalue: Unsigned integer value to write
        """
        uvalue &= 0xFFFFFFFF
        while True:
            byte = uvalue & 0x7F
            uvalue >>= 7
            if uvalue != 0:
                byte |= 0x80
            self.write_byte(byte)
            if uvalue == 0:
                break

    def write_unsigned_varint64(self, uvalue: int) -> None:
        """Writes an unsigned 64-bit variable-length integer (1-10 bytes, little-endian).

        Args:
            uvalue: 64-bit unsigned integer to write
        """
        uvalue &= 0xFFFFFFFFFFFFFFFF
        while True:
            byte = uvalue & 0x7F
            uvalue >>= 7
            if uvalue != 0:
                byte |= 0x80
            self.write_byte(byte)
            if uvalue == 0:
                break

    def write_unsigned_big_varint(self, uvalue: int) -> None:
        """Writes an unsigned big variable-length integer (little-endian).

        Args:
            uvalue: Unsigned big integer value to write
        """
        while True:
            byte = uvalue & 0x7F
            uvalue >>= 7
            if uvalue != 0:
                byte |= 0x80
            self.write_byte(byte)
            if uvalue == 0:
                break

    def write_varint(self, value: int) -> None:
        """Writes a signed variable-length integer (1-5 bytes, little-endian).

        Args:
            value: Signed integer value to write
        """
        if value >= 0:
            self.write_unsigned_varint(2 * value)
        else:
            self.write_unsigned_varint(~(2 * value))

    def write_varint64(self, value: int) -> None:
        """Writes a signed 64-bit variable-length integer (1-10 bytes, little-endian).

        Args:
            value: 64-bit signed integer to write
        """
        if value >= 0:
            self.write_unsigned_varint64(2 * value)
        else:
            self.write_unsigned_varint64(~(2 * value))

    def write_big_varint(self, value: int) -> None:
        """Writes a signed big variable-length integer (1-5 bytes, little-endian).

        Args:
            value: Signed big integer value to write
        """
        if value >= 0:
            self.write_unsigned_varint(2 * value)
        else:
            self.write_unsigned_varint(~(2 * value))

    def write_normalized_float(self, value: float) -> None:
        """Writes a normalized float value.

        Args:
            value: Float value to write (should be normalized between -1.0 and 1.0)
        """
        self.write_varint64(int(value * 2147483647.0))

    def write_signed_big_endian_int(self, value: int) -> None:
        """Writes a big-endian signed integer (4 bytes).

        Args:
            value: 32-bit signed integer to write
        """
        self._write("i", value, big_endian=True)

    def write_raw_bytes(self, raw_buffer: bytes) -> None:
        """Writes raw bytes to the stream.

        Args:
            raw_buffer: Byte data to write
        """
        self._buffer.extend(raw_buffer)
        self._update_view()

    def write_bytes(self, value: bytes) -> None:
        """Writes raw bytes.

        Args:
            raw_buffer: Byte data to write
        """
        self.write_unsigned_varint(len(value))
        self.write_raw_bytes(value)

    def write_string(self, value: str) -> None:
        """Writes a UTF-8 string.

        Args:
            value: String to write
        """
        data = value.encode("utf-8")
        self.write_bytes(data)

    def write_unsigned_int24(self, value: int) -> None:
        """Writes a 24-bit unsigned integer (3 bytes, little-endian).

        Args:
            value: 24-bit unsigned integer to write
        """
        self.write_byte(value & 0xFF)
        self.write_byte((value >> 8) & 0xFF)
        self.write_byte((value >> 16) & 0xFF)

    def write_stream(self, stream: ReadOnlyBinaryStream) -> None:
        """Writes all remaining data from another stream.

        Args:
            stream: Source stream to copy data from
        """
        self.write_raw_bytes(stream.get_left_buffer())
