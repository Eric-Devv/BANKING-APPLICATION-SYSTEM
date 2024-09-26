import customtkinter as ctk
import sqlite3
from tkinter import messagebox


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
            messagebox.showerror("Error", "please enter a valid amount!")
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
        messagebox.showerror("Error", "Please enter the accounts holder's name.")


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
        messagebox.showerror("Error", "Please enter the account holder's name.")


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
app.geometry('500x500')

#labels and entry fields
label_name = ctk.CTkLabel(app, text = "Name:")
label_name.pack(pady =5)

entry_name = ctk.CTkEntry(app)
entry_name.pack(pady = 5)

label_new_name = ctk.CTkLabel(app, text = "New Name (for modification):")
label_new_name.pack(pady = 5)

entry_new_name = ctk.CTkEntry(app)
entry_new_name.pack(pady = 5)

label_amount = ctk.CTkLabel(app, text = "Amount:")
label_amount.pack(pady = 5)

entry_amount = ctk.CTkEntry(app)
entry_amount.pack(pady = 5)

#Buttons for actions
button_ceate_account = ctk.CTkButton(app, text="Create Account", command=create_account)
button_ceate_account.pack(pady =10)

button_deposit = ctk.CTkButton(app, text ="Deposit Cash", command=deposit)
button_deposit.pack(pady =10)

button_withdraw = ctk.CTkButton(app, text="Withdraw Cash", command=withdraw)
button_withdraw.pack(pady=10)

button_check_balance = ctk.CTkButton(app, text="Balance Enquiry", command=check_balance)
button_check_balance.pack(pady=10)

button_list_accounts = ctk.CTkButton(app, text="Account Holders List", command=list_accounts)
button_list_accounts.pack(pady=10)

button_close_account = ctk.CTkButton(app, text="Close Account", command=close_account)
button_close_account.pack(pady=10)

button_modify_account = ctk.CTkButton(app, text="Modify Account", command=modify_account)
button_modify_account.pack(pady=10)






app.mainloop()