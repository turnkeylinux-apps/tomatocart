#!/usr/bin/python
"""Set TomatoCart admin password and email

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively
"""

import sys
import getopt
import random
import string
import hashlib

from dialog_wrapper import Dialog
from mysqlconf import MySQL
from executil import system

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "TomatoCart Password",
            "Enter new password for the 'admin' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "TomatoCart Email",
            "Enter email address for the 'admin' account.",
            "admin@example.com")

    salt = ''.join((random.choice(string.letters+string.digits) for x in range(2)))
    hash = ':'.join([hashlib.md5(salt+password).hexdigest(), salt])

    m = MySQL()
    m.execute('UPDATE tomatocart.administrators SET user_password=\"%s\",email_address=\"%s\" WHERE user_name=\"admin\";' % (hash, email))

    m.execute('UPDATE tomatocart.configuration SET configuration_value=\"%s\" WHERE configuration_key=\"STORE_OWNER_EMAIL_ADDRESS\";' % email)

    m.execute('UPDATE tomatocart.configuration SET configuration_value=\"\\"Store Owner\\" <%s>\" WHERE configuration_key=\"EMAIL_FROM\";' % email)

    # delete cache
    system("rm -f /var/cache/tomatocart/*")


if __name__ == "__main__":
    main()

