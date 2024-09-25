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
            



























app = ctk.CTk()
app.title("BANKING APPLICATION")
app.geometry("630x230")









app.mainloop()