from random import randint
from json import load, dumps
from yaml import dump as yamldump
from subprocess import run

import argparse

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

def generate_vaultfile(users, secret_filename, encrypt):

    valutfile_pattern = {}
    for user in users:
        valutfile_pattern[user['identifier']+"_username"] = user['username']
        valutfile_pattern[user['identifier']+"_password"] = user['password']

    #Create an ansible vaultfile for the users and identifiers
    with open(secret_filename, '+w') as outfile:
        outfile.write(yamldump(valutfile_pattern))

    # Encrypt the vaultfile
    if encrypt:
        run(["ansible-vault", "encrypt", secret_filename])
    return

def main(infilepath, systemname, encrypt):
    # Load json file containing a list of dictionaries
    # with the keys identifier and username from command line
    with open(infilepath, "r") as users:
        user_dict = load(users)

    # The users dict is modified in place
    generate_passwords(users=user_dict)
    if not systemname:
        print(dumps(user_dict, indent=2))
        return

    generate_vaultfile(
        users=user_dict,
        secret_filename=systemname+'.secret',
        encrypt=encrypt,
    )
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Secret generator for rolling out new systems."
    )
    parser.add_argument(
        '-i',
        '--infile',
        help="Input users.json file",
        required=True,
    )
    parser.add_argument(
        '-s',
        '--systemname',
        help=(
            "Target systemname. An ansible vault with this systemname will be created."
            "If this is omited no ansible vault will be created"
            "and the input object will be output to stdout"
        ),
        required=False,
    )
    parser.add_argument(
        '-e',
        '--encrypt',
        help=(
            "Allows you to disable the fault file encryption"
            "Mainly for debugging"
        ),
        default=True,
    )

    args = vars(parser.parse_args())
    main(
        infilepath=args['infile'],
        systemname=args['systemname'],
        encrypt=args['encrypt'],
    )
