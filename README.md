# PassMan
Password manager written in python and java (coming soon, for use as android app)

 - `pip install -r requirements.txt` then run `pypassman.py -h`
 - Uses AES-256 to encrypt the database file
 - Uses PBKDF2 with 100,000 rounds to generate the encryption key from a passphrase. New salt is generated each time the database is updated.
 - Runs on python 3
```
usage: pypassmancli.py [-h] [-p PASSDB] action ...

Generate and manage passwords. Passwords are stored in a flat file encrypted
with AES-256.

optional arguments:
  -h, --help            show this help message and exit
  -p PASSDB, --passdb PASSDB
                        Path to the password list file.

PassMan Action:
  action                Password action to perform
    list                List the accounts in the database
    changep             Change your passphrase
    show                Show a specific account
    add                 Add a new account
    edit                Edit an existing account
    remove              Remove and existing account
    generate            Just generate a password. Don't store it anywhere.
```
