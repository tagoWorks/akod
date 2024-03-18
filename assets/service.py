import os, subprocess, time, shutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Configure the following variables to match your GitHub account and repository

username = 'github username'
licensestorage_repo = 'github repo name'
token = 'github personal access token'
# Change your private key!
privatekey = b'12345678901234567890123456789012'





#----------------------------------------------
# ONLY CHANGE IF YOU KNOW WHAT YOU ARE DOING!!
#----------------------------------------------

url = f'github.com/{username}/{licensestorage_repo}'
repo = '/Users/' + os.getlogin() + '/Documents/GitHub/' + licensestorage_repo
key_size = 32
registered_accounts = 'registered'
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
        exit()
    print("Repository cloned successfully.")
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
                commit_changes(f"Registered account email '{folder}' with encrypted license data.")
                print(f"Email '{folder}' registered with encrypted license data.")
            except Exception as e:
                print(f"Error: {e}")
def delete_removed_folders(existing_folders, registered_folders):
    for folder in existing_folders:
        if folder != '.git' and folder not in registered_folders:
            try:
                shutil.rmtree(os.path.join(repo, folder))
                commit_changes(f"Deleted folder '{folder}'.")
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
print("\n\nWatching for changes...")
if not os.path.exists(repo):
    clone(url, token)
monitor(registered_accounts, repo)
