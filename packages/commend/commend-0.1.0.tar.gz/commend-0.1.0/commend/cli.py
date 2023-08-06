#!/usr/bin/env python3

import argparse


class Validator(object):
    def __init__(self):
        # Derived classes should define type_name and call parent init.
        if not getattr(self, "error_name", None):
            self.error_message = f"invalid {self.type_name} value"

    def validate(self, value):
        # Derived classes should return value if valid.
        raise NotImplementedError

    def __call__(self, value):
        try:
            if self.validate(value):
                return value
            else:
                raise ValueError
        except ValueError:
            raise argparse.ArgumentTypeError(f"{self.error_message}: '{value}'")


class PositiveInteger(Validator):
    def __init__(self):
        self.type_name = "positive integer"
        super().__init__()

    def validate(self, value):
        if int(value) >= 1:
            return value


class PositiveFloat(Validator):
    def __init__(self):
        self.type_name = "positive float"
        self.error_message = "fancy error message"
        super().__init__()

    def validate(self, value):
        if float(value) > 0.0:
            return value


def get_args():
    parser = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    parser.add_argument("--help", action="help")
    parser.add_argument("--retry", type=PositiveInteger(), default=1)
    parser.add_argument("--timeout", type=PositiveFloat(), default=30)
    args, command = parser.parse_known_args()
    return (args, command)


def main():
    args, command = get_args()
    print(args)
    print(command)


if __name__ == "__main__":
    main()
