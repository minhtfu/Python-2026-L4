int_list = [1, 4, 5, -1, 10]


def extract_even(l: list[int]):
    return [i for i in l if i & 1 == 0]

print(extract_even(int_list))


