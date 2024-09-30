import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# Database initialization
def init_db():
    conn = sqlite3.connect("Bank.db")
    cursor = conn.cursor()
    # Drop the accounts table if it exists
    cursor.execute("DROP TABLE IF EXISTS accounts")
    # Create the accounts table
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                      accountnumber INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      email TEXT NOT NULL,
                      phone INTEGER NOT NULL,
                      gender TEXT NOT NULL,
                      balance REAL DEFAULT 0)''')
    conn.commit()
    conn.close()

# Creating a new account
def create_account():
    name = entry_name.get()
    account_number = entry_account_number.get()
    phone_number = entry_phone_number.get()
    email_address = entry_email_address.get()
    gender = entry_gender.get()

    if all([name, account_number, phone_number, email_address, gender]):
        try:
            account_number = int(account_number)
            phone_number = int(phone_number)
            conn = sqlite3.connect('Bank.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO accounts (accountnumber, name, email, phone, gender) VALUES (?, ?, ?, ?, ?)",
                           (account_number, name, email_address, phone_number, gender))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Account created successfully!')
            clear_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Account number already exists.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid details.")
    else:
        messagebox.showerror('Error', 'Please fill out all fields.')

# Deposit money to account
def deposit():
    account_number = entry_account_number_deposit.get()
    deposit_amount = entry_amount.get()

    if account_number and deposit_amount:
        try:
            deposit_amount = float(deposit_amount)
            conn = sqlite3.connect('Bank.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE accounts SET balance = balance + ? WHERE accountnumber = ?', (deposit_amount, account_number))
            conn.commit()
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Account not found.")
            else:
                messagebox.showinfo("Success", "Deposit successful!")
            conn.close()
            clear_entries()
        except ValueError:
            messagebox.showerror('Error', "Please enter a valid amount.")
    else:
        messagebox.showerror("Error", "Please fill out all fields.")

# Withdraw money
def withdraw():
    account_number = entry_account_number_withdraw.get()
    withdraw_amount = entry_amount.get()

    if account_number and withdraw_amount:
        try:
            withdraw_amount = float(withdraw_amount)
            conn = sqlite3.connect("Bank.db")
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM accounts WHERE accountnumber = ?", (account_number,))
            result = cursor.fetchone()

            if result:
                balance = result[0]
                if balance >= withdraw_amount:
                    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE accountnumber = ?", (withdraw_amount, account_number))
                    conn.commit()
                    messagebox.showinfo('Success', "Withdrawal successful!")
                else:
                    messagebox.showerror("Error", "Insufficient funds.")
            else:
                messagebox.showerror("Error", "Account not found.")
            conn.close()
            clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

# Balance enquiry
def check_balance():
    account_number = entry_account_number_balance.get()

    if account_number:
        conn = sqlite3.connect("Bank.db")
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE accountnumber = ?", (account_number,))
        result = cursor.fetchone()
        conn.close()

        if result:
            balance = result[0]
            messagebox.showinfo("Balance", f"The balance for account number {account_number} is {balance:.2f}")
        else:
            messagebox.showerror("Error", "Account not found.")
    else:
        messagebox.showerror("Error", "Please enter the account number.")

# List all account holders
def list_accounts():
    conn = sqlite3.connect("Bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, accountnumber FROM accounts")
    accounts = cursor.fetchall()
    conn.close()

    if accounts:
        account_list = "\n".join([f"{account[0]} (Account Number: {account[1]})" for account in accounts])
        messagebox.showinfo("Account Holders", account_list)
    else:
        messagebox.showinfo("Account Holders", "No accounts found.")

# Close an account
def close_account():
    account_number = entry_account_number_close.get()

    if account_number:
        conn = sqlite3.connect("Bank.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE accountnumber = ?", (account_number,))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Account not found!")
        else:
            messagebox.showinfo("Success", "Account closed successfully.")
        clear_entries()
    else:
        messagebox.showerror("Error", "Please enter the account number!")

# Modify Account (name)
def modify_account():
    account_number = entry_account_number_modify.get()
    new_name = entry_New_name.get()

    if account_number and new_name:
        conn = sqlite3.connect("Bank.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET name = ? WHERE accountnumber = ?", (new_name, account_number))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            messagebox.showerror('Error', "Account not found.")
        else:
            messagebox.showinfo('Success', "Account updated successfully.")
        clear_entries()
    else:
        messagebox.showerror('Error', "Please fill in the required fields.")

# Clear all entry fields
def clear_entries():
    entry_name.delete(0, ctk.END)
    entry_account_number.delete(0, ctk.END)
    entry_phone_number.delete(0, ctk.END)
    entry_email_address.delete(0, ctk.END)
    entry_gender.delete(0, ctk.END)
    entry_amount.delete(0, ctk.END)
    entry_New_name.delete(0, ctk.END)

# Initialize the database
init_db()

# Creating the main app window
app = ctk.CTk()
app.title("BANKING APPLICATION SOFTWARE")
app.geometry('810x380')
app.resizable('false', 'false')

tab_view = ctk.CTkTabview(app, width=800, height=370)
tab_view.pack(pady=0, padx=0)

# Add tabs
tab_view.add("Create Account")  
tab_view.add("Deposit")  
tab_view.add("Withdraw") 
tab_view.add("Account Modification")
tab_view.add("List Accounts")  
tab_view.add("Close Account")  # Added Close Account tab

tab_view.set("List Accounts") 

# Create Account tab
label_name = ctk.CTkLabel(master=tab_view.tab("Create Account"), text="Full Name:")
label_name.place(x=1, y=5)
entry_name = ctk.CTkEntry(master=tab_view.tab("Create Account"), fg_color='white', text_color='black')
entry_name.pack(pady=7)

label_account_number = ctk.CTkLabel(master=tab_view.tab("Create Account"), text="Account Number:")
label_account_number.place(x=1, y=48)
entry_account_number = ctk.CTkEntry(master=tab_view.tab("Create Account"), fg_color='white', text_color='black')
entry_account_number.pack(pady=7)

label_phone_number = ctk.CTkLabel(master=tab_view.tab("Create Account"), text="Phone Number:")
label_phone_number.place(x=1, y=89)
entry_phone_number = ctk.CTkEntry(master=tab_view.tab("Create Account"), fg_color='white', text_color='black')
entry_phone_number.pack(pady=7)

label_email_address = ctk.CTkLabel(master=tab_view.tab("Create Account"), text="Email Address:")
label_email_address.place(x=1, y=130)
entry_email_address = ctk.CTkEntry(master=tab_view.tab("Create Account"), fg_color='white', text_color='black')
entry_email_address.pack(pady=7)

label_gender = ctk.CTkLabel(master=tab_view.tab("Create Account"), text="Gender:")
label_gender.place(x=1, y=171)
entry_gender = ctk.CTkEntry(master=tab_view.tab("Create Account"), fg_color='white', text_color='black')
entry_gender.pack(pady=7)

button_create_account = ctk.CTkButton(master=tab_view.tab("Create Account"), text="Create Account", command=create_account)
button_create_account.place(x=580, y=210)

# Deposit tab
label_account_number_deposit = ctk.CTkLabel(master=tab_view.tab("Deposit"), text="Account Number:")
label_account_number_deposit.place(x=1, y=5)
entry_account_number_deposit = ctk.CTkEntry(master=tab_view.tab("Deposit"), fg_color='white', text_color='black')
entry_account_number_deposit.pack(pady=7)

label_amount_deposit = ctk.CTkLabel(master=tab_view.tab("Deposit"), text="Amount:")
label_amount_deposit.place(x=1, y=48)
entry_amount = ctk.CTkEntry(master=tab_view.tab("Deposit"), fg_color='white', text_color='black')
entry_amount.pack(pady=7)

button_deposit = ctk.CTkButton(master=tab_view.tab("Deposit"), text="Deposit", command=deposit)
button_deposit.place(x=580, y=70)

# Withdraw tab
label_account_number_withdraw = ctk.CTkLabel(master=tab_view.tab("Withdraw"), text="Account Number:")
label_account_number_withdraw.place(x=1, y=5)
entry_account_number_withdraw = ctk.CTkEntry(master=tab_view.tab("Withdraw"), fg_color='white', text_color='black')
entry_account_number_withdraw.pack(pady=7)

label_amount_withdraw = ctk.CTkLabel(master=tab_view.tab("Withdraw"), text="Amount:")
label_amount_withdraw.place(x=1, y=48)
entry_amount_withdraw = ctk.CTkEntry(master=tab_view.tab("Withdraw"), fg_color='white', text_color='black')
entry_amount_withdraw.pack(pady=7)

button_withdraw = ctk.CTkButton(master=tab_view.tab("Withdraw"), text="Withdraw", command=withdraw)
button_withdraw.place(x=580, y=70)

# Modify Account tab
label_account_number_modify = ctk.CTkLabel(master=tab_view.tab("Account Modification"), text="Account Number:")
label_account_number_modify.place(x=1, y=5)
entry_account_number_modify = ctk.CTkEntry(master=tab_view.tab("Account Modification"), fg_color='white', text_color='black')
entry_account_number_modify.pack(pady=7)

label_new_name = ctk.CTkLabel(master=tab_view.tab("Account Modification"), text="New Name:")
label_new_name.place(x=1, y=48)
entry_New_name = ctk.CTkEntry(master=tab_view.tab("Account Modification"), fg_color='white', text_color='black')
entry_New_name.pack(pady=7)

button_modify_account = ctk.CTkButton(master=tab_view.tab("Account Modification"), text="Modify Account", command=modify_account)
button_modify_account.place(x=580, y=70)

# List Accounts tab
button_list_accounts = ctk.CTkButton(master=tab_view.tab("List Accounts"), text="List Accounts", command=list_accounts)
button_list_accounts.pack(pady=70)

# Close Account tab
label_account_number_close = ctk.CTkLabel(master=tab_view.tab("Close Account"), text="Account Number:")
label_account_number_close.place(x=1, y=5)
entry_account_number_close = ctk.CTkEntry(master=tab_view.tab("Close Account"), fg_color='white', text_color='black')
entry_account_number_close.pack(pady=7)

button_close_account = ctk.CTkButton(master=tab_view.tab("Close Account"), text="Close Account", command=close_account)
button_close_account.place(x=580, y=70)

# Balance Enquiry
label_account_number_balance = ctk.CTkLabel(master=tab_view.tab("Deposit"), text="Account Number:")
label_account_number_balance.place(x=1, y=130)
entry_account_number_balance = ctk.CTkEntry(master=tab_view.tab("Deposit"), fg_color='white', text_color='black')
entry_account_number_balance.pack(pady=7)

button_check_balance = ctk.CTkButton(master=tab_view.tab("Deposit"), text="Check Balance", command=check_balance)
button_check_balance.place(x=580, y=170)

# Run the application
app.mainloop()
