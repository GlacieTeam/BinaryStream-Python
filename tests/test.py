from binarystream import *


def test1() -> None:
    stream = BinaryStream()
    stream.write_byte(1)
    stream.write_unsigned_char(2)
    stream.write_unsigned_short(3)
    stream.write_unsigned_int(4)
    stream.write_unsigned_int64(5)
    stream.write_bool(True)
    stream.write_double(6)
    stream.write_float(7)
    stream.write_signed_int(8)
    stream.write_signed_int64(9)
    stream.write_signed_short(10)
    stream.write_unsigned_varint(11)
    stream.write_unsigned_varint64(12)
    stream.write_varint(13)
    stream.write_varint64(14)
    stream.write_normalized_float(1.0)
    stream.write_signed_big_endian_int(16)
    stream.write_string("17")
    stream.write_unsigned_int24(18)
    hex: str = stream.get_and_release_data().hex()
    print(f"hex: {hex}")
    print(
        f"compare: {hex == "010203000400000005000000000000000100000000000018400000e0400800000009000000000000000a000b0c1a1cfeffffff0f00000010023137120000"}"
    )


def test2() -> None:
    stream = ReadOnlyBinaryStream(
        bytearray.fromhex(
            "010203000400000005000000000000000100000000000018400000e0400800000009000000000000000a000b0c1a1cfeffffff0f00000010023137120000"
        )
    )

    byte: int = stream.get_byte()
    print(f"byte: {byte} compare: {byte == 1}")

    unsignedChar: int = stream.get_unsigned_char()
    print(f"unsignedChar: {unsignedChar} compare: {unsignedChar == 2}")

    unsignedShort: int = stream.get_unsigned_short()
    print(f"unsignedShort: {unsignedShort} compare: {unsignedShort == 3}")

    unsignedInt: int = stream.get_unsigned_int()
    print(f"unsignedInt: {unsignedInt} compare: {unsignedInt == 4}")

    unsignedInt64: int = stream.get_unsigned_int64()
    print(f"unsignedInt64: {unsignedInt64} compare: {unsignedInt64 == 5}")

    bool_: bool = stream.get_bool()
    print(f"bool: {bool_} compare: {bool_ == True}")

    double: float = stream.get_double()
    print(f"double: {double} compare: {double == 6}")

    float_: float = stream.get_float()
    print(f"float: {float_} compare: {float_ == 7}")

    signedInt: int = stream.get_signed_int()
    print(f"signedInt: {signedInt} compare: {signedInt == 8}")

    signedInt64: int = stream.get_signed_int64()
    print(f"signedInt64: {signedInt64} compare: {signedInt64 == 9}")

    signedShort: int = stream.get_signed_short()
    print(f"signedShort: {signedShort} compare: {signedShort == 10}")

    unsignedVarInt: int = stream.get_unsigned_varint()
    print(f"unsignedVarInt: {unsignedVarInt} compare: {unsignedVarInt == 11}")

    unsignedVarInt64: int = stream.get_unsigned_varint64()
    print(f"unsignedVarInt64: {unsignedVarInt64} compare: {unsignedVarInt64 == 12}")

    varInt: int = stream.get_varint()
    print(f"varInt: {varInt} compare: {varInt == 13}")

    varInt64: int = stream.get_varint64()
    print(f"varInt64: {varInt64} compare: {varInt64 == 14}")

    normalizedFloat: float = stream.get_normalized_float()
    print(f"normalizedFloat: {normalizedFloat} compare: {normalizedFloat == 1.0}")

    signedBigEndianInt: int = stream.get_signed_big_endian_int()
    print(
        f"signedBigEndianInt: {signedBigEndianInt} compare: {signedBigEndianInt == 16}"
    )

    string: str = stream.get_string()
    print(f"string: {string} compare: {string == "17"}")

    unsignedInt24: int = stream.get_unsigned_int24()
    print(f"unsignedInt24: {unsignedInt24} compare: {unsignedInt24 == 18}")


def test3() -> None:
    stream = BinaryStream()
    stream.write_byte(1)
    stream.write_unsigned_char(2)
    stream.write_unsigned_short(3)
    stream.write_unsigned_int(4)
    stream.write_unsigned_int64(5)
    stream.write_bool(True)
    stream.write_double(6)
    stream.write_float(7)
    stream.write_signed_int(8)
    stream.write_signed_int64(9)
    stream.write_signed_short(10)
    stream.write_unsigned_varint(11)
    stream.write_unsigned_varint64(12)
    stream.write_varint(13)
    stream.write_varint64(14)
    stream.write_normalized_float(1.0)
    stream.write_signed_big_endian_int(16)
    stream.write_string("17")
    stream.write_unsigned_int24(18)

    byte: int = stream.get_byte()
    print(f"byte: {byte} compare: {byte == 1}")

    unsignedChar: int = stream.get_unsigned_char()
    print(f"unsignedChar: {unsignedChar} compare: {unsignedChar == 2}")

    unsignedShort: int = stream.get_unsigned_short()
    print(f"unsignedShort: {unsignedShort} compare: {unsignedShort == 3}")

    unsignedInt: int = stream.get_unsigned_int()
    print(f"unsignedInt: {unsignedInt} compare: {unsignedInt == 4}")

    unsignedInt64: int = stream.get_unsigned_int64()
    print(f"unsignedInt64: {unsignedInt64} compare: {unsignedInt64 == 5}")

    bool_: bool = stream.get_bool()
    print(f"bool: {bool_} compare: {bool_ == True}")

    double: float = stream.get_double()
    print(f"double: {double} compare: {double == 6}")

    float_: float = stream.get_float()
    print(f"float: {float_} compare: {float_ == 7}")

    signedInt: int = stream.get_signed_int()
    print(f"signedInt: {signedInt} compare: {signedInt == 8}")

    signedInt64: int = stream.get_signed_int64()
    print(f"signedInt64: {signedInt64} compare: {signedInt64 == 9}")

    signedShort: int = stream.get_signed_short()
    print(f"signedShort: {signedShort} compare: {signedShort == 10}")

    unsignedVarInt: int = stream.get_unsigned_varint()
    print(f"unsignedVarInt: {unsignedVarInt} compare: {unsignedVarInt == 11}")

    unsignedVarInt64: int = stream.get_unsigned_varint64()
    print(f"unsignedVarInt64: {unsignedVarInt64} compare: {unsignedVarInt64 == 12}")

    varInt: int = stream.get_varint()
    print(f"varInt: {varInt} compare: {varInt == 13}")

    varInt64: int = stream.get_varint64()
    print(f"varInt64: {varInt64} compare: {varInt64 == 14}")

    normalizedFloat: float = stream.get_normalized_float()
    print(f"normalizedFloat: {normalizedFloat} compare: {normalizedFloat == 1.0}")

    signedBigEndianInt: int = stream.get_signed_big_endian_int()
    print(
        f"signedBigEndianInt: {signedBigEndianInt} compare: {signedBigEndianInt == 16}"
    )

    string: str = stream.get_string()
    print(f"string: {string} compare: {string == "17"}")

    unsignedInt24: int = stream.get_unsigned_int24()
    print(f"unsignedInt24: {unsignedInt24} compare: {unsignedInt24 == 18}")


if __name__ == "__main__":
    print("-" * 25, "Test1", "-" * 25)
    test1()
    print("-" * 25, "Test2", "-" * 25)
    test2()
    print("-" * 25, "Test3", "-" * 25)
    test3()
    print("-" * 25, "End", "-" * 25)
