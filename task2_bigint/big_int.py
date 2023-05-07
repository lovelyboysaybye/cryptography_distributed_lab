from __future__ import annotations
from enum import Enum, IntEnum


class EndianType(Enum):
    """
    Static class with types of endians.
    """
    LITTLE_ENDIAN_TYPE = 1
    BIG_ENDIAN_TYPE = 2


class Base(IntEnum):
    """
    Static class with types of endians.
    """
    BASE_32 = 32
    BASE_64 = 64


class BigInt:
    def __init__(self, base: Base = Base.BASE_32, endian_type: EndianType = EndianType.BIG_ENDIAN_TYPE, hex_repr: str = None):
        self.base_size = base
        self.endian_type = endian_type
        self.value = 0
        if hex_repr:
            self.setHex(hex_repr)

    def getHex(self):
        hex_repr = hex(self.value)[2:]

        if self.endian_type == EndianType.LITTLE_ENDIAN_TYPE:
            hex_repr = BigInt.hex_to_little_endian(hex_repr)
        hex_len = len(hex_repr)
        if hex_len % 2 == 1:
            hex_repr = "0" + hex_repr
            hex_len += 1
        hex_repr += "00" * (self.base_size - len(hex_repr) // 2)
        return hex_repr

    def setHex(self, hex_repr: str):
        if self.endian_type == EndianType.LITTLE_ENDIAN_TYPE:
            hex_repr = BigInt.hex_to_little_endian(hex_repr)

        self.value = int(hex_repr, base=16)

    @staticmethod
    def hex_to_little_endian(hex_repr: str) -> str:
        """
        Converts hex_representation from BIG ENDIAN to LITTLE ENDIAN.
        :param hex_repr: str hex representation
        :return: little endian hex representation
        """
        return "".join([hex_repr[x:x+2] for x in range(0,len(hex_repr),2)][::-1])

    def __str__(self):
        return self.getHex()

    def __repr__(self):
        return self.__str__()

    def __and__(self, other):
        return BigInt(base=self.base_size, endian_type=self.endian_type, hex_repr=hex(self.value & other.value)[2:])

    def __or__(self, other):
        return BigInt(base=self.base_size, endian_type=self.endian_type, hex_repr=hex(self.value | other.value)[2:])

    def __xor__(self, other):
        return BigInt(base=self.base_size, endian_type=self.endian_type, hex_repr=hex(self.value ^ other.value)[2:])

    def __invert__(self):
        value_mask = (1 << self.base_size * 8) - 1
        inverted = (~self.value) & value_mask
        hex_repr = hex(inverted)[2:].zfill(self.base_size * 2)
        if self.endian_type == EndianType.LITTLE_ENDIAN_TYPE:
            hex_repr = BigInt.hex_to_little_endian(hex_repr)
        return BigInt(base=self.base_size, endian_type=self.endian_type, hex_repr=hex_repr)

    def __lshift__(self, other):
        return BigInt(base=self.base_size, endian_type=self.endian_type, hex_repr=hex(self.value << other)[2:])

    def __rshift__(self, other):
        return BigInt(base=self.base_size, endian_type=self.endian_type, hex_repr=hex(self.value >> other)[2:])

    def __add__(self, other):
        return BigInt(base=self.base_size, endian_type=self.endian_type, hex_repr=hex(self.value + other.value)[2:])

    def __sub__(self, other):
        return BigInt(base=self.base_size, endian_type=self.endian_type, hex_repr=hex(self.value - other.value)[2:])


def test_set_get_hex(input_hex_repr, endian_type):
    b = BigInt(hex_repr=input_hex_repr, endian_type=endian_type)
    print(f"Endian: {endian_type}; Input \"{input_hex_repr}\"; Output: \"{b.getHex()}\"")
    assert b.getHex() == input_hex_repr, f"Error for {input_hex_repr}. Output is {b.getHex()}"


def test_and(input_hex_repr_1, input_hex_repr_2, expected, endian_type, base):
    b1 = BigInt(hex_repr=input_hex_repr_1, endian_type=endian_type, base=base)
    b2 = BigInt(hex_repr=input_hex_repr_2, endian_type=endian_type, base=base)
    result = b1 & b2
    assert result.getHex() == expected, f"Error for {input_hex_repr_1} & {input_hex_repr_2}. Output is {result.getHex()}"


def test_or(input_hex_repr_1, input_hex_repr_2, expected, endian_type, base):
    b1 = BigInt(hex_repr=input_hex_repr_1, endian_type=endian_type, base=base)
    b2 = BigInt(hex_repr=input_hex_repr_2, endian_type=endian_type, base=base)
    result = b1 | b2
    assert result.getHex() == expected, f"Error for {input_hex_repr_1} | {input_hex_repr_2}. Output is {result.getHex()}"


def test_xor(input_hex_repr_1, input_hex_repr_2, expected, endian_type, base):
    b1 = BigInt(hex_repr=input_hex_repr_1, endian_type=endian_type, base=base)
    b2 = BigInt(hex_repr=input_hex_repr_2, endian_type=endian_type, base=base)
    result = b1 ^ b2

    assert result.getHex() == expected, f"Error for {input_hex_repr_1} ^ {input_hex_repr_2}. Output is {result.getHex()}"


def test_inv(input_hex_repr, expected, endian_type, base):
    b = BigInt(hex_repr=input_hex_repr, endian_type=endian_type, base=base)
    result = ~b
    assert result.getHex() == expected, f"Error for ~{input_hex_repr}. Output is {result.getHex()}"


def test_lshift(input_hex_repr, expected, shift, endian_type, base):
    b = BigInt(hex_repr=input_hex_repr, endian_type=endian_type, base=base)
    result = b << shift
    assert result.getHex() == expected, f"Error for {input_hex_repr} << {shift}. Output is {result.getHex()}"


def test_rshift(input_hex_repr, expected, shift, endian_type, base):
    b = BigInt(hex_repr=input_hex_repr, endian_type=endian_type, base=base)
    result = b >> shift
    assert result.getHex() == expected, f"Error for {input_hex_repr} >> {shift}. Output is {result.getHex()}"


def test_add(input_hex_repr_1, input_hex_repr_2, expected, endian_type, base):
    b1 = BigInt(hex_repr=input_hex_repr_1, endian_type=endian_type, base=base)
    b2 = BigInt(hex_repr=input_hex_repr_2, endian_type=endian_type, base=base)
    result = b1 + b2
    assert result.getHex() == expected, f"Error for {input_hex_repr_1} + {input_hex_repr_2}. Output is {result.getHex()}"


def test_sub(input_hex_repr_1, input_hex_repr_2, expected, endian_type, base):
    b1 = BigInt(hex_repr=input_hex_repr_1, endian_type=endian_type, base=base)
    b2 = BigInt(hex_repr=input_hex_repr_2, endian_type=endian_type, base=base)
    result = b1 - b2
    assert result.getHex() == expected, f"Error for {input_hex_repr_1} - {input_hex_repr_2}. Output is {result.getHex()}"


if __name__ == "__main__":
    # Hex tests
    test_set_get_hex("0100000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE)

    test_set_get_hex("ff00000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE)
    test_set_get_hex("ff00000000000000000000000000000000000000000000000000000000000000", EndianType.BIG_ENDIAN_TYPE)

    test_set_get_hex("ffaa000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE)
    test_set_get_hex("ffaa000000000000000000000000000000000000000000000000000000000000", EndianType.BIG_ENDIAN_TYPE)

    # And operation
    test_and("0100000000000000000000000000000000000000000000000000000000000000", "0100000000000000000000000000000000000000000000000000000000000000", "0100000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE, base=Base.BASE_32)
    test_and("0100000000000000000000000000000000000000000000000000000000000000", "0200000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE, base=Base.BASE_32)

    # Or operation
    test_or("0100000000000000000000000000000000000000000000000000000000000000", "0100000000000000000000000000000000000000000000000000000000000000", "0100000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE, base=Base.BASE_32)
    test_or("0100000000000000000000000000000000000000000000000000000000000000", "0200000000000000000000000000000000000000000000000000000000000000", "0300000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE, base=Base.BASE_32)

    # Xor operation
    test_xor("51bf608414ad5726a3c1bec098f77b1b54ffb2787f8d528a74c1d7fde6470ea4",
            "403db8ad88a3932a0b7e8189aed9eeffb8121dfac05c3512fdb396dd73f6331c",
            "1182d8299c0ec40ca8bf3f49362e95e4ecedaf82bfd167988972412095b13db8", EndianType.BIG_ENDIAN_TYPE,
            base=Base.BASE_32)

    test_xor("0100000000000000000000000000000000000000000000000000000000000000",
            "0100000000000000000000000000000000000000000000000000000000000000",
            "0000000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE,
            base=Base.BASE_32)
    test_xor("0100000000000000000000000000000000000000000000000000000000000000",
            "2600000000000000000000000000000000000000000000000000000000000000",
            "2700000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE,
            base=Base.BASE_32)

    # Invert operation
    test_inv("0100000000000000000000000000000000000000000000000000000000000000",
            "feffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", EndianType.LITTLE_ENDIAN_TYPE,
            base=Base.BASE_32)
    test_inv("feffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            "0100000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE,
            base=Base.BASE_32)

    # LShift operation
    test_lshift("0100000000000000000000000000000000000000000000000000000000000000",
                "0200000000000000000000000000000000000000000000000000000000000000",
                1, EndianType.BIG_ENDIAN_TYPE, Base.BASE_32)
    test_lshift("0100000000000000000000000000000000000000000000000000000000000000",
                "0400000000000000000000000000000000000000000000000000000000000000",
                2, EndianType.BIG_ENDIAN_TYPE, Base.BASE_32)

    # RShift operation
    test_rshift("0100000000000000000000000000000000000000000000000000000000000000",
                "8000000000000000000000000000000000000000000000000000000000000000",
                1, EndianType.BIG_ENDIAN_TYPE, Base.BASE_32)
    test_rshift("0100000000000000000000000000000000000000000000000000000000000000",
                "4000000000000000000000000000000000000000000000000000000000000000",
                2, EndianType.BIG_ENDIAN_TYPE, Base.BASE_32)

    test_add("0100000000000000000000000000000000000000000000000000000000000000",
            "2600000000000000000000000000000000000000000000000000000000000000",
            "2700000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE,
            base=Base.BASE_32)

    test_add("0100000000000000000000000000000000000000000000000000000000000000",
            "2600000000000000000000000000000000000000000000000000000000000000",
            "2700000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE,
            base=Base.BASE_32)

    test_sub("2600000000000000000000000000000000000000000000000000000000000000",
            "0100000000000000000000000000000000000000000000000000000000000000",
            "2500000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE,
            base=Base.BASE_32)