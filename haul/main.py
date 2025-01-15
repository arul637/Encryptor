from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES 
import getpass
import hashlib
import argparse
import colorama
from colorama import Fore, Style
import sys, os 

# initializations
colorama.init(autoreset=True)

class Encryptor:
    def __init__(self):
        self.CHUNK_SIZE = 64 * 1024
        self.BLOCK_SIZE = AES.block_size

    def passwordHandler(self):
        password = getpass.getpass("Enter the password: ")
        return hashlib.sha512(password.encode("utf-8")).hexdigest()
    
    def pad(self, data):
        pad_length = self.BLOCK_SIZE - (len(data) % self.BLOCK_SIZE)
        return data + bytes([pad_length] * pad_length)
    
    def unpad(self, data):
        pad_length = data[-1]
        return data[:-pad_length]

    def encrypt(self, filename, key, iv):
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            with open(filename, "rb") as input_file, open(f"{filename}.enc", "wb") as output_file:
                
                while True:
                    chunk = input_file.read(self.CHUNK_SIZE)
                    if len(chunk) == 0:
                        break
                    if len(chunk) % self.BLOCK_SIZE != 0:
                        chunk = self.pad(chunk)
                    output_file.write(cipher.encrypt(chunk))

                os.remove(filename)  
                print(Fore.GREEN + Style.BRIGHT + "[+] Encrypting" + Fore.MAGENTA + f" {filename} ")

        except FileNotFoundError:
            print(Fore.RED + "File" + Fore.CYAN + f" {filename} " + Fore.RED + " not found! ☹️")

        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"Error -> {e} ☹️") 
    
    def decrypt(self, filename, key, iv):
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            with open(file=filename, mode="rb") as input_file, open(file=f"{str(filename).replace('.enc', '')}", mode="wb") as output_file: 
                
                while True:
                    chunk = input_file.read(self.CHUNK_SIZE)
                    if len(chunk) == 0:  
                        break
                    decrypted_chunk = cipher.decrypt(chunk)

                    if len(input_file.peek(1)) == 0:  
                        decrypted_chunk = self.unpad(decrypted_chunk)

                    output_file.write(decrypted_chunk)

            os.remove(filename)
            print(Fore.GREEN + Style.BRIGHT + "[-] Decrypting" + Fore.MAGENTA + f" {filename} ")

        except FileNotFoundError:
            print(Fore.RED + "File" + Fore.CYAN + f" {filename} " + Fore.RED + " not found! ☹️")

        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"Error -> {e} ☹️") 

class HaulFileEncryptor:
    def __init__(self):
        pass 

    def passwordHandler(self):
        password = getpass.getpass("Enter the password: ")
        return hashlib.sha512(password.encode("utf-8")).hexdigest()

    def keyInitialization(self):
        salt = get_random_bytes(16)
        iv = get_random_bytes(16)
        with open("key.key", "wb") as key_file:
            key_file.write(salt)
            key_file.write(iv)

    def encryption(self, directory):
        password = self.passwordHandler()
        file_names = []
        for root, _, files in os.walk(directory):
            for file in files:
                importantFiles = ["haul.py", "key.key"]
                if file in importantFiles:
                    continue
                file_names.append(os.path.join(root, file))
        
        with open("key.key", "ab") as key_file:
            key_file.write(password.encode("utf-8"))

        with open("key.key", "rb") as key_file:
            salt = key_file.read(16)
            iv = key_file.read(16)
            password_hash = key_file.read(512)
        
        key = PBKDF2(password=password, dkLen=32, salt=salt)
        
        for file in file_names:
            Encryptor().encrypt(file, key, iv)

    def decryption(self, directory):
        password = self.passwordHandler()
        file_names = []
        for root, _, files in os.walk(directory):
            for file in files:
                importantFiles = ["haul.py", "key.key"]
                if file in importantFiles:
                    continue
                file_names.append(os.path.join(root, file))
        
        with open("key.key", "rb") as key_file:
            salt = key_file.read(16)
            iv = key_file.read(16)
            password_hash = key_file.read(512)

        if password != password_hash.decode("utf-8"):
            print(Fore.RED + Style.BRIGHT + "\n\nIncorrect Password\n\n")
            sys.exit(0)

        key = PBKDF2(password=password, dkLen=32, salt=salt)

        for file in file_names:
            Encryptor().decrypt(file, key, iv)
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file == "key.key":
                    os.remove(os.path.join(root, file))

    def handleDirectory(self, directory):
        if directory:
            if self.permissionChecker(directory):
                return directory
            else:
                sys.exit(1)
        else:
            current_directory = os.getcwd()
            if self.permissionChecker(current_directory):
                return current_directory
            else:
                sys.exit(1)

    def permissionChecker(self, directory):
        if os.access(directory, os.W_OK):
            return True 
        else:
            username = os.getlogin()
            print(Fore.RED + Style.BRIGHT + "user: " + Fore.MAGENTA + f"{username}" + Fore.RED + " has no permission to modify the directory " + Fore.MAGENTA + f"{directory}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Directory Encryption toolkit 🔐")
    parser.add_argument("--action", choices=["encrypt", "decrypt", "init"], type=str, help="Action need to perform, Encryption, Decryption or Generate the key.")
    parser.add_argument("--directory", "-d", type=str, help="Directory path", required=False)

    args = parser.parse_args() 

    haul = HaulFileEncryptor()
    directory = haul.handleDirectory(args.directory)

    if args.action == "init":
        haul.keyInitialization() 
    elif args.action == "encrypt":
        haul.encryption(directory) 
    elif args.action == "decrypt":
        haul.decryption(directory) 
    

if __name__ == "__main__":
    main()
