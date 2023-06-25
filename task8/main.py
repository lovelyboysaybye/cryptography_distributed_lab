from ecpy.curves import Curve, Point, ECPyException


class ECCPoint:
    def __init__(self, x, y, curve_name):
        self.x = x
        self.y = y
        self.curve_name = curve_name


class ECCWrapper:
    def __init__(self, curve_name):
        self.curve_name = curve_name
        self.curve = Curve.get_curve(curve_name)

    def ec_point_gen(self, x, y):
        return ECCPoint(x, y, self.curve_name)

    def get_y_coordinate(self, x_coordinate):
        try:
            # Create a point object with the x-coordinate
            point = Point(x_coordinate, self.curve(x_coordinate), self.curve)
            # Check if the point is on the curve
            if not self.curve.is_on_curve(point):
                raise ECPyException("The point is not on the curve.")
            # Return the y-coordinate of the point
            return point.y
        except ECPyException as e:
            print(f"Error: {str(e)}")
            return None

    def is_on_curve_check(self, point):
        try:
            res = self.curve.is_on_curve(Point(point.x, point.y, self.curve))
        except ECPyException:
            res = False
        return res

    def add_ec_points(self, point_a, point_b):
        result = self.curve.add_point(Point(point_a.x, point_a.y, self.curve), Point(point_b.x, point_b.y, self.curve))
        return ECCPoint(result.x, result.y, self.curve_name)

    def double_ec_point(self, point):
        result = self.curve._mul_point(2, Point(point.x, point.y, self.curve))
        return ECCPoint(result.x, result.y, self.curve_name)

    def scalar_mult(self, k, point):
        result = self.curve._mul_point(k, Point(point.x, point.y, self.curve))
        return ECCPoint(result.x, result.y, self.curve_name)

    def ec_point_to_string(self, point):
        return f"({point.x}, {point.y})"

    def string_to_ec_point(self, s):
        x, y = map(int, s.strip("()").split(","))
        return ECCPoint(x, y, self.curve_name)

    def print_ec_point(self, point):
        print(f"({point.x}, {point.y})")

    def base_point_get(self):
        generator = self.curve.generator
        return ECCPoint(generator.x, generator.y, self.curve_name)


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
