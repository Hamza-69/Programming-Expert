import json


CONTACT_FILE_PATH = "Contact List/contacts.json"


def read_contacts(file_path):
    try:
        with open(file_path, 'r') as f:
            contacts = json.load(f)
    except FileNotFoundError:
        contacts = {}

    return contacts


def write_contacts(file_path, contacts):
    with open(file_path, 'w') as f:
        json.dump(contacts, f)


def verify_email_address(email):
    if "@" not in email:
        return False

    split_email = email.split("@")
    identifier = "".join(split_email[:-1])
    domain = split_email[-1]

    if len(identifier) < 1:
        return False

    if "." not in domain:
        return False

    split_domain = domain.split(".")

    for section in split_domain:
        if len(section) == 0:
            return False
    return True

def return_email():
    while True:
        email = input("Email Address: ")
        if email == "":
            print("No Email was added.")
            return email
        elif verify_email_address(email):
            return email
        else:
            print("Invalid Email Address. Try Again.")
    
def verify_phone(text):
    while True:
        mb = input(text)
        if mb == "":
            print("No number was added.")
            return mb
        elif mb.replace("-","").isdigit() and len(mb.replace("-", "")) == 10:
            return mb
        else:
            print("Invalid Phone Number. Try Again.")
def address():
    while True:
        email = input("Address: ")
        if email == "":
            print("No Address was added.")
        return email      
    
def empty(text):
    if text == "":
        return True
    else:
        return False
    
def print_contact(key,contacts):
    item = contacts[key]
    print(key)
    for i in item.keys():
        if empty(item):
            continue
        else:
            print(f"    {i}: {item[i]}")
def info():
    print("Welcome to your contact list!")
    print(
        '''
The following is a list of useable commands:
"add": Adds a contact.
"delete": Deletes a contact.
"list": Lists all contacts.
"search": Searches for a contact by name.
"q": Quits the program and saves the contact list.
        '''
    )

def command_flow(contacts):
    cmds = ["add", "delete", "list", "search", "q"]
    x = input("Type a command: ")
    if x == cmds[0]:
        add_contact(contacts)
    elif x == cmds[1]:
        delete_contact(contacts)
    elif x == cmds[2]:
        list_contacts(contacts)
    elif x == cmds[3]:
        search_for_contact(contacts)
    elif x == cmds[4]:
        print("Contacts were saved successfully.")
        write_contacts(CONTACT_FILE_PATH, contacts)
        return False
    else:
        print("Unknown command.")

def add_contact(contacts):
    Fn = input("First Name: ")
    Ln = input("Last Name: ")
    mb = verify_phone("Mobile Phone Number: ")
    pn = verify_phone("Home Phone Number: ")
    em = return_email()
    ad = address()
    if f"{Fn} {Ln}" in contacts.keys():
        print("A contact with this name already exists.")
        return
    else:
        contacts[f"{Fn} {Ln}"] = {"Mobile Phone Number":mb,"Home Phone Number":pn,"Email Address":em,"Address":ad }
        print("Contact Added!")

def search_for_contact(contacts):
    f = input("First Name: ")
    l = input("Last Name: ")
    found = []
    for i in contacts.keys():
        if f in i or l in i:
            found.append(i)
    nb = 0
    print(f"Found {len(found)} matching contacts.")
    for i in found:
        nb+=1
        print(f"{nb}.", end=" ")
        print_contact(i, contacts)

def delete_contact(contacts):
    Fn = input("First Name: ")
    Ln = input("Last Name: ")
    if f"{Fn} {Ln}" in contacts.keys():
        result = input("Are you sure you want to delete this contact (yes/no)? ")
    else:
        print("No contact with this name exists.")
        return
    if result == "yes":
        del contacts[f"{Fn} {Ln}"]
        print("Contact deleted!")
def list_contacts(contacts):
    nb = 0
    for i in contacts.keys():
        nb+=1
        print(f"{nb}.", end=" ")
        print_contact(i, contacts)

def main(contacts_path):
    contacts = read_contacts(contacts_path)
    info()
    while True:
        x = command_flow(contacts)
        if x == False:
            break

if __name__ == "__main__":
    main(CONTACT_FILE_PATH)