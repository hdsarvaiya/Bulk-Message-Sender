import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.parse

def send_message(driver, phone_number, message):
    print(f"Opening chat for phone number: {phone_number}")
    
    # URL encode the message
    encoded_message = urllib.parse.quote(message)
    
    # Open WhatsApp Web chat for the phone number
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
    driver.get(url)
    
    try:
        print(f"Waiting for chat to open for phone number: {phone_number}")
        # Wait for the chat to open and the send button to be visible
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox']"))
        )
        print(f"Chat opened for phone number: {phone_number}")
        
        print(f"Attempting to find send button for phone number: {phone_number}")
        # Wait for the send button to be clickable
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))
        )
        
        if send_button:
            print(f"Send button found and clickable for phone number: {phone_number}")
            # Click the send button
            send_button.click()
            print(f"Clicked send button for phone number: {phone_number}")
            
            # Wait to ensure the message is sent
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "span[data-icon='send']"))
            )
            print(f"Message sent to {phone_number}")
        else:
            print(f"Send button not found for phone number: {phone_number}")
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")

def send_messages():
    # Extract phone numbers and message from the GUI
    phone_numbers = phone_numbers_entry.get("1.0", tk.END).strip().split("\n")
    message = message_entry.get("1.0", tk.END).strip()

    if not phone_numbers or not message:
        messagebox.showerror("Error", "Please enter phone numbers and a message.")
        return
    
    print("Initializing Chrome WebDriver")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    print("Opening WhatsApp Web")
    driver.get('https://web.whatsapp.com')

    input("Press Enter after scanning the QR code and ensuring WhatsApp Web is fully loaded")

    for number in phone_numbers:
        print(f"Starting to send message to {number}")
        send_message(driver, number, message)
        print(f"Waiting 2 seconds before sending next message")
        time.sleep(2)  # Small delay to avoid rate limiting

    print("All messages sent. Closing browser.")
    driver.quit()

# Create the GUI window
root = tk.Tk()
root.title("WhatsApp Message Sender")

# Create and place labels and text boxes
tk.Label(root, text="Phone Numbers (one per line):").grid(row=0, column=0, padx=10, pady=10)
phone_numbers_entry = tk.Text(root, height=10, width=30)
phone_numbers_entry.grid(row=1, column=0, padx=10, pady=10)

tk.Label(root, text="Message:").grid(row=0, column=1, padx=10, pady=10)
message_entry = tk.Text(root, height=10, width=30)
message_entry.grid(row=1, column=1, padx=10, pady=10)

# Create and place the Send button
send_button = tk.Button(root, text="Send Message", command=send_messages)
send_button.grid(row=2, column=0, columnspan=2, pady=20)

# Start the GUI loop
root.mainloop()
