import math


def ex1():
    rad = int(input("Enter circle radius? "))
    area = rad**2 * math.pi
    print(area)


def ex2():
    celsius = int(input("Enter the temperature in Celsius? "))
    fah = float(celsius * (9 / 5)) + 32.0

    print(f"{celsius} (C) = {fah} (F)")


def ex3():
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


def ex4():
    num = int(input("Enter a number? "))

    def is_perfect(n):
        if n <= 1:
            return False

        divisors_sum = sum(i for i in range(1, (n // 2) + 1) if n % i == 0)

        return divisors_sum == n

    status = " " if is_perfect(num) else " NOT "

    print(f"{num} is a{status}perfect number")


def ex5():
    color_list = ["red", "blue", "green"]
    color_pick = input("What is your favourite color? ")

    index = -1
    for i, color in enumerate(color_list):
        if color_pick.lower() == color:
            index = i
            break

    if index >= 0:
        print(f"Your colod is at index {index} in my list")
    else:
        print("Sorry, I could not find your color")


def ex6():
    def range1():
        for i in range(0, 7):
            print(i)

    def range2():
        for i in range(1, 11, 3):
            print(i)

    def range3():
        for i in range(5, 0, -1):
            print(i)

    def range4():
        for i in range(6, -3, -2):
            print(i)

    range4()


def ex7():
    string = input("Enter a string: ")

    def remove_dollar_sign(s: str) -> str:
        return s.replace("$", "")

    print(remove_dollar_sign(string))


def ex8():
    int_list = [1, 4, 5, -1, 10]

    def extract_even(l: list[int]):
        return [i for i in l if i & 1 == 0]

    print(extract_even(int_list))


def ex9():
    num = int(input("Enter a number: "))

    factorial = 1
    for i in range(1, num + 1):
        factorial *= i

    print(factorial)


def ex10():
    num = int(input("Enter a number: "))

    divisors = []

    if num > 0:
        for i in range(1, int(num**0.5) + 1):
            if num % i == 0:
                divisors.append(i)

                if i != num // i:
                    divisors.append(num // i)

    print(f"Divisors: {divisors}")


def ex11():
    x1, y1 = 2, 4
    x2, y2 = 6, 8

    print(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)


def ex12():
    def print_pattern(m: int, n: int):
        for i in range(m):
            for j in range(n):
                if i == 0 or i == m - 1 or j == 0 or j == n - 1:
                    print("*", end=" ")
                else:
                    print(" ", end=" ")
            print()

    print_pattern(6, 9)

def main():
    ex1()

if __name__ == "__main__":
    main()
