import requests
import os
import hashlib

# There are multiple improvements that could be done, and this script could easily be made 10 times more efficient, however this was made as a learning experience to try out multiple different new things.

def hash_check(): 
    # Gets the response from the API as json, and prints the up-to-date version's MD5 hash.
    r = requests.get('https://stats.olympus-entertainment.com/api/v3.0/public/mission/latest/')
    data = r.json()
    curr_hash = data[0]["hash"]
    print("Hash of current mission file: " + curr_hash)
    # Finds local folder of AppData, then goes down subdirectories into where the Arma 3 Multiplayer Mission Files are kept and tries to find the OlyUpdaterHash.txt generated by the program.
    local_appdata = os.getenv('LOCALAPPDATA')
    subdir_path = os.path.join(local_appdata, 'Arma 3')
    subdir_path = os.path.join(subdir_path, 'MPMissionsCache')
    ## TESTING ## 
    # Create a folder named "MPMissionsCache2" and uncomment out the bit under this to test.
    #subdir_path = os.path.join(subdir_path, 'MPMissionsCache2') # Purely for testing, commented out when not needed.
    ## TESTING ##
    file_path = os.path.join(subdir_path, 'OlyUpdaterHash.txt')
    # Sets the value of the stored_hash variable to "None". Attempts to read the hash file, if it can't find it, it'll go to the no_hash_file function. If it can find it, it'll compare the hashes to see if the held copy is up-to-date.
    stored_hash = None
    try:
        with open(file_path, "r") as f:
            stored_hash = f.read()
            print("The stored hash is: " + stored_hash)
        print("Comparing hashes...")
        if curr_hash != stored_hash:
            print("The hashes are different, downloading the new mission file.")
            api_mission_req()
        else: # If the hashes match up, then the current version is identical to the up-to-date version.
            print("Hash verficiation complete, version is up-to-date and without errors.")
            input("Press ENTER to close...")
    except Exception as e:
        # Shows that there was some kind of error and its type.
        print(e)
        # Goes to the no_hash_file function passing variables.
        no_hash_file(file_path, curr_hash, subdir_path, data) 

def no_hash_file(file_path, curr_hash, subdir_path, data):
    print("No hash file exists, creating one...")
    # This creates a .txt file containing the up-to-date hash for the mission file.
    with open(file_path, 'w') as f:
        f.write(curr_hash)
    stored_hash = curr_hash
    # Although this is an area that could be massively improved upon, it is deliberately awful purely for implementing certain things.
    # But the intent here is to verify the currently held mission file's MD5 hash with the most up-to-date MD5 hash.
    print("Trying different method of verification...")
    curr_ver_filename = data[0]["name"]
    print("The up-to-date file name is: " + curr_ver_filename)
    file_path = os.path.join(subdir_path, curr_ver_filename)
    if os.path.exists(file_path):
        print("File exists, checking MD5 hashes...")
        with open(file_path, "rb") as f:
            md5_hash = hashlib.md5()
            while chunk := f.read(4096):
                md5_hash.update(chunk)
        print("Current file MD5 hash: " + md5_hash)
        if curr_hash == md5_hash: #Did someone say nested if statements? Compares the stored current version's hash to the up-to-date one.
            print("The currently held version is the same as the most recent version.")
            input("There is nothing further to do, press ENTER to close...")
        else:
            print("The currently held version differs from the most recent version.")
    else: 
        print("Current version not found, moving on.")
        api_mission_req(file_path, curr_hash, subdir_path, data, curr_ver_filename) 
    
def api_mission_req(file_path, curr_hash, subdir_path, data, curr_ver_filename):
# This section downloads the mission file in the Arma 3 Multiplayer Mission File directory, then checks the hash to ensure it is
# correctly downloaded without any errors.
    url = data[0]["url"] # Pulls the URL from the API for the Altis Life mission file.
    file_name = os.path.basename(url) # Uses the file name being the name from the URL.
    file_name, extension = os.path.splitext(file_name)
    DL_file_path = os.path.join(subdir_path, file_name + extension) # Specifies file path
    response = requests.get(url) # Assigns the response variable to the response.
    # This bit writes the response to the directory.
    with open(DL_file_path, "wb") as f:
        f.write(response.content)
    print("File downloaded successfully.")
    print("Checking hash to verify correct download.")
    hash_check()

# The official start to the script, instantly calling the hash_check function.
print("Welcome to Olympus Altis Life Mission File Updater!")
hash_check()