num = int(input("Enter a number: "))

divisors = []

if num > 0:
    for i in range(1, int(num**0.5) + 1):
        if num % i == 0:
            divisors.append(i)

            if i != num // i:
                divisors.append(num // i)

print(f"Divisors: {divisors}")
