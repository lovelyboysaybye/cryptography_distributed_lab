import Cryptodome.Util.number as num
import random
from task5_hash.main import SHA1


class ElGamelSignature:
    """
    Class for ElGamel signature.
    """
    P_CONST = 602334574490710843
    G_CONST = 72757217426062278

    def __init__(self, p, g) -> None:
        """
        Initializes a ElGamelSignature object with p and g values.
        :param p: prime number
        :param g: primitive
        """
        self.p = p
        self.g = g

    @staticmethod
    def generate_prime_and_primitive_root(bit_length=2048) -> (int, int):
        """
        Function for generating p and g values for specified number of bits.
        :param bit_length: bit length for p value for generation
        :return (p, g)
        """
        p = 4
        while not num.isPrime(p):
            tmp_p = num.getPrime(bit_length)
            p = 2 * tmp_p + 1

        g = random.randint(2, p - 1)
        while (p - 1) % g == 1:
            g = random.randint(2, p - 1)

        return p, g

    def get_private_public_keys(self, seed=1) -> (int, int):
        """
        Generates a private key in range(1; p-1) and calculates a public key as pub_key = g**priv_key mod p.
        :param seed: seed for random
        :return: (priv_key, pub_key) private and public keys
        """

        # Set seed for generation random values
        random.seed(seed)

        # Generate random private key
        #   Range to p-2 to not generate a p-1 value
        priv_key = random.randint(1, self.p - 2)

        # Calculate a public key from the private key, p, and g values.
        pub_key = pow(self.g, priv_key, self.p)

        return priv_key, pub_key

    def sign(self, priv_key, message) -> (int, int):
        """
        Generates a signature for message by private key, p and g.
        :param priv_key: private key
        :param message: message to sign
        :return: (r, s) first and second components of signature
        """
        while 1:
            k = random.randint(1,self. p - 2)
            if ElGamelSignature.GCD(k, self.p - 1) == 1:
                break

        r = pow(self.g, k, self.p)
        l = ElGamelSignature.inverse(k, self.p - 1)
        s = l * (message - priv_key * r) % (self.p - 1)
        return r, s

    def signVerif(self, pub_key, r, s, message) -> bool:
        """
        Verifies a signature (r, s) value of specified message by pub_key.
        :param pub_key: public key of user, who sign message.
        :param r: first component of signature
        :param s: second component of signature
        :return: valid signature - True, otherwise False
        """
        if r < 1 or r > self.p - 1:
            return False
        v1 = pow(pub_key, r, self.p) % self.p * pow(r, s, self.p) % self.p
        v2 = pow(self.g, message, self.p)
        return v1 == v2

    @staticmethod
    def GCD(x, y):
        """
        Generates Greates Common Denominator of x and y
        """
        x = abs(x)
        y = abs(y)
        while x > 0:
            x, y = y % x, x
        return y

    @staticmethod
    def inverse(u, v):
        """
        Calculates inverse for u and v.
        """

        if v == 0:
            raise ZeroDivisionError("Modulus cannot be zero")
        if v < 0:
            raise ValueError("Modulus cannot be negative")

        u3, v3 = u, v
        u1, v1 = 1, 0
        while v3 > 0:
            q = u3 // v3
            u1, v1 = v1, u1 - v1 * q
            u3, v3 = v3, u3 - v3 * q
        if u3 != 1:
            raise ValueError("No inverse value can be computed")
        while u1 < 0:
            u1 = u1 + v
        return u1


class ElGamalEncryption:
    """
    Class for ElGamal encryption.
    """
    # The P and G should be >> then int value for encryption (bigger then chunk_size)
    P_CONST = 90439
    G_CONST = 52627

    def __init__(self, p, g) -> None:
        """
        Initializes an ElGamalEncryption object with p and g values.
        :param p: prime number
        :param g: primitive root
        """
        self.p = p
        self.g = g

    def get_private_public_keys(self, seed=1) -> (int, int):
        """
        Generates a private key in range(1; p-1) and calculates a public key as pub_key = g**priv_key mod p.
        :param seed: seed for random
        :return: (priv_key, pub_key) private and public keys
        """

        # Set seed for generation random values
        random.seed(seed)

        # Generate random private key
        #   Range to p-2 to not generate a p-1 value
        priv_key = random.randint(1, self.p - 2)

        # Calculate a public key from the private key, p, and g values.
        pub_key = pow(self.g, priv_key, self.p)

        return priv_key, pub_key

    def encrypt(self, pub_key, message, chunk_size=2) -> [(int, int)]:
        """
        Encrypts a message using the public key.
        :param pub_key: public key
        :param message: message to encrypt
        :return: (c1, c2) encrypted components
        """
        output = []
        for mess_str in ElGamalEncryption.divide_chunks(message, chunk_size):
            mess_val = ElGamalEncryption.str_to_val(mess_str)
            k = random.randint(1, self.p - 2)
            c1 = pow(self.g, k, self.p)
            c2 = (pow(pub_key, k, self.p) * mess_val) % self.p
            output.append((c1, c2))

        return output

    def decrypt(self, priv_key, c1_c2_arr, chunk_size=2) -> str:
        """
        Decrypts an encrypted message using the private key.
        :param priv_key: private key
        :param c1: first component of the encryption
        :param c2: second component of the encryption
        :return: decrypted message
        """
        output = ""
        for c1,c2 in c1_c2_arr:
            s = pow(c1, priv_key, self.p)
            s_inverse = self.inverse(s, self.p)
            decrypted_int = (c2 * s_inverse) % self.p
            decrypted_str = ElGamalEncryption.val_to_str(decrypted_int, chunk_size)
            output += decrypted_str
        return output

    def encrypt_whole(self, pub_key, message, chunk_size=4) -> [(int, int)]:
        """
        Encrypts a message using the public key.
        :param pub_key: public key
        :param message: message to encrypt
        :return: (c1, c2) encrypted components
        """

        k = random.randint(1, self.p - 2)
        c1 = pow(self.g, k, self.p)
        c2 = (pow(pub_key, k, self.p) * message) % self.p

        return (c1, c2)

    def decrypt_whole(self, priv_key, c1, c2, chunk_size=4) -> int:
        """
        Decrypts an encrypted message using the private key.
        :param priv_key: private key
        :param c1: first component of the encryption
        :param c2: second component of the encryption
        :return: decrypted message
        """
        s = pow(c1, priv_key, self.p)
        s_inverse = num.inverse(s, self.p)
        decrypted_int = (c2 * s_inverse) % self.p
        return decrypted_int

    @staticmethod
    def str_to_val(string) -> int:
        """
        Converts string message as int ASCII representation, and concatenates it to one int value of string_len-bytes.
        :param string: ASCII string
        :return: int value of the string
        """
        ascii_values = [ord(letter) for letter in string]
        result = 0
        for ascii_value in ascii_values:
            result = (result << 8) | ascii_value
        return result

    @staticmethod
    def val_to_str(val, chunk_size) -> str:
        """
        Converts int value of string to ASCII representation and retrieves the original string.
        :param val: int value of string
        :param chunk_size: length of the original string
        :return: the original string
        """
        ascii_values = []
        for _ in range(chunk_size):
            ascii_values.append(val & 0xFF)
            val >>= 8
        ascii_values.reverse()
        ascii_string = ''.join(chr(ascii_value) for ascii_value in ascii_values)
        return ascii_string

    @staticmethod
    def divide_chunks(arr, chunk_size) -> []:
        """
        Divides array on a chunk sizes. Padded with zeros, if needed.
        :param arr: list of element
        :param chunk_size: chunk size
        """
        arr = list(arr)  # Convert the input to a list
        pad_len = len(arr) % chunk_size
        if pad_len != 0:
            arr += ['\x00'] * (chunk_size - pad_len)

        for i in range(0, len(arr), chunk_size):
            yield arr[i:i + chunk_size]

    @staticmethod
    def inverse(u, v):
        """
        Calculates inverse for u and v.
        """

        if v == 0:
            raise ZeroDivisionError("Modulus cannot be zero")
        if v < 0:
            raise ValueError("Modulus cannot be negative")

        u3, v3 = u, v
        u1, v1 = 1, 0
        while v3 > 0:
            q = u3 // v3
            u1, v1 = v1, u1 - v1 * q
            u3, v3 = v3, u3 - v3 * q
        if u3 != 1:
            raise ValueError("No inverse value can be computed")
        while u1 < 0:
            u1 = u1 + v
        return u1


if __name__ == "__main__":
    print("Verify string to int convertion (and backwards)")
    inp_str = "hello"
    val = ElGamalEncryption.str_to_val(inp_str)
    res = ElGamalEncryption.val_to_str(val, len(inp_str))
    print(f"Original str: {inp_str}; Converted: {val}; Encrypted: {res}")

    print("\nI. ElGamelSignature")
    message = "Distribution lab the best!"

    # Use my SHA1 implementation to calculate hash of message!
    my_sha = SHA1()

    hash_val = int(my_sha.get_hash(message.encode('ascii')), 16)

    p = ElGamelSignature.P_CONST
    g = ElGamelSignature.G_CONST
    # Or can generate P and G values, but requires to long time to find prime.
    # p, g = ElGamelSignature.generate_prime_and_primitive_root()

    elgamel_obj = ElGamelSignature(p, g)

    priv_key, pub_key = elgamel_obj.get_private_public_keys()
    print(f"Private key: {priv_key}; Public key: {pub_key}")

    r, s = elgamel_obj.sign(priv_key, hash_val)

    print("\n 1. Test: original priv_key, original pub_key, original message")
    sign_valid = elgamel_obj.signVerif(pub_key, r, s, hash_val)
    print(f"Verify validation for original pub_key and message: {sign_valid}")

    wrong_hash = hash_val + 1
    print(f"\n 2. Test: original priv_key, original pub_key, another message:\n\tOriginal message={hash_val}\n\tUpdated message={wrong_hash}")
    sign_valid = elgamel_obj.signVerif(pub_key, r, s, wrong_hash)
    print(f"Verify validation for original pub_key, but another message: {sign_valid}")

    r, s = elgamel_obj.sign(priv_key + 6, hash_val)
    print(f"\n 3. Test: another priv_key, original pub_key (not that calculates from the current priv_key), orig message:")
    sign_valid = elgamel_obj.signVerif(pub_key, r, s, hash_val)
    print(f"Verify validation for wrong pub_key (another priv_key used): {sign_valid}")

    print("\n\nII. ElGamelEncryption")
    message = "Distribution lab the best!"

    p = ElGamalEncryption.P_CONST
    g = ElGamalEncryption.G_CONST
    # Or can generate P and G values, but requires to long time to find prime.
    # p, g = ElGamelSignature.generate_prime_and_primitive_root()

    elgamel_obj = ElGamalEncryption(p, g)

    priv_key, pub_key = elgamel_obj.get_private_public_keys()
    print(f"Private key: {priv_key}; Public key: {pub_key}")

    mess = 12345
    print(f"Original message: {mess}")

    encrypted_text_c1, encrypted_text_c2 = elgamel_obj.encrypt_whole(pub_key, mess)
    print(f"Encrypted message (two components): ({encrypted_text_c1}, {encrypted_text_c2})")

    decrypted_text = elgamel_obj.decrypt_whole(priv_key, encrypted_text_c1, encrypted_text_c2)
    print(f"Encrypted message: {decrypted_text}")

    print(f"Does original message equal to encrypted {mess == decrypted_text}")

    print(f"\n\n1. Test: Encrypt and decrypt by original priv and pub key pairs\nOriginal message: {message}")

    encrypted_text_c1_c2 = elgamel_obj.encrypt(pub_key, message)
    print(f"Encrypted message (two components): {encrypted_text_c1_c2}")

    decrypted_text = elgamel_obj.decrypt(priv_key, encrypted_text_c1_c2)
    print(f"Encrypted message: {decrypted_text}")

    print(f"Does original message equal to encrypted {message == decrypted_text}")

    print(f"\n\n2. Test: Encrypt by original priv and pub key pairs, but try to encrypt by another priv key\nOriginal message: {message}")

    encrypted_text_c1_c2 = elgamel_obj.encrypt(pub_key, message)
    print(f"Encrypted message (two components): {encrypted_text_c1_c2}")

    wrong_priv_key = priv_key + 10
    print(f"Orig priv key: {priv_key}; Wrong priv_key: {wrong_priv_key}")
    decrypted_text = elgamel_obj.decrypt(wrong_priv_key, encrypted_text_c1_c2)
    print(f"Encrypted message: {decrypted_text}")

    print(f"Does original message equal to encrypted {message == decrypted_text}")

    message = "Distribution lab the best!" * 1000
    print(f"\n\n3. Test: Encrypt and decrypt by original priv and pub key pairs\nOriginal message: {message}")

    encrypted_text_c1_c2 = elgamel_obj.encrypt(pub_key, message)
    print(f"Encrypted message (two components): {encrypted_text_c1_c2}")

    decrypted_text = elgamel_obj.decrypt(priv_key, encrypted_text_c1_c2)
    print(f"Encrypted message: {decrypted_text}")

    print(f"Does original message equal to encrypted {message == decrypted_text}")
