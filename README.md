📚 Library Management System

A Python-based Library Management System that allows **staff and members** to interact with a SQL Server database through a command-line interface. Built with `pyodbc` and follows OOP design principles.

---

## 🚀 Features

- 👤 User authentication (Register/Login)
- 👮 Staff operations:
  - Add / delete books
  - Create new members
  - Approve / reject book reservation requests
- 🙋 Member operations:
  - Request books
  - View active loans
  - Return borrowed books
- 🔐 Role-based access (Staff / Member)
- 💾 SQL Server database with normalized tables
- 📋 Logging system for all errors and operations
- 📦 CLI menu with input handling

---

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Database**: SQL Server
- **Library**: pyodbc
- **Modules**: OOP-based classes (User, Member, Staff, Connection, etc.)

---

## 📁 Project Structure

```
LibraryManagementSystem/
├── Modules/
│   ├── User.py
│   ├── Member.py
│   ├── Staff.py
│   ├── Connection.py
│   └── Log.py
├── app.py
└── README.md
```

---

## 🧑‍💻 Usage

> Make sure your SQL Server is running and configured correctly.

1. Install dependencies:
   ```bash
   pip install pyodbc
   ```

2. Run the main application:
   ```bash
   python app.py
   ```

3. Follow the CLI prompts to:
   - Login / Register
   - Interact as a staff or member

---

## 🗄️ Database Tables

- `tblUser` — users with role (0: Member, 1: Staff)
- `tblBook` — books in the library
- `tblLoans` — active & past book loans
- `tblReservations` — book reservation requests
- `tblLogs` — error and operation logging

> You can find table creation SQL scripts in your `.sql` or setup phase.

---

## 📌 Notes

- A member can borrow a max of 3 books at a time.
- Reservation status must be approved by staff.
- ISBN and username fields are unique.

---

## ✍️ Author

Developed by [@devberatzengin](https://github.com/devberatzengin)  
Feel free to contribute or fork the repo!

---

## 📄 License

This project is open-source and available under the MIT License.
