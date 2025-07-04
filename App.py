from Modules.User import User
from Modules.Staff import Staff
from Modules.Member import Member
from Modules.Connection import Connection


#staff.login("staffuser", "staffpass")


#print(s.get_user_info().get("username"))

#current.add_new_book("New Book", "Author Name", "1234567891", 2023)
#current.delete_book("1234567891")

#current.create_new_member("newuser", "newpass",None, None)    


#staff.loan_to_user("1234567890", 4, 7)

mem = Member() 
mem.login("newuser2", "pass")
print(mem.get_id())

sta = Staff()
sta.login("testuser2", "testpass2")
print(sta.get_id())