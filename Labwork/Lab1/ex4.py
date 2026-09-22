num = int(input("Enter a number? "))


def is_perfect(n):
    if n <= 1:
        return False

    divisors_sum = sum(i for i in range(1, (n // 2) + 1) if n % i == 0)

    return divisors_sum == n


status = " " if is_perfect(num) else " NOT "

print(f"{num} is a{status}perfect number")
