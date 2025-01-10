import sqlite3
import random
class InvalidPin(Exception):
    ...

conn=sqlite3.connect('bank.db')
cursor=conn.cursor()

# cursor.execute("CREATE TABLE Upna_Bank (Name varchar(50),Phone number CHECK (Phone >= 1000000000 AND Phone <= 9999999999), Mail varchar(80),Account_No number,Balance number,Pin varchar(15))")
# conn.commit()

# cursor.execute("DELETE FROM Upna_Bank WHERE Name='Ramya';")
# conn.commit()

print()
print(f"{"*"*20} WELCOME TO SHIVA BANK 😍 ☺️☺️☺️☺️😍 {"*"*20}")
print()
print(f"{"-"*10}Belive in our self {"-"*10}")
print("please select your option .....")
print("1. Create new account")
print("2. Pin generation")
print("3. To Deposite money")
print("4. TO Widthdraw money")
print("5. To Transfer money")
print("6. To Check the Balance")
a=int(input('Please enter your option here : '))
if a==1:
    name=input("NAME: ")
    phone=int(input("PHONE NUMBER: "))
    mail=input("E-MAIL :")
    cursor.execute("SELECT MAX(Account_No) FROM Upna_Bank")
    max_account_no = cursor.fetchone()

    if max_account_no is None or max_account_no[0] is None:
        account_no = random.randint(100000000000, 999999999999)
    else:
        account_no = max_account_no[0] + 1
    cursor.execute("""
        INSERT INTO Upna_Bank (Name, Phone, Mail, Account_No)
        VALUES (?, ?, ?, ?)
        """, (name, phone, mail, account_no))
    conn.commit()
    print(f"congratulations  {name} 🥳🥳... \nYour Account is created successfully! Your account number is: {account_no}")
elif a==2:
    name=input("NAME: ")
    account_no=int(input("ACCOUNT NUMBER: "))
    pin=input('enter your 4 digit pin : ')
    if len(pin) == 4 and pin.isdigit() :
        cursor.execute("""
            UPDATE Upna_Bank 
            SET Pin = ? 
            WHERE Name = ? AND account_no = ?
            """, (pin, name, account_no))
        conn.commit()
        print("Pin Generation Done 👍")
    else:
        raise InvalidPin("Invalid PIN. Please enter a valid 4-digit number.")
elif a==3:
    print("Please enter valid details ....")
    account_no=int(input("Account_no NUMBER: "))
    pin=input('PIN : ')
    cursor.execute("""
    SELECT Balance FROM Upna_Bank WHERE account_no = ? and Pin = ?
    """, (account_no,pin))
    result = cursor.fetchone()
    balance = result[0]
    if balance is None:
        balance=0
        deposit = int(input('Enter the amount: '))
        balance+=deposit
        if deposit>=500:
            cursor.execute("""
                UPDATE Upna_Bank 
                SET Balance = ? 
                WHERE account_no = ? AND Pin = ?
            """, (balance, account_no, pin))
            conn.commit()
            print('You have successfully deposited your amount 🎉') 
elif a==4:
    print("Please enter valid details ....")
    account_no=int(input("PHONE Account_no: "))
    pin=input('PIN : ')
    cursor.execute("""
    SELECT Balance FROM Upna_Bank WHERE account_no = ? and Pin = ?
    """, (account_no,pin))
    result = cursor.fetchone()
    balance = result[0]
    withdrawel_amount=int(input("enter the amount : "))
    balance-=withdrawel_amount
    cursor.execute("""
                UPDATE Upna_Bank 
                SET Balance = ? 
                WHERE account_no = ? AND Pin = ?
            """, (balance, account_no, pin))
    conn.commit()
    print(f"you are sucessfully withdrawed your {withdrawel_amount} 🫣")
    print(f"your current balance is {balance}")
elif a==5:
    s_name=input(" SENDER NAME: ")
    s_account_no=int(input(" SENDER ACCOUNT NUMBER: "))
    r_name=input(" RECIPTENT NAME: ")
    r_account_no=int(input(" RECIPTENT ACCOUNT NUMBER: "))
    transfer_amount=int(input('enter the amount to be transfered : '))
    cursor.execute("""
    SELECT Balance FROM Upna_Bank WHERE Name = ? AND account_no = ? 
    """, (s_name, s_account_no))
    result = cursor.fetchone()
    balance=result[0]
    if balance is None:
        balance=0
    if balance<transfer_amount:
        print(" OOPS! your current balace is lesser than the transfer amount. ")
    else:
        balance-=transfer_amount
        cursor.execute("""
                UPDATE Upna_Bank 
                SET Balance = ? 
                WHERE account_no = ? AND Name = ?
            """, (balance, s_account_no,s_name))
        conn.commit()
        cursor.execute("""
    SELECT Balance FROM Upna_Bank WHERE Name = ? AND account_no = ? 
    """, (r_name, r_account_no))
        r_result = cursor.fetchone()
        r_balance=result[0]
        r_balance+=transfer_amount
        print(r_balance)
        cursor.execute("""
                UPDATE Upna_Bank 
                SET Balance = ? 
                WHERE account_no = ? AND Name = ?
            """, (r_balance, r_account_no,r_name))
        conn.commit()
elif a==6:
    print("Please enter valid details ....")
    name=input("NAME: ")
    account_no=int(input("ACCOUNT NUMBER: "))
    pin=input('PIN : ')
    cursor.execute("""
    SELECT Balance FROM Upna_Bank WHERE Name = ? AND account_no = ? and Pin = ?
    """, (name, account_no,pin))
    result = cursor.fetchone()
    if result:
        balance = result[0]
        print(balance)
        print(f"Your current balance is: {balance}")
    else:
        print("No matching record found. Please check your details.")
