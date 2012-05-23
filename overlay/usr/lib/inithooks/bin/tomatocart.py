#!/usr/bin/python
"""Set TomatoCart/Piwik admin password and email (and domain for piwik tracking)

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively
    --domain=   unless provided, will ask interactively
                DEFAULT=shop.example.com
"""

import re
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

DEFAULT_DOMAIN="shop.example.com"

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email=', 'domain='])
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
        elif opt == '--domain':
            domain = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "TomatoCart/Piwik Password",
            "Enter new password for the 'admin' accounts.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "TomatoCart/Piwik Email",
            "Enter email address for the 'admin' accounts.",
            "admin@example.com")

    if not domain:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        domain = d.get_input(
            "Piwik Domain",
            "Enter the domain for piwik tracking.",
            DEFAULT_DOMAIN)

    if domain == "DEFAULT":
        domain = DEFAULT_DOMAIN

    t_salt = ''.join((random.choice(string.letters+string.digits) for x in range(2)))
    t_hash = ':'.join([hashlib.md5(t_salt+password).hexdigest(), t_salt])

    p_hash = hashlib.md5(password).hexdigest()

    m = MySQL()
    m.execute('UPDATE tomatocart.administrators SET user_password=\"%s\",email_address=\"%s\" WHERE user_name=\"admin\";' % (t_hash, email))

    m.execute('UPDATE tomatocart.piwik_user SET password=\"%s\",email=\"%s\" WHERE login=\"piwik_view\";' % (p_hash, email))

    m.execute('UPDATE tomatocart.configuration SET configuration_value=\"%s\" WHERE configuration_key=\"STORE_OWNER_EMAIL_ADDRESS\";' % email)
    m.execute('UPDATE tomatocart.configuration SET configuration_value=\"\\"Store Owner\\" <%s>\" WHERE configuration_key=\"EMAIL_FROM\";' % email)

    m.execute('UPDATE tomatocart.piwik_site SET main_url=\"http://%s\" WHERE idsite=1;' % domain)

    CONFIG="/var/www/tomatocart/ext/piwik/config/config.ini.php"
    old = file(CONFIG).read()
    new = re.sub("email.*", "email = \"%s\"" % email, old)
    new = re.sub("password.*", "password = \"%s\"" % p_hash, old, count=1)
    file(CONFIG, "w").write(new)

    # delete cache
    system("rm -f /var/cache/tomatocart/*")


if __name__ == "__main__":
    main()

