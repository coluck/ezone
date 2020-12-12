import pickle
import getpass


# Fuction which saves the users dictionary object
def save_list(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


# Function which loads the user dictionary object
# if none exists an empty dictionary is returned
def load_list(name):
    try:
        with open(name + '.pkl', 'rb') as f:
          return pickle.load(f)
    except FileNotFoundError:
          return {}

# users dictionary (Hash map)
users = load_list("users")
# Bool which indicates if admin is logged in or not
privilege = False

# Checks to see if dictionary is empty or not
if not users:
    accounts = 0
else:
    accounts = 1

#Function to create a new user
def newUser():   
    while True:
        createLogin = input("Create login name: ")
        if createLogin in users:
            print("\nLogin name already exist! Try again\n")
        else:
            createPassword = getpass.getpass("Create password: ")
            users[createLogin] = createPassword
            #Takes user inputs stores in dictionary then saves it using the save_list funciton
            save_list(users, "users")
            print("\nUser created\n")
            break


# Function which allows user to login
def login(nick, pwd):

    if nick in users and users[nick] == pwd:
        return True
    else:
        return False


# Function to delete a user
def deleteUser():
    userName = input("\nEnter username you wish to delete: ")
    # Cannot delete admin for obvious reasons
    if userName == "admin":
        print("Cannot delete the admin account.\n")
    elif userName in users:
        #Deleting user from dictionary
        del users[userName]
        save_list(users, "users")
        print("User deleted.\n")
    else:
        print("User name does not exist in network.\n")