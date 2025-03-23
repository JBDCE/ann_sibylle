from random import randint
from json import load, dumps
from subprocess import run
from os.path import isfile

# Assigning aliases here to make it easier
# to see the difference between yaml and json handling in code
from yaml import safe_dump as yamldump
from yaml import safe_load as yamlload
# TODO: Perhaps just importing yaml and 
# then calling yaml.load() would be cleaner?

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

def generate_vaultfile(users):
    # Convert the users dict into the format required for use in ansible
    vaultfile_pattern = {}
    for user in users:
        vaultfile_pattern[user['identifier']+"_username"] = user['username']
        vaultfile_pattern[user['identifier']+"_password"] = user['password']

    return vaultfile_pattern

def write_vaultfile(vaultfile_pattern, secret_filename, encrypt):
    # Hander for vaultfile operations.
    # Makes sure only new keys are added to existing files
    # and handles ansible-vault encryption

    updated_vaultfile = {}
    if isfile(secret_filename):
        # Decrypt input file. If we are unable to decrypt the file
        # we bail as we would otherwise delete previously created secrets
        if encrypt:
            result = run(["ansible-vault", "decrypt", secret_filename])
            assert result.returncode == 0, "Decrypting vault failed"

        # Load the existing vaultfile
        with open(secret_filename, 'r') as outfile:
            updated_vaultfile = yamlload(outfile)

    for key, value in vaultfile_pattern.items():
        # If the username or password was already set dont alter it
        if key in updated_vaultfile:
            continue
        updated_vaultfile[key] = value

    with open(secret_filename, 'w') as outfile:
        outfile.write(yamldump(updated_vaultfile))

    # Encrypt the vaultfile
    if encrypt:
        result = run(["ansible-vault", "encrypt", secret_filename])
        assert result.returncode == 0, "Encrypting vault failed"

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

    vaultfile_pattern = generate_vaultfile(
        users=user_dict,
    )
    write_vaultfile(
        vaultfile_pattern=vaultfile_pattern,
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
        '--dont-encrypt',
        dest='dont_encrypt',
        help=(
            "Allows you to disable the fault file encryption"
            "Mainly for debugging"
        ),
        default=False,
        action='store_true',
    )

    args = vars(parser.parse_args())
    main(
        infilepath=args['infile'],
        systemname=args['systemname'],
        encrypt=not args['dont_encrypt'],
    )
