import argparse
import os
import sys
import getpass

from passgen import PassGen
from passdb import PassDb, AccountExistsError, AccountDoesNotExistError, DbLoadError, DbSaveError

def get_passphrase(first_time=False):
    if first_time:
        print(
            """
            Enter a passphrase to secure your password list.
            It is not my job to explain what a good passphrase is.
            """
        )
        passphrase = None
        check = ""
        while(passphrase != check):
            try:
                passphrase = getpass.getpass("Passphrase:")
                check = getpass.getpass("Again:")
            except KeyboardInterrupt:
                sys.exit(0)
            if passphrase != check:
                print("Passphrases don't match. Try again.")
        return passphrase
    else:
        return getpass.getpass("Enter your passphrase:")

def get_password(size=15,exclude_chars=""):
    print("Generating password...")
    while 1:
        password = PassGen.generate(size=size,exclude_chars=exclude_chars)
        print(password)
        check = input("Apply this password to the account? (y,N): ")
        if check.lower() in ("y","yes"):
            return password

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Generate and manage passwords. Passwords are stored in a flat file encrypted with AES-256.")
    parser.add_argument("-p","--passdb",help="Path to the password list file.",type=str,action="store",default=os.path.join(".","passdb.pm"))
    subcmd = parser.add_subparsers(title="PassMan Action",metavar="action",help="Password action to perform",dest="action")
    subcmd.required = True
    
    list_accounts = subcmd.add_parser("list",help="List the accounts in the database")
    
    show_account = subcmd.add_parser("show",help="Show a specific account")
    show_account.add_argument("account",metavar="ACCOUNT",action="store",type=str,help="Name of the account to display")
    show_account.add_argument("-s","--show_all",action="store_true",help="Show all information for the selected account, including cleartext passwords")
    
    add_account = subcmd.add_parser("add",help="Add a new account")
    add_account.add_argument("account",metavar="ACCOUNT",action="store",type=str,help="Name of the new account to add")
    add_account.add_argument("username",metavar="USERNAME",action="store",type=str,help="Username for the new account")
    add_account.add_argument("-d","--description",action="store",type=str,help="Description for the new account",default=None)
    add_account.add_argument("-u","--url",action="store",type=str,help="URL For the account login page",default=None)
    add_account.add_argument("-l","--password_length",action="store",type=int,help="Length for the generated password",default=15)
    add_account.add_argument("-e","--exclude_chars",action="store",type=str,help="List of characters to exclude from the generated password",default="")
    
    edit_account = subcmd.add_parser("edit",help="Edit an existing account")
    edit_account.add_argument("account",metavar="ACCOUNT",action="store",type=str,help="Name of the account to edit")
    
    remove_account = subcmd.add_parser("remove",help="Remove and existing account")
    remove_account.add_argument("account",metavar="ACCOUNT",action="store",type=str,help="Name of the account to remove")
    
    args = parser.parse_args()
   
    first_time = False
    if not os.path.exists(args.passdb):
        if args.action == "list" or args.action == "show":
            print("Passdb has not been created yet. Nothing to list or show.")
            sys.exit(0)
        print("Passdb path:",args.passdb,"does not exist.")
        ans = input("Create it? (y,N): ")
        if ans.lower() not in ('y','yes'):
            print("Goodbye.")
            sys.exit(0)
        first_time = True

    passphrase = get_passphrase(first_time)
    db = PassDb(args.passdb)
    
    try:
        db.load(passphrase)
        
        if args.action == "list":
            db.ls()
        elif args.action == "show":
            db.show(args.account, secure=(not args.show_all))
        elif args.action == "add":
            password = get_password(size=int(args.password_length),exclude_chars=args.exclude_chars)
            db.add(args.account,args.username,password,args.description,args.url)
            print("Account added!")
        elif args.action == "edit":
            account = db.get(args.account)
            name = input("Enter the new name for the account ["+account.name+"]: ") or account.name
            username = input("Enter the new username for the account ["+account.username+"]: ") or account.username
            check = input("Generate a new password for the account? (y,N): ")
            password = account.password
            if check.lower() in ('y','yes'):
                length = int(input("Select a new password length [15]: ")) or 15
                exclude = input("Enter a list of characters to exclude: ") or ""
                password = get_password(length,exclude)
            description = input("Enter the new description for the account ["+account.description+"]: ") or account.description
            url = input("Enter the new URL for the account ["+account.url+"]: ") or account.url
            if name == args.account:
                name = None
            db.update(args.account,name,username,password,description,url)
            print("Account updated!")
        elif args.action == "remove":
            check = input("Are you sure you want to remove "+args.account+"? This action cannot be undone. (y,N): ")
            if check.lower() in ('y','yes'):
                db.remove(args.account)
                print("Account removed!")
            
        if args.action in ("edit","remove","add"):
            db.save(passphrase)
    except KeyboardInterrupt:
        print("Operation canceled. Changes will not be saved.")
    except (AccountExistsError, AccountDoesNotExistError, DbLoadError, DbSaveError) as e:
        print(str(e))
        sys.exit(-1)
    sys.exit(0)