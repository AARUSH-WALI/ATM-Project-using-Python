import os
import time
import qrcode
import pygame
import random
import smtplib
from email.message import EmailMessage

pygame.mixer.init()

# Define the file path for storing account data
file_path = "accounts.txt"

# Function to load existing accounts
def load_accounts():
    accounts = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(',')
                # Check if the line contains all the necessary account information
                if len(data) == 5:
                    account = {
                        'Name':data[0],
                        'Account Number': data[1],
                        'PIN': data[2],
                        'Balance': float(data[3]),
                        'Email': data[4]
                    }
                    accounts.append(account)
                else:
                    print(f"Issue with data in the accounts file: {line.strip()}")
    return accounts


# Function to save accounts to file
def save_accounts(accounts):
    with open(file_path, 'w') as file:
        for acc in accounts:
            file.write(f"{acc['Name']},{acc['Account Number']},{acc['PIN']},{acc['Balance']},{acc['Email']}\n")



# Function to create a new account
def create_account():
    acc_holder_name=input("Enter your name")
    account_number = input("Enter your account number: ")
    receiver_email=input("Enter the Email address")
    a=1
    while(a):
        pin = str(input("Enter your PIN: "))
        while(len(pin) != 4):
            print("\t\t\tOnly 4 digit pin is applicable.")
            pin = str(input("Enter your PIN: "))
                
        pin1 = str(input("Confirm Pin : "))    
        while(len(pin1) != 4):
            print("Only 4 digit pin is applicable.")
            pin1 = str(input("Confirm Pin : "))
            
        if pin1==pin:
            a=0
        else:
            a=1
            print("Pin doesnot match")
            
    
    balance = 5000
    accounts = load_accounts()
    accounts.append({'Name': acc_holder_name,'Account Number': account_number, 'PIN': pin, 'Balance': balance, 'Email': receiver_email})
    save_accounts(accounts)
    time.sleep(2)
    print("Amount Of 5000 Credited to your account.")
    time.sleep(2)
    print("Account created successfully.")
    time.sleep(1.5)





# Function to generate OTP
def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp_email(account, otp):
    sender_email = "aarushwali12@gmail.com"  # Update with your email
    password = "mprx njix bbgc ptsc"  # Update with your password

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = account['Email']
    msg.set_content(f"Dear {account['Name']},\n\nYour OTP is: {otp}\n\nThank you!")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)

def verify_otp(account):
    otp = generate_otp()
    send_otp_email(account, otp)

    entered_otp = input("Enter the OTP sent to your email: ")

    if entered_otp == otp:
        print("OTP verification successful.")
        return True
    else:
        print("Invalid OTP. Please try again.")
        return False

# Function to login with OTP for users under 18
def login_with_otp():
    account_number = input("Enter your account number: ")
    age = int(input("Enter your age: "))
    if age < 18:
        accounts = load_accounts()
        account = next((acc for acc in accounts if acc['Account Number'] == account_number), None)
        
        if account:
            if verify_otp(account):
                return account
            else:
                return None
        else:
            print("Account not found.")
            return None
    else:
        return login()


        
# Function to login
def login():
    attempts = 0
    while attempts < 3:
        account_number = input("Enter your account number: ")
        pin = input("Enter your PIN: ")
        
        accounts = load_accounts()
        account = next((acc for acc in accounts if acc['Account Number'] == account_number and acc['PIN'] == pin), None)

        if account:
            
            print("                         LOADING ",end='')
            time.sleep(1)
            sound = pygame.mixer.Sound('1700793962108tbn11bhn-voicemaker.in-speech.WAV')
            # Play the sound effect
            sound.play()
            print("PLEASE ",end='')
            time.sleep(1)
            print("WAIT",end='')
            time.sleep(1)
            print("..",end='')
            time.sleep(1)
            print("..",end='')
            time.sleep(1)
            print("..",)
            
            time.sleep(1)
            print("                             LOGIN SUCCESSFUL",end='')
            time.sleep(2)
            return account
        else:
            attempts += 1
            remaining_attempts = 3 - attempts
            if remaining_attempts > 0:
                print(f"Invalid account number or PIN. {remaining_attempts} attempts remaining.")
            else:
                print("Three unsuccessful attempts. Exiting.")
                accounts = load_accounts()
                account = next((acc for acc in accounts if acc['Account Number'] == account_number), None)
                if account:
                    accounts.remove(account)
                    save_accounts(accounts)
                    print(f"Account {account_number} has been deleted.")
                else:
                    print(f"Account {account_number} not found.")
                print("                     Your Account is Blocked")
                print("           Please visit your nearest Branch of your bank")
                print()
                
                return None
    return None
    
# Function to perform balance inquiry
def balance_inquiry(account):
    print(f"Account Number: {account['Account Number']}")
    print(f"Balance: {account['Balance']}")

# Function to perform a deposit
def deposit(account):
    amount = float(input("Enter the amount to deposit: "))
    if amount%100!=0:
        print("Amount should be in multiple of 100")
    if amount > 100000:
        print("Maximum 100000 rupees can be deposited at once.")
    else:
        account['Balance'] += amount
        save_accounts([account])
        sound = pygame.mixer.Sound('1700850368570nwdvxell-voicemaker.in-speech.WAV')
        # Play the sound effect
        sound.play()
        send_email_notification_dep(account,amount)
        
        print("                  =================================================")
        print("                  =              Transaction Receipt              =")
        print("                  =================================================")
        print(f"                  =  Account Holder: {account['Name']}                  =")
        print(f"                  =  Account Number: {account['Account Number']}                         =")
        print(f"                  =  Deposit amount: {amount}                      =")
        print(f"                  =  New Balance: {account['Balance']}                        =")
        print("                  =================================================")


# Function to perform a withdrawal
def withdraw(account):
    amount = float(input("Enter the amount to withdraw: "))
    if amount % 100 != 0:
        print("Amount should be in multiples of 100")
        return  # Exit the function if the amount is not in multiples of 100

    if amount > account['Balance']:
        print("Insufficient funds.")
        return
    
    if amount > 50000:
        print("Can't Withdraw more than 50000 rupees at a time")
        return

    # Introduce the penalty calculation
    if account['Balance'] < 5000:
        penalty = amount * 0.0112  # 1.12% penalty
        print(f"A penalty of {penalty} will be deducted from your account due to low balance.")
        account['Balance'] -= penalty

    account['Balance'] -= amount
    save_accounts([account])
    send_email_notification_withd(account, amount)
    # Your sound effects and email notification functions here
    sound = pygame.mixer.Sound('96165-Atm_machine_distribute_cash-BLASTWAVEFX-30797 (1).WAV')
    sound.play()
    sound = pygame.mixer.Sound('1700850397028ol1dyv1u-voicemaker.in-speech.WAV')
    # Display transaction receipt
    print("                  =================================================")
    print("                  =              Transaction Receipt              =")
    print("                  =================================================")
    print(f"                  =  Account Holder: {account['Name']}                  =")
    print(f"                  =  Account Number: {account['Account Number']}                         =")
    print(f"                  =  Withdrawal amount: {amount}                      =")
    print(f"                  =  New Balance: {account['Balance']}                        =")
    print("                  =================================================")

    # Function to calculate denominations
    calculate_denominations(amount)


def calculate_denominations(amount):
    denominations = [2000, 500, 200, 100]  # Different currency denominations
    notes = {}

    for denom in denominations:
        if amount >= denom:
            count = amount // denom
            notes[denom] = count
            amount -= count * denom

    print("Denominations:")
    for note, count in notes.items():
        print(f"{note} : {count}")


# Function to perform an online money transfer
def online_transfer(account):
    print("                           Transfer money with any method")
    print("                      =========================================")
    print("                      =1.Transfer money using UPI             =")
    print("                      =2.Transfer money using Mobile Number   =")
    print("                      =3.Transfer money using QR Code         =")
    print("                      =========================================")
    choicee=int(input("Select the Option"))
    if choicee==1:
        upi=input("Enter UPI ID");
        amount = float(input("Enter the amount to transfer online: "))
        if amount > account['Balance']:
            print("Insufficient funds.")
        else:
            if account['Balance'] < 5000:
                penalty = amount * 0.0112  # 1.12% penalty
                print(f"A penalty of {penalty} will be deducted from your account due to low balance.")
                account['Balance'] -= penalty

            account['Balance'] -= amount
            save_accounts([account])
            send_email_notification_withd(account,amount)
            print(f"Transfer of {amount} successful. New balance: {account['Balance']}")

    if choicee==2:
        mobile=input("Enter Mobile Number")
        amount = float(input("Enter the amount to transfer online: "))
        if amount > account['Balance']:
            print("Insufficient funds.")
        else:
            if account['Balance'] < 5000:
                penalty = amount * 0.0112  # 1.12% penalty
                print(f"A penalty of {penalty} will be deducted from your account due to low balance.")
                account['Balance'] -= penalty
            account['Balance'] -= amount
            save_accounts([account])
            send_email_notification_withd(account,amount)
            print(f"Transfer of {amount} successful. New balance: {account['Balance']}")
    if choicee==3:
        print("                          ========================")
        print("                         |      1. Saksham        |")
        print("                         |      2. Aarush         |")
        print("                         |      3. Other          |")
        print("                          ========================")
        choice = str(input("Enter the command : "))
        if choice == '1':
             # Open an image file
            image_path = "D:\\sakshamqrcode.jpg"
            img = Image.open(image_path)
            # Display image (optional)
            img.show()
        if choice == '2':
            # Open an image file
            image_path = "E:\\aarushqrcode.jpg"
            img = Image.open(image_path)
            # Display image (optional)
            img.show()
        if choice == '3':
            img = qrcode.make("https://me-qr.com/text/4359904/show")
            img.save("saksham.jpg")
            img.show("saksham.jpg")  

#Function to remove an existing account
def delete_account(account):
    account_number = input("Enter the account number to delete: ")
    accounts = load_accounts()
    account = next((acc for acc in accounts if acc['Account Number'] == account_number), None)

    if account:
        accounts.remove(account)
        save_accounts(accounts)
        print(f"Account {account_number} has been deleted.")
    else:
        print(f"Account {account_number} not found.")




def send_email_notification_dep(account,amount):
    sender_email = "aarushwali12@gmail.com"  
    
    password = "mprx njix bbgc ptsc" 

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = account['Email']

    # Crafting email body
    msg.set_content(f"Dear {account['Name']},\n\ndeposit of rupees {amount} has been made.\n\nAccount Number: {account['Account Number']}\nNew Balance: {account['Balance']}\n\nThank you!")

    # Establishing a connection to the SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)

def send_email_notification_withd(account,amount):
    sender_email = "aarushwali12@gmail.com"  
    
    password = "mprx njix bbgc ptsc" 

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = account['Email']

    # Crafting email body
    msg.set_content(f"Dear {account['Name']},\n\nWithdrawl of rupees {amount} has been made.\n\nAccount Number: {account['Account Number']}\nNew Balance: {account['Balance']}\n\nThank you!")

    # Establishing a connection to the SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)


# Main function
def main():
    print("                     "+"="*33)
    print("                     Welcome to the ATM Banking System")
    print("                     "+"="*33)
    while True:
        print()
        print("                         Hello, how may i help you")
        print("                         ==========================")
        print("                         =   1. Create Account    =")
        print("                         =   2. Login             =")
        print("                         =   3. Quit              =")
        print("                         ==========================")
        sound = pygame.mixer.Sound('1700793544245lk1850c-voicemaker.in-speech.WAV')
        # Play the sound effect
        sound.play()
        choice = input("Enter your choice: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            age = int(input("Enter your age: "))
            if age < 18:
                account = login_with_otp()
            else:
                account = login()
                
            if account:
                while True:
                    sound = pygame.mixer.Sound('1700794137279l6x0awy-voicemaker.in-speech.WAV')
                    # Play the sound effect
                    sound.play()
                    print("                                \nOptions:")
                    print("                          ==========================")
                    print("                          = 1. Balance Inquiry     =")
                    print("                          = 2. Deposit             =")
                    print("                          = 3. Withdraw            =")
                    print("                          = 4. Online Transaction  =")
                    print("                          = 5. Remove Account      =")
                    print("                          = 6. Logout              =")
                    print("                          ==========================")

                    choice = input("Enter your choice: ")

                    if choice == '1':
                        balance_inquiry(account)
                    elif choice == '2':
                        deposit(account)
                    elif choice == '3':
                        withdraw(account)
                    elif choice == '4':
                        online_transfer(account)
                    elif choice == '5':
                        delete_account(account)
                    elif choice == '6':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid account number or PIN. Please try again.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
