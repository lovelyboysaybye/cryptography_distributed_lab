import random
from ecpy.curves import Curve, Point, ECPyException


class ECCPoint:
    def __init__(self, x, y, curve_name):
        self.x = x
        self.y = y
        self.curve_name = curve_name


class ECCWrapper:
    """
    ECCWrapper class to use ECPy library
    """
    def __init__(self, curve_name):
        """
        Initializes the ECCWrapper object.
        :param curve_name: name of curve that used
        """
        self.curve_name = curve_name
        self.curve = Curve.get_curve(curve_name)

    def ec_point_gen(self, x, y):
        """
        Initializes ECCPoint with x and y on a curve.
        :param x: x of point
        :param y: y of point
        """
        return ECCPoint(x, y, self.curve_name)

    def is_on_curve_check(self, point):
        """
        Checks if point placed on Curve or not.
        :param point: Point object with x and y coordinates
        :return: True if Point on curve otherwise False
        """
        try:
            res = self.curve.is_on_curve(Point(point.x, point.y, self.curve))
        except ECPyException:
            res = False
        return res

    def add_ec_points(self, point_a, point_b):
        """
        Adds Point_A to Point_B
        :param point_a: first point
        :param point_b: second point
        :return: created after addition Point
        """
        result = self.curve.add_point(Point(point_a.x, point_a.y, self.curve), Point(point_b.x, point_b.y, self.curve))
        return ECCPoint(result.x, result.y, self.curve_name)

    def double_ec_point(self, point):
        """
        Multiplies point by 2.
        :param point: point to multiplication
        :return: new point as a result of point * 2
        """
        result = self.curve._mul_point(2, Point(point.x, point.y, self.curve))
        return ECCPoint(result.x, result.y, self.curve_name)

    def scalar_mult(self, k, point):
        """
        Multiplies point by k times
        :param point: point to multiplication on scalar
        :param k: scalar value how many time multiply point
        :return: new point as a result of point * K
        """
        result = self.curve._mul_point(k, Point(point.x, point.y, self.curve))
        return ECCPoint(result.x, result.y, self.curve_name)

    def ec_point_to_string(self, point):
        """
        Returns string representation of point.
        :param point: point to represent
        :return: str
        """
        return f"({point.x}, {point.y})"

    def string_to_ec_point(self, s):
        """
        Converts string to point.
        :param s: string representation of point
        :return: ECCPoint object of string represented point
        """
        x, y = map(int, s.strip("()").split(","))
        return ECCPoint(x, y, self.curve_name)

    def print_ec_point(self, point):
        self.ec_point_to_string(point)

    def base_point_get(self):
        """
        Returns base point of curve
        :return: Base point of curve
        """
        generator = self.curve.generator
        return ECCPoint(generator.x, generator.y, self.curve_name)

    def generate_key_pair(self, seed=3):
        """
        Generates private and public key. Private key is randomly by provided seed
        :param seed: seed for randomizer
        :return: private and public key
        """
        private_key = self.generate_private_key(seed=seed)
        public_key = self.calculate_public_key(private_key)
        return private_key, public_key

    def generate_private_key(self, seed=3):
        """
        Generates private key. Private key is randomly by provided seed
        :param seed: seed for randomizer
        :return: private
        """
        random.seed(seed)
        private_key = random.randint(1, self.curve.order - 1)
        return private_key

    def calculate_public_key(self, private_key):
        """
        Calculates the public key from private_key.
        :param private_key: private key
        :return: public key
        """
        base_point = self.curve.generator
        public_key = self.curve.mul_point(private_key, base_point)
        return ECCPoint(public_key.x, public_key.y, self.curve_name)


if __name__ == "__main__":
    # Create an instance of ECCWrapper
    wrapper = ECCWrapper("secp256r1")  # Specify the desired elliptic curve

    # Generate an EC point
    point1 = wrapper.ec_point_gen(602046282375688656758213480587526111916698976636884684818, 174050332293622031404857552280219410364023488927386650641)
    print("Generated EC Point:")
    print(f"X: {point1.x}, Y: {point1.y}, Curve: {point1.curve_name}")

    # Check if the point is on the curve
    is_on_curve = wrapper.is_on_curve_check(point1)
    print("\nIs the point on the curve?", is_on_curve)

    # Generate an EC point
    x = 0x7d550bc2384fd76a47b8b0871165395e4e4d5ab9cb4ee286d1c60d074d7d60ef
    y = 0x8cc6dd01e747ccb8bedaae6e7fb875d036ce7e4e6231b75b93993b15202829ac

    point1 = wrapper.ec_point_gen(x, y)
    print("Generated EC Point:")
    print(f"X: {point1.x}, Y: {point1.y}, Curve: {point1.curve_name}")

    # Check if the point is on the curve
    is_on_curve = wrapper.is_on_curve_check(point1)
    print("\nIs the point on the curve?", is_on_curve)

    # Get the base point on the curve
    base_point = wrapper.base_point_get()
    print("\nBase Point:")
    print(f"X: {base_point.x}, Y: {base_point.y}, Curve: {base_point.curve_name}")

    # Add two EC points
    point2 = wrapper.ec_point_gen(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
    sum_point = wrapper.add_ec_points(point1, point2)
    print("Sum of Points:")
    print(f"X: {sum_point.x}, Y: {sum_point.y}, Curve: {sum_point.curve_name}")

    # Double an EC point
    double_point = wrapper.double_ec_point(point1)
    print("\nDoubled Point:")
    print(f"X: {double_point.x}, Y: {double_point.y}, Curve: {double_point.curve_name}")

    # Perform scalar multiplication
    scalar = 3
    mult_point = wrapper.scalar_mult(scalar, point1)
    print(f"\nScalar Multiplication ({scalar} * Point):")
    print(f"X: {mult_point.x}, Y: {mult_point.y}, Curve: {mult_point.curve_name}")

    # Convert EC point to string
    point_str = wrapper.ec_point_to_string(point1)
    print("\nEC Point as String:", point_str)

    # Convert string to EC point
    converted_point = wrapper.string_to_ec_point(point_str)
    print("\nConverted EC Point:")
    print(f"X: {converted_point.x}, Y: {converted_point.y}, Curve: {converted_point.curve_name}")

    # Print an EC point
    print("\nPrint EC Point:")
    wrapper.print_ec_point(point1)

    # Generate a key pair
    private_key, public_key = wrapper.generate_key_pair()
    print("\nGenerated Key Pair:")
    print("Private Key:", private_key)
    print("Public Key:")
    print(f"X: {public_key.x}")
    print(f"Y: {public_key.y}")
    print("Curve:", public_key.curve_name)

    # Generate a private key
    private_key = wrapper.generate_private_key(seed=12345)
    print("\nGenerated Private Key:", private_key)

    # Calculate the corresponding public key
    public_key = wrapper.calculate_public_key(private_key)
    print("Calculated Public Key:")
    print(f"X: {public_key.x}")
    print(f"Y: {public_key.y}")
    print("Curve:", public_key.curve_name)
