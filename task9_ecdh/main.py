from task8.main import ECCWrapper, ECCPoint


class ECDH_user:
    """
    Implementation of ECDH based on my own ECCWrapper class.
    """
    def __init__(self, priv_key: int, pub_key: ECCPoint, ecc_wrapper: ECCWrapper) -> None:
        """
        Initializes ECDH for user.
        :param priv_key: private key of user
        :param pub_key: public key of user
        :param curve: used curve
        """
        self.priv_key = priv_key
        self.pub_key = pub_key
        self.ecc_wrapper = ecc_wrapper
        self.external_pub_key = None

    def add_external_pub_key(self, pub_key: ECCPoint) -> None:
        """
        Adds external public key of user with whom required to create secret.
        :param pub_key: public key of another user
        """
        self.external_pub_key = pub_key

    def calc_secret(self) -> int:
        """
        Calculates secret based on priv_key and external_pub_ley.
        :return: X coordinate as resulted secret
        """
        secret = self.ecc_wrapper.scalar_mult(self.priv_key, self.external_pub_key)
        return secret.x


if __name__ == "__main__":
    # Create an instance of ECCWrapper
    wrapper = ECCWrapper("secp256r1")  # Specify the desired elliptic curve

    # User 1
    priv_key_user_1, pub_key_user_1 = wrapper.generate_key_pair(seed=1)
    print("Generated Key Pair for User1:")
    print(f"Private Key: {priv_key_user_1}")
    print("Public Key:")
    wrapper.print_ec_point(pub_key_user_1)

    ecdh_user1 = ECDH_user(priv_key_user_1, pub_key_user_1, wrapper)

    # User 2
    priv_key_user_2, pub_key_user_2 = wrapper.generate_key_pair(seed=2)
    print("\nGenerated Key Pair for User2:")
    print(f"Private Key: {priv_key_user_2}")
    print("Public Key:")
    wrapper.print_ec_point(pub_key_user_2)

    ecdh_user2 = ECDH_user(priv_key_user_2, pub_key_user_2, wrapper)

    # Share public key with each other
    ecdh_user1.add_external_pub_key(pub_key_user_2)
    ecdh_user2.add_external_pub_key(pub_key_user_1)

    # Each of users calculate the secret
    user_secret1 = ecdh_user1.calc_secret()
    user_secret2 = ecdh_user2.calc_secret()

    # Verify secrets
    print(f"\nUser1 calculated secret: {user_secret1}")
    print(f"User2 calculated secret: {user_secret2}")
    print(f"Does secret equals? {user_secret1 == user_secret2}")

    # User 3
    priv_key_user_3, pub_key_user_3 = wrapper.generate_key_pair(seed=3)
    print("\nGenerated Key Pair for User3:")
    print(f"Private Key: {priv_key_user_3}")
    print("Public Key:")
    wrapper.print_ec_point(pub_key_user_3)

    ecdh_user3 = ECDH_user(priv_key_user_3, pub_key_user_3, wrapper)

    print("\n Let's try to generate secret with User1 and verify, that it would not equal to calculated secret with User2")
    ecdh_user3.add_external_pub_key(pub_key_user_1)

    user_secret3 = ecdh_user3.calc_secret()
    # Verify secrets
    print(f"\nUser1 calculated secret: {user_secret1}")
    print(f"User3 calculated secret: {user_secret3}")
    print(f"Does secret equals? {user_secret1 == user_secret3}")
    print("User3 cannot calculated the same secret as User1, because it requires the User2 private key!")
