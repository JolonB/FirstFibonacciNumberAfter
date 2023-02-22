import argparse
import sys

parser = argparse.ArgumentParser(
    prog="GetFirstFib",
    description="Find the amount of Fibonacci numbers less than a every value up to a given value",
)
parser.add_argument("max_value", type=int)
parser.add_argument("-f", "--filename", type=str)
parser.add_argument("-F", "--full_output", action="store_true")
parser.add_argument("-C", "--csv_output", action="store_true")
parser.add_argument("-O", "--oeis_output", action="store_true", help="Store in the OEIS b-file format")

def generate_fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def main(args):
    max_value = args.max_value + 1
    result = [0] * max_value

    # Start with invalid Fibonacci number
    fib_number = -1
    fib_generated_count = 0
    fib_generator = generate_fibonacci()
    for value in range(max_value):
        while fib_number < value:
            fib_number = next(fib_generator)
            fib_generated_count += 1
        result[value] = fib_generated_count

    return result


if __name__ == "__main__":
    args = parser.parse_args()

    result = main(args)

    output_stream = open(args.filename, "w") if args.filename else sys.stdout

    if not (args.csv_output or args.oeis_output or args.full_output):
        output_stream.write("{}\n".format(result))

    if args.csv_output:
        for index, first_value in enumerate(result):
            output_stream.write("{},{}\n".format(index, first_value))

    if args.oeis_output:
        for index, first_value in enumerate(result):
            output_stream.write("{} {}\n".format(index, first_value))

    if args.full_output:
        for max_value, first_value in enumerate(result):
            fibonacci_values = []
            for fib_value in generate_fibonacci():
                if fib_value >= max_value:
                    break
                fibonacci_values.append(fib_value)
            # Add the last fibonacci value
            fibonacci_values.append(fib_value)
            output_stream.write("{},{} -- {}\n".format(max_value, first_value, fibonacci_values))

    output_stream.close()
