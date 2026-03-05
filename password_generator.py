#!/usr/bin/env python3
"""Secure, customizable password generator.

This script uses the `secrets` module for cryptographically strong randomness
and allows the user to choose length and whether to include uppercase letters,
numbers, and symbols. A complexity check ensures that the generated password
contains at least one character from each chosen category.

Usage is interactive; it will prompt the user for input.

"""

import string
import secrets


def generate_password(length: int = 16,
                      use_upper: bool = True,
                      use_digits: bool = True,
                      use_symbols: bool = True) -> str:
    """Generate a secure password according to user-specified rules.

    Args:
        length: Desired length of the password (must be >= 1).
        use_upper: Include uppercase letters if True.
        use_digits: Include digits if True.
        use_symbols: Include punctuation/symbols if True.

    Returns:
        A string containing the generated password.

    Raises:
        ValueError: If length is less than the number of required character
            categories or if no character sets are selected.
    """

    if length < 1:
        raise ValueError("Password length must be at least 1")

    # build pools
    pools = []
    pools.append(string.ascii_lowercase)  # always include lowercase
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(string.punctuation)

    if not pools:
        raise ValueError("At least one character set must be selected.")

    if length < len(pools):
        raise ValueError(
            "Length too short to include all selected categories (need at least {} characters).".format(len(pools))
        )

    # ensure each selected category contributes at least one character
    password_chars = [secrets.choice(pool) for pool in pools]

    # fill the rest
    all_chars = ''.join(pools)
    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(all_chars))

    # shuffle to avoid predictable patterns
    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)


def main():
    print("Secure Password Generator")
    try:
        inp = input("Password length [16]: ").strip()
        length = int(inp) if inp else 16
    except ValueError:
        print("Invalid length; falling back to default of 16.")
        length = 16

    def ask_bool(prompt: str, default: bool) -> bool:
        resp = input(f"{prompt} [{'Y' if default else 'y'}/{'n' if default else 'N'}]: ").strip().lower()
        if resp == "":
            return default
        return resp[0] == "y"

    use_upper = ask_bool("Include uppercase letters?", True)
    use_digits = ask_bool("Include digits?", True)
    use_symbols = ask_bool("Include symbols?", True)

    try:
        pwd = generate_password(length, use_upper, use_digits, use_symbols)
        print("Generated password: ", pwd)
    except ValueError as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
