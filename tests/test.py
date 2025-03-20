from binarystream import *


def test1() -> None:
    stream = BinaryStream()
    stream.writeByte(1)
    stream.writeUnsignedChar(2)
    stream.writeUnsignedShort(3)
    stream.writeUnsignedInt(4)
    stream.writeUnsignedInt64(5)
    stream.writeBool(True)
    stream.writeDouble(6)
    stream.writeFloat(7)
    stream.writeSignedInt(8)
    stream.writeSignedInt64(9)
    stream.writeSignedShort(10)
    stream.writeUnsignedVarInt(11)
    stream.writeUnsignedVarInt64(12)
    stream.writeVarInt(13)
    stream.writeVarInt64(14)
    stream.writeNormalizedFloat(1.0)
    stream.writeSignedBigEndianInt(16)
    stream.writeString("17")
    stream.writeUnsignedInt24(18)
    hex: str = stream.getAndReleaseData().hex()
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

    byte: int = stream.getByte()
    print(f"byte: {byte} compare: {byte == 1}")

    unsignedChar: int = stream.getUnsignedChar()
    print(f"unsignedChar: {unsignedChar} compare: {unsignedChar == 2}")

    unsignedShort: int = stream.getUnsignedShort()
    print(f"unsignedShort: {unsignedShort} compare: {unsignedShort == 3}")

    unsignedInt: int = stream.getUnsignedInt()
    print(f"unsignedInt: {unsignedInt} compare: {unsignedInt == 4}")

    unsignedInt64: int = stream.getUnsignedInt64()
    print(f"unsignedInt64: {unsignedInt64} compare: {unsignedInt64 == 5}")

    bool_: bool = stream.getBool()
    print(f"bool: {bool_} compare: {bool_ == True}")

    double: float = stream.getDouble()
    print(f"double: {double} compare: {double == 6}")

    float_: float = stream.getFloat()
    print(f"float: {float_} compare: {float_ == 7}")

    signedInt: int = stream.getSignedInt()
    print(f"signedInt: {signedInt} compare: {signedInt == 8}")

    signedInt64: int = stream.getSignedInt64()
    print(f"signedInt64: {signedInt64} compare: {signedInt64 == 9}")

    signedShort: int = stream.getSignedShort()
    print(f"signedShort: {signedShort} compare: {signedShort == 10}")

    unsignedVarInt: int = stream.getUnsignedVarInt()
    print(f"unsignedVarInt: {unsignedVarInt} compare: {unsignedVarInt == 11}")

    unsignedVarInt64: int = stream.getUnsignedVarInt64()
    print(f"unsignedVarInt64: {unsignedVarInt64} compare: {unsignedVarInt64 == 12}")

    varInt: int = stream.getVarInt()
    print(f"varInt: {varInt} compare: {varInt == 13}")

    varInt64: int = stream.getVarInt64()
    print(f"varInt64: {varInt64} compare: {varInt64 == 14}")

    normalizedFloat: float = stream.getNormalizedFloat()
    print(f"normalizedFloat: {normalizedFloat} compare: {normalizedFloat == 1.0}")

    signedBigEndianInt: int = stream.getSignedBigEndianInt()
    print(
        f"signedBigEndianInt: {signedBigEndianInt} compare: {signedBigEndianInt == 16}"
    )

    string: str = stream.getString()
    print(f"string: {string} compare: {string == "17"}")

    unsignedInt24: int = stream.getUnsignedInt24()
    print(f"unsignedInt24: {unsignedInt24} compare: {unsignedInt24 == 18}")


if __name__ == "__main__":
    print("-" * 25, "Test1", "-" * 25)
    test1()
    print("-" * 25, "Test2", "-" * 25)
    test2()
    print("-" * 25, "End", "-" * 25)
