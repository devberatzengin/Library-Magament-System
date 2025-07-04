from Modules.User import User
from Modules.Staff import Staff

staff = Staff()

staff.login("staffuser", "staffpass")


#print(s.get_user_info().get("username"))

#current.add_new_book("New Book", "Author Name", "1234567891", 2023)
#current.delete_book("1234567891")

#current.create_new_member("newuser", "newpass",None, None)    


staff.loan_to_user("1234567890", 4, 7)