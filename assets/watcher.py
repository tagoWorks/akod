import os, subprocess, time, shutil, string, secrets, json, glob
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


#----------------------------------------------
# ONLY CHANGE IF YOU KNOW WHAT YOU ARE DOING!!
#----------------------------------------------





def clone(url, pat):
    git_command = ['git', 'clone', f'https://{pat}@{url}']
    try:
        if not os.path.exists('/Users/' + os.getlogin() + '/Documents/GitHub/'):
            os.makedirs('/Users/' + os.getlogin() + '/Documents/GitHub/')
        os.chdir('/Users/' + os.getlogin() + '/Documents/GitHub/')
        output = subprocess.check_output(git_command)
        os.chdir('.')
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    print("Repository cloned successfully.")
    exit()
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return iv + ciphertext
def process_new_folders(new_folders):
    for folder in new_folders:
        folder_path = os.path.join(registered_accounts, folder)
        target_folder_path = os.path.join(repo, folder)
        if not os.path.exists(target_folder_path):
            try:
                files = os.listdir(folder_path)
                for file in files:
                    file_path = os.path.join(folder_path, file)
                    encrypted_data = encrypt_file(file_path, privatekey)
                    shutil.copytree(folder_path, target_folder_path)
                    encrypted_file_path = os.path.join(target_folder_path, file)
                    with open(encrypted_file_path, 'wb') as f:
                        f.write(encrypted_data)
                commit_changes(f"Account '{folder}' created with encrypted license data.")
                print(f"'{folder}' created an account with an encrypted license.")
            except Exception as e:
                print(f"Error: {e}")
def delete_removed_folders(existing_folders, registered_folders):
    for folder in existing_folders:
        if folder != '.git' and folder not in registered_folders:
            try:
                shutil.rmtree(os.path.join(repo, folder))
                commit_changes(f"Deleted account '{folder}'.")
                print(f"Account '{folder}' deleted.")
            except Exception as e:
                print(f"Error: {e}")
def commit_changes(commit_message):
    global token
    try:
        git_add = f'git -C {repo} add .'
        git_commit = f'git -C {repo} commit -m "{commit_message}"'
        git_push = 'git -C ' + repo + ' push https://' + token + '@' + url
        os.system(git_add)
        os.system(git_commit)
        os.system(git_push)
        print("Changes committed and pushed successfully through Git.")
    except Exception as e:
        print(f"Error: {e}")
def monitor(registered_accounts, repo_path):
    while True:
        existing_folders = [folder for folder in os.listdir(repo_path) if os.path.isdir(os.path.join(repo_path, folder)) and folder != '.git']
        registered_folders = [folder for folder in os.listdir(registered_accounts) if os.path.isdir(os.path.join(registered_accounts, folder))]
        process_new_folders(registered_folders)
        delete_removed_folders(existing_folders, registered_folders)
        time.sleep(1)
def load_config():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(current_dir)
    config_file_path = os.path.join(parent_dir, 'config.json')
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config
config = load_config()
username = config.get('GITUSERNAME', 'not_found')
licensestorage_repo = config.get('GITSTORAGEREPO', 'not_found')
token = config.get('GITPAT', 'not_found')
pubkeylink = config.get('netlifyURL', 'not_found')
if token == 'not_found' or username == 'not_found' or licensestorage_repo == 'not_found' or pubkeylink == 'not_found':
    print("Missing configuration. Please check your config.json file.")
url = f'github.com/{username}/{licensestorage_repo}'
repo = '/Users/' + os.getlogin() + '/Documents/GitHub/' + licensestorage_repo
# Please only change the identifier if you know what you are doing. Learn more at https://github.com/tagoWorks/akod/wiki/What-are-the-AKoDAuth-Identifiers%3F#important-notices
identifier = b'3iDdjV4wARLuGZaPN9_E-hqHT0O8Ibiju293QLmCsgo='
registered_accounts = 'registered'  
if not os.path.exists('identifiers.txt'):
    backupfile = glob.glob('/Users/' + os.getlogin() + '/Documents/' + 'akodidentifiers-backup-*.txt')
    if backupfile:
        for backupfile in backupfile:
            if os.path.exists(backupfile):
                cont = input("Could not find identifiers.txt but found a backup! It is heavily recommended that you do not regenerate your identifiers as it can cause key reading errors (Learn more at Learn more at https://github.com/tagoWorks/akod/wiki/What-are-the-AKoDAuth-Identifiers%3F). Do you want to restore the backup (y/n) ")
                if cont == 'y':
                    shutil.copyfile(backupfile, 'identifiers.txt')
                    print("Restored backup identifiers. Please do not share it with anyone. It is recommended that you do not regenerate it.")   
                    exit()
                if cont == 'n':
                    os.remove(backupfile)
    if not os.path.exists(registered_accounts):
        os.mkdir(registered_accounts)
    privkey = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    if not bytes(''.join(chr(array) for array in [51, 105, 68, 100, 106, 86, 52, 119, 65, 82, 76, 117, 71, 90, 97, 80, 78, 57, 95, 69, 45, 104, 113, 72, 84, 48, 79, 56, 73, 98, 105, 106, 117, 50, 57, 51, 81, 76, 109, 67, 115, 103, 111, 61]), 'utf-8') == identifier: print("It seems that you've edited the identifier from the default identifier key! Only change the identifier if you know what you are doing, as it will make validating licenses impossible with AKoDAuth. Learn more at https://github.com/tagoworks/akod") and exit()
    with open('identifiers.txt', 'w') as f:
        fernet = Fernet(identifier)
        pubkey = fernet.encrypt(pubkeylink.encode()).decode()
        f.write("---- This auto generated file contains very sensitive strings - Do not share them with anyone - https://github.com/tagoWorks/akod/wiki/What-are-the-AKoDAuth-Identifiers%3F ----\n\n")
        f.write('PRIVATE KEY IDENTIFIER\n')
        f.write(privkey)
        f.write('\n\nPUBLIC KEY IDENTIFIER\n')
        f.write(pubkey)
        f.write("\n\n---- This auto generated file contains very sensitive strings - Do not share them with anyone - https://github.com/tagoWorks/akod/wiki/What-are-the-AKoDAuth-Identifiers%3F ----\n\n")
        f.close()
    with open ('/Users/' + os.getlogin() + '/Documents/akodidentifiers-backup-' + time.strftime("%d-%m-%Y-%H-%M-%S") + '.txt', 'w') as f:
        f.write("---- This auto generated file contains very sensitive strings - Do not share them with anyone - https://github.com/tagoWorks/akod/wiki/What-are-the-AKoDAuth-Identifiers%3F ----\n\n")
        f.write('PRIVATE KEY IDENTIFIER\n')
        f.write(privkey)
        f.write('\n\nPUBLIC KEY IDENTIFIER\n')
        f.write(pubkey)
        f.write("\n\n---- This auto generated file contains very sensitive strings - Do not share them with anyone - https://github.com/tagoWorks/akod/wiki/What-are-the-AKoDAuth-Identifiers%3F ----\n\n")
        f.close()
    print("Generated identifiers. Please do not share it with anyone. It is recommended that you do not regenerate it.")
    exit()
if not os.path.exists(repo):
    clone(url, token)
with open('identifiers.txt', 'r') as f:
    lines = f.readlines()
    for i in range(len(lines)):
        if "PRIVATE KEY IDENTIFIER" in lines[i]:
            privatekey = lines[i+1].strip().encode()
            break
if not os.path.exists(registered_accounts):
    os.mkdir(registered_accounts)
    exit()
print("\n\nWatching account folder...")
monitor(registered_accounts, repo)