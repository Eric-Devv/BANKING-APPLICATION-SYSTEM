import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from tkinter import ttk


# database initialization
def init_db():
    conn = sqlite3.connect("Bank.db")
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS accounts
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   name TEXT NOT NULL, 
                   balance REAL NOT NULL)''')
    
    conn.commit()
    conn.close()


#creating new account
def create_account():
    name = entry_name.get()
    initial_deposit = entry_amount.get()

    if name and initial_deposit:
        try:
            initial_deposit = float(initial_deposit)
            conn = sqlite3.connect('Bank.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO accounts(name, balance) VALUES (?,?)",(name, initial_deposit))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success','Account created successfully!')
            clear_entries()
        except ValueError:
            messagebox.showerror("Error", "please enter full details")
    else:
        messagebox.showerror('Error','Please fill out the entries.')


# Deposit money to account
def deposit():
    name = entry_name.get()
    deposit_amount = entry_amount.get()

    if name and deposit_amount:
        try:
            deposit_amount = float(deposit_amount)
            conn = sqlite3.connect('Bank.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE accounts SET balance = balance + ? WHERE name = ?',(deposit_amount,name))
            conn.commit()
            conn.close()

            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Account not found.")
            else:
                messagebox.showinfo("Success", "Deposit successful!")
            
            clear_entries()
        except ValueError:
            messagebox.showerror('Error', "Please the correct infomation.")
    
    else:
        messagebox.showerror("Error","Please insert all fields.")


# withdraw money
def withdraw():
    name = entry_name.get()
    withdraw_amount = entry_amount.get()

    if name and withdraw_amount:
        try:
            withdraw_amount = float(withdraw_amount)
            conn = sqlite3.connect("Bank.db")
            conn = conn.cursor()
            cursor.execute("SELECT balance FROM accounts WHERE name =?",(name,))
            result = cursor.fetchone()
            
            if result:
                balance = result[0]
                if balance >= withdraw_amount:
                    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE name = ?",(name, withdraw_amount))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Success', "Withdrawal successful!")
                
                else:
                    messagebox.showerror("Error","Insufficient funds.")
            else:
                messagebox.showerror("Error","Account not found.")
        except ValueError:
            messagebox.showerror("Error","Please fill out all fields.")


#Balance enquiry...
def check_balance():
    name = entry_name.get()

    if name:
        conn = sqlite3.connect("Bank.db")
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE name = ?",(name,))
        result = cursor.fetchone
        conn.close()

        if result:
            balance = result[0]
            messagebox.showinfo("balance",f"The balance for {name} is {balance:.2f}")
        else:
            messagebox.showerror("Error", "Account not found.")
    else:
        messagebox.showerror("Error", "Please enter the account number.")


# List all account holders
def list_accounts():
    conn = sqlite3.connect("Bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM accounts")
    accounts = cursor.fetchall()
    conn.close()

    if accounts:
        account_list = "\n".join([account[0]for account in accounts])
        messagebox.showinfo("Account Holders", account_list)

    else:
        messagebox.showinfo("Account Holders","No account found.")


#Close an account
def close_account():
    name = entry_name.get()

    if name:
        conn =sqlite3.connect("Bank.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE name = ?", (name,))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Account not found!")
        else:
            messagebox.showinfo("Success","Account closed succesfully.")
        clear_entries()

    else:
        messagebox.showerror("Error", "Please enter the account details!")


#Modify Account (name/balance)
def modify_account():
    name = entry_name.get()
    new_name = entry_new_name.get()
    new_balance  = entry_amount.get()

    if name and (new_name or new_balance):
        conn = sqlite3.connect("Bank.db")
        cursor = conn.cursor()
        
        if new_name:
            cursor.execute("UPDATE accounts SET balance = ? WHERE name = ?", (new_balance,new_name))
        
        if new_balance:
            try:
                new_balance = float(new_balance)
                cursor.execute("UPDATE accounts SET balance = ? WHERE name = ?",(new_balance, name))
            except ValueError:
                messagebox.showerror("Error", "please enter a valid amount.")
                return
            
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            messagebox.showerror('Error',"Account not found.")
        else:
            messagebox.showinfo('Success', "Account updated successfully")
        clear_entries()

    else:
        messagebox.showerror('Error', "Please fill in the required fields")


#clear all entry fields
def clear_entries():
    entry_name.delete(0, ctk.END)
    entry_new_name.delete(0, ctk.END)
    entry_amount.delete(0, ctk.END)

#initialize the database
init_db()


#Creating the main app window
app = ctk.CTk()
app.title("BANKING APPLICATION SOFTWARE")
app.geometry('810x400')
app.resizable('false','false')

tab_view = ctk.CTkTabview(app, width=800, height=500)
tab_view.pack(pady=0, padx=0)

# Add tabs
tab_view.add("Create Account")  
tab_view.add("Deposit")  
tab_view.add("Withdraw") 
tab_view.add("Account Modification")
tab_view.add("List Accounts")  


tab_view.set("List Accounts") 

# Create Account tab
label_name = ctk.CTkLabel(master=tab_view.tab("Create Account"), text="Full Name:")
label_name.place(x=1, y=5)

entry_name = ctk.CTkEntry(master=tab_view.tab("Create Account"))
entry_name.pack(pady=7)

label_account_number = ctk.CTkLabel(master=tab_view.tab("Create Account"), text="Account Number:")
label_account_number.place(x=1, y=48)

entry_account_number = ctk.CTkEntry(master=tab_view.tab("Create Account"))
entry_account_number.pack(pady=7)

label_phone_number = ctk.CTkLabel(master=tab_view.tab("Create Account"), text="Phone Number:")
label_phone_number.place(x=1, y=89)

entry_phone_number = ctk.CTkEntry(master=tab_view.tab("Create Account"))
entry_phone_number.pack(pady=7)

label_email_address = ctk.CTkLabel(master=tab_view.tab("Create Account"), text="Email Address:")
label_email_address.place(x=1, y=128)

entry_email_address = ctk.CTkEntry(master=tab_view.tab("Create Account"))
entry_email_address.pack(pady=7)

def option_changed(selected_option):
    print(f"Selected option: {selected_option}")
    label.config(text=f"You selected: {selected_option}")

# Create a label
label = ctk.CTkLabel(master=tab_view.tab("Create Account"), text="Gender:")
label.place(x=1,y=180)

# Create the dropdown (OptionMenu)
options = ["MALE", "FEMALE"]
dropdown = ctk.CTkOptionMenu(master=tab_view.tab("Create Account"), values=options, command=option_changed)
dropdown.pack(pady=20)

# Set default value for the dropdown
dropdown.set("Select Gender")  # Default label

button_create_account = ctk.CTkButton(master=tab_view.tab("Create Account"), text="Create Account", )
button_create_account.place(x=580,y=70)


# Deposit tab
label_name = ctk.CTkLabel(master=tab_view.tab("Deposit"), text="Full Name:")
label_name.place(x=1, y=5)

entry_name = ctk.CTkEntry(master=tab_view.tab("Deposit"))
entry_name.pack(pady=7)

label_account_number = ctk.CTkLabel(master=tab_view.tab("Deposit"), text="Account Number:")
label_account_number.place(x=1, y=48)

entry_account_number = ctk.CTkEntry(master=tab_view.tab("Deposit"))
entry_account_number.pack(pady=7)

label_amount = ctk.CTkLabel(master=tab_view.tab("Deposit"), text="Amount:")
label_amount.place(x=1, y=89)

entry_amount = ctk.CTkEntry(master=tab_view.tab("Deposit"))
entry_amount.pack(pady=17)

button_create_account = ctk.CTkButton(master=tab_view.tab("Deposit"), text="DEPOSIT", )
button_create_account.place(x=580,y=40)

button_create_account = ctk.CTkButton(master=tab_view.tab("Deposit"), text="CHECK BALANCE", command=check_balance )
button_create_account.place(x=580,y=90)

#WITHDRAWALS
label_name = ctk.CTkLabel(master=tab_view.tab("Withdraw"), text="Full Name:")
label_name.place(x=1, y=5)

entry_name = ctk.CTkEntry(master=tab_view.tab("Withdraw"))
entry_name.pack(pady=7)

label_account_number = ctk.CTkLabel(master=tab_view.tab("Withdraw"), text="Account Number:")
label_account_number.place(x=1, y=48)

entry_account_number = ctk.CTkEntry(master=tab_view.tab("Withdraw"))
entry_account_number.pack(pady=7)

label_amount = ctk.CTkLabel(master=tab_view.tab("Withdraw"), text="Amount:")
label_amount.place(x=1, y=89)

entry_amount = ctk.CTkEntry(master=tab_view.tab("Withdraw"))
entry_amount.pack(pady=17)

button_create_account = ctk.CTkButton(master=tab_view.tab("Withdraw"), text="WITHDRAW", )
button_create_account.place(x=580,y=40)

button_create_account = ctk.CTkButton(master=tab_view.tab("Withdraw"), text="CHECK BALANCE", command=check_balance )
button_create_account.place(x=580,y=90)


#Account modification
label_name = ctk.CTkLabel(master=tab_view.tab("Account Modification"), text="Full Name:")
label_name.place(x=1, y=5)

entry_name = ctk.CTkEntry(master=tab_view.tab("Account Modification"))
entry_name.pack(pady=7)

label_account_number = ctk.CTkLabel(master=tab_view.tab("Account Modification"), text="Account Number:")
label_account_number.place(x=1, y=48)

entry_account_number = ctk.CTkEntry(master=tab_view.tab("Account Modification"))
entry_account_number.pack(pady=7)

button_create_account = ctk.CTkButton(master=tab_view.tab("Account Modification"), text="CHANGE DETAILS", command=modify_account )
button_create_account.place(x=580,y=20)

button_close_account = ctk.CTkButton(master=tab_view.tab("Account Modification"), text="CLOSE ACCOUNT", command=close_account)
button_close_account.place(x=320,y=127)


#LIST ACCOUNTS
button_list_accounts = ctk.CTkButton(master=tab_view.tab("List Accounts"), text="All Account Holder List", command=list_accounts)
button_list_accounts.pack(pady=40)














app.mainloop()