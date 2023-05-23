import random


class MonobitTest:
    """
    Class for monobit test
    """
    # Constants for min max values of same bits in sequence of 20000 bits (2500 bytes).
    NUM_BYTES = 2500
    MIN_VAL = 9654
    MAX_VAL = 10346
    MIN_VAL_8 = MIN_VAL / NUM_BYTES
    MAX_VAL_8 = MAX_VAL / NUM_BYTES

    @staticmethod
    def run_test(bytes_arr: bytearray) -> bool:
        """
        Testing the input bytes_arr for number of 0 and 1 in bit representation.
        :param bytes_arr: array of bytes input
        :return: True if test passed else False.
        """
        sum_of_ones = sum([byte_val.bit_count() for byte_val in bytes_arr])

        min_val = int(MonobitTest.MIN_VAL_8 * len(bytes_arr))
        max_val = int(MonobitTest.MAX_VAL_8 * len(bytes_arr))
        return min_val < sum_of_ones < max_val


def bytes_to_bits(byte_array):
    bit_array = []
    for byte in byte_array:
        bits = [int(bit) for bit in bin(byte)[2:].zfill(8)]
        bit_array.extend(bits)
    return bit_array


class MaxLengthSequenceTest:
    """
    Class for max-length sequence of same bit value test
    """
    # Max length of same bits max length
    MAX_LENGTH = 36

    @staticmethod
    def run_test(bytes_arr: bytearray) -> bool:
        """
        Testing the input bytes_arr for number of 0 and 1 in bit representation.
        :param bytes_arr: array of bytes input
        :return: True if test passed else False.
        """
        bits_array = bytes_to_bits(bytes_arr)
        max_length_seq = 0  # Maximum sequence length
        current_length = 0  # Tmp variable to save current sequence length
        previous_bit = None # Tmp variable to save previous bit value

        for bit in bits_array:
            if bit == previous_bit:
                current_length += 1
            else:
                previous_bit = bit
                current_length = 1

            if current_length > max_length_seq:
                max_length_seq = current_length

        return max_length_seq < MaxLengthSequenceTest.MAX_LENGTH


class PokerTest:
    """
    Poker test of bits sequence.
    """
    MIN_XI3 = 1.03
    MAX_XI3 = 57.4

    @staticmethod
    def run_test(bytes_arr: bytearray, m: int = 4) -> bool:
        """
        Testing the input bytes_arr for Poker test
        :param bytes_arr: array of bytes input
        :param m: length of Poker block
        :return: True if test passed else False.
        """
        bits_array = bytes_to_bits(bytes_arr)
        Y = len(bits_array)
        k = Y // m

        # Create a dictionary, where key - is a possible value of m-bits and
        # value is number of thib locks in input sequence
        possible_blocks_dict = {i: 0 for i in range(2**m)}

        for i in range(0, Y, m):
            tmp_m_block = bits_array[i:i+m]
            val = sum(jj<<ii for ii, jj in enumerate(reversed(tmp_m_block)))
            possible_blocks_dict[val] += 1

        xi3 = 2**m / k * (sum([val ** 2for val in possible_blocks_dict.values()])) - k
        return PokerTest.MIN_XI3 < xi3 < PokerTest.MAX_XI3


class SequenceLengthTest:
    """
    Test the number of sequence of ones and zeros
    """
    MAX_SEQ_VAL = 6
    MAX_KEY = "MAX"
    MIN_KEY = "MIN"
    EXPECTED_LENGHT = {1: {MIN_KEY: 2267, MAX_KEY: 2733},
                       2: {MIN_KEY: 1079, MAX_KEY: 1421},
                       3: {MIN_KEY: 502, MAX_KEY: 748},
                       4: {MIN_KEY: 223, MAX_KEY: 402},
                       5: {MIN_KEY: 90, MAX_KEY: 223},
                       6: {MIN_KEY: 90, MAX_KEY: 223}}


    @staticmethod
    def run_test(bytes_arr: bytearray) -> bool:
        """
        Testing the input bytes_arr for number of sequence of different length of 0 and 1 in bit representation.
        :param bytes_arr: array of bytes input
        :return: True if test passed else False.
        """
        bits_array = bytes_to_bits(bytes_arr)
        current_length = 1  # Tmp variable to save current sequence length
        previous_bit = None # Tmp variable to save previous bit value

        # Recalculate expected values to our length of bytes
        my_expected_length = {key: {SequenceLengthTest.MIN_KEY: int(value[SequenceLengthTest.MIN_KEY] * len(bits_array) / 10000), SequenceLengthTest.MAX_KEY: int(value[SequenceLengthTest.MAX_KEY] * len(bits_array) / 10000)} for key, value in SequenceLengthTest.EXPECTED_LENGHT.items()}
        seq_len_dict = {i: 0 for i in range(1, SequenceLengthTest.MAX_SEQ_VAL + 1)}

        for bit in bits_array:
            if bit == previous_bit:
                current_length += 1
            else:
                previous_bit = bit
                if current_length < SequenceLengthTest.MAX_SEQ_VAL:
                    seq_len_dict[current_length] += 1
                else:
                    seq_len_dict[SequenceLengthTest.MAX_SEQ_VAL] += 1

                current_length = 1

        output_flag = True
        for key_seq in seq_len_dict.keys():
            expected_min, expected_max = my_expected_length[key_seq][SequenceLengthTest.MIN_KEY], my_expected_length[key_seq][SequenceLengthTest.MAX_KEY]
            current_val = seq_len_dict[key_seq]
            if not (expected_min < current_val < expected_max):
                output_flag = False
                break
        return output_flag


if __name__ == "__main__":
    random.seed(3)

    #Test monobit
    print("1. Test monobit:")
    input_bytes = bytearray([0x01 for _ in range(1250)])
    print(f"Test array of 0x01 in hex of 1250 bytes. Res = {MonobitTest.run_test(input_bytes)}")

    input_bytes = bytearray([random.randint(0, 255) for _ in range(2500)])
    print(f"Test array of random bytes in hex of 2500 bytes. Res = {MonobitTest.run_test(input_bytes)}")

    # Max-length sequence test
    print("\n\n2. Test max-length sequence:")
    bytes_array = bytearray([random.randint(0, 255) for _ in range(2500)])  # Example byte array
    print(f"Test array of random bytes in hex of 2500 bytes. Res = {MaxLengthSequenceTest.run_test(bytes_array)}")

    bytes_array = bytearray([0xFF, 0xFF, 0xF0, 0xAA])  # Example byte array
    print(f"Test array of 0xFF, 0xFF, 0xF0, 0xAA hex. Res = {MaxLengthSequenceTest.run_test(bytes_array)}")

    bytes_array = bytearray([0xFF for _ in range(100)])  # Example byte array
    print(f"Test array of 100 bytes of 0xFF hex. Res = {MaxLengthSequenceTest.run_test(bytes_array)}")

    # Poker test
    print("\n\n3. Poker test:")
    bytes_array = bytearray([random.randint(0, 255) for _ in range(2500)])  # Example byte array
    print(f"Test array of random bytes in hex of 2500 bytes. Res = {PokerTest.run_test(bytes_array)}")

    bytes_array = bytearray([0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00])  # Example byte array
    print(f"Test array of 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00 hex. Res = {PokerTest.run_test(bytes_array)}")

    # Poker test
    print("\n\n4. Sequence length test:")
    bytes_array = bytearray([random.randint(0, 255) for _ in range(2500)])  # Example byte array
    print(f"Test array of random bytes in hex of 2500 bytes. Res = {SequenceLengthTest.run_test(bytes_array)}")

    bytes_array = bytearray([0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00])  # Example byte array
    print(f"Test array of 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00 hex. Res = {SequenceLengthTest.run_test(bytes_array)}")
