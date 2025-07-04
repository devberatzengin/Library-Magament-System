from Modules.User import User
from Modules.Staff import Staff
from Modules.Member import Member
import sys

def main_menu():
    print("\n📚 Library Management System")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

def staff_menu():
    print("\n👩‍💼 Staff Panel")
    print("1. Add New Book")
    print("2. Delete Book")
    print("3. Create New Member")
    print("4. Loan Book to Member")
    print("5. Approve Book Request")
    print("6. Reject Book Request")
    print("7. View Pending Book Requests")
    print("8. Logout")

def member_menu():
    print("\n🙋 Member Panel")
    print("1. Return Book")
    print("2. Request Book")
    print("3. Logout")

def main():
    while True:
        main_menu()
        choice = input("👉 Choose an option: ")

        if choice == "1":  # Login
            username = input("👤 Username: ")
            password = input("🔒 Password: ")

            temp_user = User()
            if temp_user.login(username, password):
                role = temp_user.get_role()
                if role == 1:  # Staff
                    current_user = Staff()
                    current_user.login(username, password)
                    staff_panel(current_user)
                elif role == 0:  # Member
                    current_user = Member()
                    current_user.login(username, password)
                    member_panel(current_user)
                else:
                    print("❌ Unknown user role.")
            else:
                print("❌ Login failed.")

        elif choice == "2":  # Register
            username = input("👤 Choose username: ")
            password = input("🔒 Choose password: ")
            user = User()
            user.register(username, password)

        elif choice == "3":
            print("👋 Goodbye!")
            sys.exit()

        else:
            print("⚠️ Invalid option. Try again.")

def staff_panel(staff):
    while True:
        staff_menu()
        choice = input("👉 Choose an option: ")

        if choice == "1":
            title = input("📕 Title: ")
            author = input("✍️ Author: ")
            isbn = input("📘 ISBN: ")
            year = input("📅 Publication Year: ")
            staff.add_new_book(title, author, isbn, year)

        elif choice == "2":
            isbn = input("❌ ISBN to delete: ")
            staff.delete_book(isbn)

        elif choice == "3":
            uname = input("👤 Username: ")
            pwd = input("🔑 Password: ")
            email = input("📧 Email: ")
            phone = input("📞 Phone: ")
            staff.create_new_member(uname, pwd, email, phone)

        elif choice == "4":
            isbn = input("📘 Book ISBN: ")
            uid = int(input("🔢 Member UserID: "))
            staff.loan_to_user(isbn, uid)

        elif choice == "5":
            rid = int(input("✅ Reservation ID to approve: "))
            staff.approve_request(rid)

        elif choice == "6":
            rid = int(input("❌ Reservation ID to reject: "))
            reason = input("📄 Reason for rejection: ")
            staff.reject_request(rid, reason)

        elif choice == "7":
            staff.view_pending_requests()

        elif choice == "8":
            print("👋 Logging out...")
            break

        else:
            print("⚠️ Invalid choice.")

def member_panel(member):
    while True:
        member_menu()
        choice = input("👉 Choose an option: ")

        if choice == "1":
            isbn = input("📘 Enter ISBN to return: ")
            member.return_book(isbn)

        elif choice == "2":
            isbn = input("📘 Enter ISBN to request: ")
            member.request_book(isbn)

        elif choice == "3":
            print("👋 Logging out...")
            break

        else:
            print("⚠️ Invalid choice.")

if __name__ == "__main__":
    main()
