import string
import random

length = int(input())

def create_pass(length):
    password = ""
    num_pass = 5
    pass_list = []
    characters = string.printable
    for i in range(num_pass):

        for i in range(length):
            char = random.choice(characters)
            password += char

        pass_list.append(password)
        password = ""
    return pass_list



if __name__ == '__main__':
    print(create_pass(length))