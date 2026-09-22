string = input("Enter a string: ")

def remove_dollar_sign(s: str) -> str: 
    return s.replace("$", "")


print(remove_dollar_sign(string))
