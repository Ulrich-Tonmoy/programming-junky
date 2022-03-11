from cryptography.fernet import Fernet
import os


class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        try:
            with open(path, 'rb') as f:
                self.key = f.read()
        except IOError:
            print("Invalid filename!!!")

    def create_pass_file(self, path, init_value=None):
        self.password_file = path

        if init_value is not None:
            for key, value in init_value.items():
                self.add_password(key, value)

    def load_pass_file(self, path):
        self.password_file = path

        try:
            with open(path, 'r') as f:
                for line in f:
                    site, encrypted = line.split(":")
                    self.password_dict[site] = Fernet(self.key).decrypt(
                        encrypted.encode()).decode()
        except IOError:
            print("Invalid filename!!!")

    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, "a+") as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict[site]

    def get_all_password(self):
        return self.password_dict

    def del_password(self, site):
        try:
            password = self.password_dict[site]

            with open(self.password_file, "r") as f:
                lines = f.readlines()

                with open(self.password_file, "w") as f:
                    for line in lines:
                        username, encrypted = line.split(":")
                        if username != site:
                            f.write(line)

            print("Password Deleted!")

        except IOError:
            print("Invalid!!!")

    def del_all_password(self):
        try:
            os.remove(self.password_file)
            print("All Password Deleted!")
        except IOError:
            print("Invalid!!!")


def main():
    password = {}

    pm = PasswordManager()

    print(""" Menu
        (1) Create a new key
        (2) Load an existing key
        (3) Create a new password file
        (4) Load existing password file
        (5) Add a new password
        (6) Get a password
        (7) Get all password
        (8) Delete a password
        (9) Delete all password
        (0) Quit
        """)

    done = False

    while not done:
        choice = input("Enter your choice: ")

        if choice == "1":
            path = input("Enter a filename: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter filename: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter filename: ")
            pm.create_pass_file(path, password)
        elif choice == "4":
            path = input("Enter filename: ")
            pm.load_pass_file(path)
        elif choice == "5":
            sitename = input("Enter site name: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            site = sitename + "~" + username
            pm.add_password(site, password)
        elif choice == "6":
            sitename = input("Enter site name: ")
            username = input("Enter username: ")
            site = sitename + "~" + username
            print(
                f"Pass for the site -> {sitename} & username-> {username} is -> {pm.get_password(site)}")
        elif choice == "7":
            print(pm.get_all_password())
        elif choice == "8":
            sitename = input("Enter site name: ")
            username = input("Enter username: ")
            site = sitename + "~" + username
            pm.del_password(site)
        elif choice == "9":
            path = input("Enter filename: ")
            pm.del_all_password(path)
        elif choice == "0":
            done = True
        else:
            print("Invalid Choice!!!")


main()
