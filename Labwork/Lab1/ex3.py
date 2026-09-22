num = int(input("Enter a number? "))


def is_prime(n: int):
    if n < 2:
        return False

    if n in (2, 3):
        return True

    if n % 2 == 0:
        return False

    for i in range(3, int(n**0.5) + 1, 2):
        if n % i:
            return False

    return True


status = " " if is_prime(num) else " NOT "

print(f"{num} is{status}a prime number")
