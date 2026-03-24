contacts = {}

while True:

    print("\n1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter name: ")
        phone = input("Enter phone number: ")
        contacts[name] = phone
        print("Contact added!")

    elif choice == "2":
        print("\nContacts List:")
        for name, phone in contacts.items():
            print(name, ":", phone)

    elif choice == "3":
        search = input("Enter name to search: ")
        if search in contacts:
            print("Phone number:", contacts[search])
        else:
            print("Contact not found")

    elif choice == "4":
        delete = input("Enter name to delete: ")
        if delete in contacts:
            del contacts[delete]
            print("Contact deleted")
        else:
            print("Contact not found")

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice")