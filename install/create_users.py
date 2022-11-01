from random import choice

from name_lists import fnames, lnames

# This script produces N create_user() calls, with random names
# (listed in name_lists.py). These calls are printed to stdout
# and can be piped to a shell. All of the names have been chosen
# so that each username (first 3 letters of first name + first 3
# letters of last name) will be unique.

# --- HOW TO USE ---
# Run the following in the project directory:
# python3 create_users.py | pipenv run django-admin shell_plus

N = 100

fulltext = ""
usrnames = []

for i in range(N):
    fname = choice(fnames)
    lname = choice(lnames)
    usrname = fname[:3].lower() + lname[:3].lower()
    while usrname in usrnames:
        fname = choice(fnames)
        lname = choice(lnames)
        usrname = fname[:3].lower() + lname[:3].lower()
    usrnames.append(usrname)
    fulltext = (
        fulltext
        + """UserAccount.objects.create_user(
first_name=\"{fname}\",
last_name=\"{lname}\",
username=\"{usrname}\",
email=\"{email}\",
password=\"abcde\"
)
""".format(
            fname=fname,
            lname=lname,
            usrname=usrname,
            email=fname.lower() + "@" + lname.lower() + ".se",
        )
    )
print(fulltext, end="")
