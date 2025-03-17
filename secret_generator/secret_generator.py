from random import randint
from json import load
from sys import argv

# This excludes a bunch of chars that might
# lead to problems down the line so omitting them
valid_chars = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "1234567890"
    "-_()[]"
)

def _generate_password(charlist="", length=15):
    password = []
    for _ in range(length):
        password.append(charlist[randint(0, len(charlist)-1)])
    return "".join(password)

def generate_passwords(users):
    if not users:
        users = {
            'identifier': 'foo',
            'username': 'bar',
        }
    for user in users:
        user['password'] = _generate_password(valid_chars)
    return

def generate_vaultfile(users):
    # TODO Create an ansible vaultfile for the users and identifiers
    return

def main(infilepath):
    # Load json file containing a list of dictionaries
    # with the keys identifier and username from command line
    with open(infilepath, "r") as users:
        user_dict = load(users)

    # The users dict is modified in place
    generate_passwords(users=user_dict)

    generate_vaultfile(users=user_dict)
    return

if __name__ == "__main__":
    infile=argv[1]
    print(infile)
    main(infilepath=infile)