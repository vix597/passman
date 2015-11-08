import json
import os
from crypt import FileCryptoTool

class AccountExistsError(Exception):
    pass
class AccountDoesNotExistError(Exception):
    pass

class Account:
    def __init__(self, name, username, password, description=None, url=None):
        self.name = name
        self.username = username
        self.password = password
        self.description = description
        self.url = url
    
    def update(self, name, username, password, description=None, url=None):
        if name and len(name):
            self.name = name
        if username and len(username):
            self.username = username
        if password and len(password):
            self.password = password
        if description and len(description):
            self.description = description
        if url and len(url):
            self.url = url
    
    def display(self, secure=True):
        print("="*70)
        print("Name:",self.name)
        if not secure:
            print("Username: ",self.username)
            print("Password: ",self.password)
        print("Description: ",self.description)
        print("URL: ",self.url)
    
    def to_dict(self):
        return {
            "name":self.name,
            "username":self.username,
            "password":self.password,
            "description":self.description,
            "url":self.url
        }
    
    @classmethod
    def from_dict(self, d):
        return Account(
            name = d.get('name',None),
            username = d.get('username',None),
            password = d.get('password',None),
            description = d.get('description',None),
            url = d.get('url',None)
        )

class PassDb:
    def __init__(self, path):
        self.path = path
        self.accounts = {}
        
    def load(self, password):
        if not os.path.exists(self.path):
            return
            
        account_list = json.loads(
            FileCryptoTool.decrypt_file(
                password,
                self.path
            ).decode('utf-8')
        )
        
        for account in account_list:
            self.accounts[account['name']] = Account.from_dict(account)
        
    def update(self, name, new_name=None, username=None, password=None, description=None, url=None):
        if name not in self.accounts:
            raise AccountDoesNotExistError("No account with name "+name+" in the database.")
        if new_name and new_name in self.accounts:
            raise AccountExistsError("Cannot change "+name+" to "+new_name+". An account already exists with name: "+new_name)
        
        account = self.accounts[name]
        account.update(new_name, username, password, description, url)
        
        if new_name:
            del self.accounts[name]
            self.accounts[new_name] = account
    
    def remove(self, name):
        if name not in self.accounts:
            raise AccountDoesNotExistError("No account with name: "+name+" in the database.")
        
        del self.accounts[name]
    
    def add(self, name, username, password, description=None, url=None):
        if name in self.accounts:
            raise AccountExistsError("An account with name "+name+" already exists.")
        
        self.accounts[name] = Account(name, username, password, description, url)
    
    def get(self, name):
        if name in self.accounts:
            return self.accounts[name]
        else:
            return None
    
    def list_accounts(self):
        print("Count:",len(self.accounts),"accounts.")
        for account in self.accounts.values():
            account.display()
            
    def display_account(self, name, secure=True):
        if name not in self.accounts:
            raise AccountDoesNotExistError("No account with name "+name+" in the database.")
            
        self.accounts[name].display(secure)
    
    def save(self, password):
        if len(self.accounts) > 0:
            account_list = []
            for account in self.accounts.values():
                account_list.append(account.to_dict())
        
            FileCryptoTool.encrypt_file(
                password, 
                self.path, 
                json.dumps(account_list).encode('utf-8')
            )
