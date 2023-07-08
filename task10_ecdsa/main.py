from task5_hash.main import SHA1
from task8.main import ECCWrapper, ECCPoint


class ECDSA:
    """
    Class of ECDSA (Elliptic Curve Digital Signature Algorithm) implementation.
    """

    def __init__(self, curve_name: str) -> None:
        """
        Initializes of ECDSA object.
        :param curve_name: name of curve that used
        """
        self.curve_name = curve_name
        self.ecc_wrapper = ECCWrapper(curve_name)
        self.sha1 = SHA1()

    def generate_key_pair(self, seed=1) -> (int, ECCPoint):
        """
        Generates private and public keys.
        :param seed: seed for random
        :return: int private key and ECCPoint as public key (x, y coordinates)
        """
        private_key, public_key = self.ecc_wrapper.generate_key_pair(seed=seed)
        return private_key, public_key

    def sign_message(self, private_key: int, message: str) -> (int, int):
        """
        Signs message (hash of the message).
        :param private_key: int of private key
        :param message: string message to sign
        :return: r and s parts of signature
        """
        hash_value = self.sha1.get_hash(message.encode())
        signature = self._ecdsa_sign(int(private_key), hash_value)
        return signature

    def verify_signature(self, public_key: ECCPoint, message: str, signature: (int, int)) -> bool:
        """
        Verifies signature of the message by r and s value and public key.
        :param public_key: public key of user who sign the message
        :param message: string of message (will calculate hash from it)
        :param signature: r and s value of signature
        :return: True of False whether the signature are correct or not
        """
        recalculated_hash_value = self.sha1.get_hash(message.encode())
        return self._ecdsa_verify(public_key, int(recalculated_hash_value, 16), signature)

    def _ecdsa_sign(self, private_key: int, hash_value: str) -> (int, int):
        """
        Sign function.
        :param private_key: private key for signing
        :param hash_value: strin hash value
        :return: r and s
        """
        # Generate random value that is not bigger than curve order
        k = self.ecc_wrapper.generate_private_key()
        r = 0
        s = 0

        while r == 0 or s == 0:
            point = self.ecc_wrapper.scalar_mult(k, self.ecc_wrapper.base_point_get())
            r = point.x % self.ecc_wrapper.curve.order
            s = ((int(hash_value, 16) + r * private_key) * self._mod_inverse(k, self.ecc_wrapper.curve.order)) % self.ecc_wrapper.curve.order

        return r, s

    def _ecdsa_verify(self, public_key: ECCPoint, hash_value: str, signature: (int, int)) -> bool:
        """
        Verify function.
        :param public_key: public key
        :param hash_value: string of hash value
        :signature: r and s of signature
        :return: True of False whether the signature are correct or not
        """
        r, s = signature
        w = self._mod_inverse(s, self.ecc_wrapper.curve.order)
        u1 = (hash_value * w) % self.ecc_wrapper.curve.order
        u2 = (r * w) % self.ecc_wrapper.curve.order

        point1 = self.ecc_wrapper.scalar_mult(u1, self.ecc_wrapper.base_point_get())
        point2 = self.ecc_wrapper.scalar_mult(u2, public_key)
        point = self.ecc_wrapper.add_ec_points(point1, point2)

        return point.x % self.ecc_wrapper.curve.order == r

    def _mod_inverse(self, a, m):
        """
        Mod calculation
        """
        if a == 0:
            raise ZeroDivisionError("Inverse does not exist.")
        if a < 0:
            a = m - (-a % m)
        t, new_t = 0, 1
        r, new_r = m, a

        while new_r != 0:
            quotient = r // new_r
            t, new_t = new_t, t - quotient * new_t
            r, new_r = new_r, r - quotient * new_r

        if r > 1:
            raise ValueError("a is not invertible.")
        if t < 0:
            t += m

        return t


if __name__ == "__main__":
    curve_name = "secp256k1"
    ecdsa = ECDSA(curve_name)

    # Генерація ключів
    print("1. Generate key pair: ")
    private_key, public_key = ecdsa.generate_key_pair(seed=1)
    print("Private Key:", private_key)
    print("Public Key:", ecdsa.ecc_wrapper.ec_point_to_string(public_key))

    # Підпис повідомлення
    message = "Hello, world!"
    print(f"\nMessage for signing: {message}")
    signature = ecdsa.sign_message(private_key, message)
    print("Signature:", signature)

    # Перевірка підпису повідомлення
    verified = ecdsa.verify_signature(public_key, message, signature)
    print("Signature Verified:", verified)

    # Перевірка підпису повідомлення
    wrong_message = message + " HELLO ME!"
    print(f"\nTry to verify signature of another message: {wrong_message}")
    verified = ecdsa.verify_signature(public_key, wrong_message, signature)
    print("Signature Verified:", verified)

    print("\n2. Generate key pair: ")
    private_key1, public_key2 = ecdsa.generate_key_pair(seed=2)
    print("Private Key:", private_key)
    print("Public Key:", ecdsa.ecc_wrapper.ec_point_to_string(public_key2))

    print(f"\nTry to verify signature of message by providing another public key")
    verified = ecdsa.verify_signature(public_key2, message, signature)
    print("Signature Verified:", verified)
