import argparse
import os
import sys
import json
import getpass
import string
import random
from passdb import PassDb, AccountExistsError, AccountDoesNotExistError
from wizards import account_wizard, generate_password_wizard

def pass_gen(size=15, exclude_chars="", upper_case_count=0):
    if upper_case_count > size:
        upper_case_count = size
    
    out = ""
    
    valid_chars = string.digits+string.ascii_lowercase+string.punctuation
    valid_chars = ''.join(e for e in valid_chars if e not in exlude_chars)
    upper_case = string.ascii_upercase
    
    if upper_case_count > 0:
        uc = ''.join(random.choice(upper_case) for x in range(upper_case_count))
        out ++ uc
        size -= upper_case_count
    else:
        valid_chars += string.ascii_uppercase
        
    out += ''.join(random.choice(valid_chars) for x in range(size))
    return out

def add_account(db):
    account_wizard.run()
    generate_password_wizard.run()
    
    name = account_wizard['name'].value
    username = account_wizard['username'].value
    description = account_wizard['description'].value
    url = account_wizard['url'].value
    
    num_upper = generate_password_wizard['password.case.rule'].value
    exclude = generate_password_wizard['password.disallow.chars'].value
    size = generate_password_wizard['password.size'].value
    copy = generate_password_wizard['password.copy'].value
    
    password = pass_gen(size, exclude, num_upper)
    print("Password is: ",password)
    
    db.add(name, username, password, description, url)
    
def list_accounts(db):
    db.list_accounts()
    
def remove_account(db):
    name = input("Name of the account to remove: ")
    check = input("Are you sure you want to continue? This cannot be undone. (y,n)")
    if check.lower() in ("y","yes"):
        db.remove(name)
    
def edit_account(db):
    name = input("Name of account to edit: ")
    account = db.get(name)
    if not account:
        print("No account with name of",name,"exists in the database.")
        return
    
    check = input("Modify account details? (not including password) (y,n): ")
    if check.lower() in ('y','yes'):
        account_wizard.steps['name'].default = name
        account_wizard.steps['username'].default=account.username
        account_wizard.run()
        
    check = input("Generate a new password? (y,n): ")
    if check.lower() in ('y','yes'):
        generate_password_wizard.run()
    
def show_account(db):
    name = input("Name of the account to show: ")
    show_pass = input("Include password in output? (y,n): ")
    if show_pass.lower() in ('y','yes'):
        secure = False
    else:
        secure = True
    db.display_account(name, secure)
    
if __name__ == "__main__":
    actions = {
        "add":add_account,
        "list":list_accounts,
        "show":show_account,
        "remove":remove_account,
        "edit":edit_account
    }
    
    parser = argparse.ArgumentParser(
        description=
        """
        Generate and manage passwords. Passwords are stored 
        in a flat file encrypted with AES-256. 
        """
    )
    parser.add_argument(
        "-p",
        "--passdb",
        help="Path to the password list file.",
        type=str,
        action="store",
        default=os.path.join(".","passdb.pm")
    )
    parser.add_argument(
        "-a",
        "--action",
        help="Specify an action: "+', '.join(actions),
        type=str,
        action="store",
        required=True
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.passdb):
        print("Passdb path:",args.passdb,"does not exist.")
        ans = input("Create it? (y,n): ")
        if ans.lower() in ('y','yes'):
            print(
                """
                Enter a password to secure your password list.
                A good password is greater than 8 charcters and
                inludes letters (upper/lower case), numbers, and
                special characters. That being said, this application
                does nothing to ensure you're not dumb. 
                """
            )
            password = None
            check = ""
            while(password != check):
                try:
                    password = getpass.getpass()
                    check = getpass.getpass("Again:")
                except KeyboardInterrupt:
                    sys.exit(0)
                if password != check:
                    print("Passwords don't match. Try again.")
        else:
            print("Goodbye.")
            sys.exit(0)
            
    
    db = PassDb(args.passdb)
    db.load(password)
    
    if not args.action in actions:
        print("Invalid action :",args.action)
        sys.exit(-1)
    else:
        try:
            actions[args.action](db)
            db.save(password)
        except KeyboardInterrupt:
            pass
        except AccountExistsError as e:
            print(str(e))
            sys.exit(-1)
        except AccountDoesNotExistError as e:
            print(str(e))
            sys.exit(-1)
        sys.exit(0)
    
    
