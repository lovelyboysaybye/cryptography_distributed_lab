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
    MAX_BYTE_VAL = 16

    def __init__(self, base: Base = Base.BASE_32, endian_type: EndianType = EndianType.BIG_ENDIAN_TYPE, hex_repr: str = None):
        self.base_size = base
        self.endian_type = endian_type
        self.bytes = [0] * self.base_size
        if hex_repr:
            self.setHex(hex_repr)

    def getHex(self):
        hex_repr = ""
        for bytes_idx in range(0, self.base_size):
            hex_byte_repr = hex(self.bytes[bytes_idx])[2:]
            if len(hex_byte_repr) % 2 == 1:
                hex_byte_repr = "0" + hex_byte_repr
            hex_repr += hex_byte_repr

        if self.endian_type == EndianType.LITTLE_ENDIAN_TYPE:
            hex_repr = BigInt.hex_to_little_endian(hex_repr)
        return hex_repr

    def setHex(self, hex_repr: str):
        if self.endian_type == EndianType.LITTLE_ENDIAN_TYPE:
            hex_repr = BigInt.hex_to_little_endian(hex_repr)

        for bytes_idx in range(0, self.base_size):
            self.bytes[bytes_idx] = int(hex_repr[bytes_idx * 2:bytes_idx * 2 + 2], base=16)

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
        result = BigInt(base=self.base_size, endian_type=self.endian_type)
        for bytes_idx in range(0, self.base_size):
            result.bytes[bytes_idx] = self.bytes[bytes_idx] & other.bytes[bytes_idx]

        return result

    def __or__(self, other):
        result = BigInt(base=self.base_size, endian_type=self.endian_type)
        for bytes_idx in range(0, self.base_size):
            result.bytes[bytes_idx] = self.bytes[bytes_idx] | other.bytes[bytes_idx]

        return result

    def __xor__(self, other):
        result = BigInt(base=self.base_size, endian_type=self.endian_type)
        for bytes_idx in range(0, self.base_size):
            result.bytes[bytes_idx] = self.bytes[bytes_idx] ^ other.bytes[bytes_idx]

        return result

    def __invert__(self):
        result = BigInt(base=self.base_size, endian_type=self.endian_type)
        for bytes_idx in range(0, self.base_size):
            result.bytes[bytes_idx] = BigInt.MAX_BYTE_VAL - self.bytes[bytes_idx]

        return result

    def __lshift__(self, other):
        result = BigInt(base=self.base_size, endian_type=self.endian_type)
        byte_shifts, bit_shifts = divmod(other, 8)

        for i in range(0, self.base_size - byte_shifts):
            shifted_byte = self.bytes[i + byte_shifts] << bit_shifts
            if i + byte_shifts + 1 < self.base_size and bit_shifts > 0:
                shifted_byte |= self.bytes[i + byte_shifts + 1] >> (8 - bit_shifts)
            result.bytes[i] = shifted_byte

        return result

    def __rshift__(self, other):
        result = BigInt(base=self.base_size, endian_type=self.endian_type)
        byte_shifts, bit_shifts = divmod(other, 8)

        for i in range(byte_shifts, self.base_size):
            shifted_byte = self.bytes[i - byte_shifts] >> bit_shifts
            if i - byte_shifts - 1 >= 0 and bit_shifts > 0:
                shifted_byte |= self.bytes[i - byte_shifts - 1] << (8 - bit_shifts)
            result.bytes[i] = shifted_byte

        return result

    def __add__(self, other):
        result = BigInt(base=self.base_size, endian_type=self.endian_type)
        carry = 0
        for i in range(self.base_size - 1, -1, -1):
            byte_sum = self.bytes[i] + other.bytes[i] + carry
            result.bytes[i] = byte_sum % 256
            carry = byte_sum // 256
        return result

    def __sub__(self, other):
        result = BigInt(base=self.base_size, endian_type=self.endian_type)
        borrow = 0
        for i in range(self.base_size - 1, -1, -1):
            byte_diff = self.bytes[i] - other.bytes[i] - borrow
            if byte_diff < 0:
                byte_diff += 256
                borrow = 1
            else:
                borrow = 0
            result.bytes[i] = byte_diff
        return result

    def __mul__(self, other: "BigInt") -> "BigInt":
        result = BigInt(base=self.base_size * 2, endian_type=self.endian_type)

        # Create a temporary buffer to store intermediate results
        buffer = [0] * (2 * self.base_size)

        # Perform long multiplication digit by digit
        for i in range(self.base_size):
            for j in range(self.base_size):
                product = self.bytes[i] * other.bytes[j]
                buffer[i + j] += product
                buffer[i + j + 1] += buffer[i + j] // 256
                buffer[i + j] %= 256

        # Reduce the buffer modulo 256 and store it in the result
        carry = 0
        for i in range(2 * self.base_size - 1, -1, -1):
            carry *= 256
            carry += buffer[i]
            result.bytes[i] = carry % 256
            carry //= 256

        return result

    def __le__(self, other):
        result = True
        for i in range(self.base_size):
            if self.bytes[i] > other.bytes[i]:
                result = False
        return result


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


def test_mul(input_hex_repr_1, input_hex_repr_2, expected, endian_type, base):
    b1 = BigInt(hex_repr=input_hex_repr_1, endian_type=endian_type, base=base)
    b2 = BigInt(hex_repr=input_hex_repr_2, endian_type=endian_type, base=base)
    result = b1 * b2
    assert result.getHex() == expected, f"Error for {input_hex_repr_1} * {input_hex_repr_2}. Output is {result.getHex()}"


if __name__ == "__main__":
    # Hex tests
    test_set_get_hex("0100000000000000000000000000000000000000000000000000000000000000", EndianType.BIG_ENDIAN_TYPE)
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
            "0f10101010101010101010101010101010101010101010101010101010101010", EndianType.LITTLE_ENDIAN_TYPE,
            base=Base.BASE_32)
    test_inv("0f10101010101010101010101010101010101010101010101010101010101010",
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
                "0080000000000000000000000000000000000000000000000000000000000000",
                1, EndianType.BIG_ENDIAN_TYPE, Base.BASE_32)
    test_rshift("0100000000000000000000000000000000000000000000000000000000000000",
                "0040000000000000000000000000000000000000000000000000000000000000",
                2, EndianType.BIG_ENDIAN_TYPE, Base.BASE_32)

    # Add operator
    test_add("0100000000000000000000000000000000000000000000000000000000000000",
            "2600000000000000000000000000000000000000000000000000000000000000",
            "2700000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE,
            base=Base.BASE_32)

    test_add("0100000000000000000000000000000000000000000000000000000000000000",
            "2600000000000000000000000000000000000000000000000000000000000000",
            "2700000000000000000000000000000000000000000000000000000000000000", EndianType.LITTLE_ENDIAN_TYPE,
            base=Base.BASE_32)

    test_add("36f028580bb02cc8272a9a020f4200e346e276ae664e45ee80745574e2f5ab80",
            "70983d692f648185febe6d6fa607630ae68649f7e6fc45b94680096c06e4fadb",
            "a78865c13b14ae4e25e90771b54963ee2d68c0a64d4a8ba7c6f45ee0e9daa65b", EndianType.BIG_ENDIAN_TYPE,
            base=Base.BASE_32)

    # Sub operator
    test_sub("33ced2c76b26cae94e162c4c0d2c0ff7c13094b0185a3c122e732d5ba77efebc",
            "22e962951cb6cd2ce279ab0e2095825c141d48ef3ca9dabf253e38760b57fe03",
            "10e570324e6ffdbc6b9c813dec968d9bad134bc0dbb061530934f4e59c2700b9", EndianType.BIG_ENDIAN_TYPE,
            base=Base.BASE_32)

    test_mul("0000000000000000000000000000000000000000000000000000000000000002",
             "0000000000000000000000000000000000000000000000000000000000000002",
             "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400", EndianType.BIG_ENDIAN_TYPE,
            base=Base.BASE_32)

