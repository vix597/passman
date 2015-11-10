# passman
Password manager

```
usage: passman.py [-h] [-p PASSDB] action ...

Generate and manage passwords. Passwords are stored in a flat file encrypted
with AES-256.

optional arguments:
  -h, --help            show this help message and exit
  -p PASSDB, --passdb PASSDB
                        Path to the password list file.

PassMan Action:
  action                Password action to perform
    list                List the accounts in the database
    show                Show a specific account
    add                 Add a new account
    edit                Edit an existing account
    remove              Remove and existing account
```