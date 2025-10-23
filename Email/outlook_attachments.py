#!/usr/bin/env python3
"""
Mac Outlook.com Image Attachment Downloader with GUI
- Downloads only image attachments (JPG, PNG, GIF) from Inbox
- Skips inline images
- Handles duplicate filenames
- Zips all images into a single file
"""

import imaplib
import email
import os
import zipfile
import shutil
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
import threading
import sys

# ===== SETTINGS =====
IMAP_SERVER = "outlook.office365.com"
OUTPUT_DIR = "outlook_temp_attachments"
ZIP_FILENAME = "outlook_image_attachments.zip"
FOLDER = "Inbox"
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif")

# ===== HELPER FUNCTIONS =====
def download_attachments(email_address, app_password, log_var):
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        seen_filenames = {}
        total_count = 0

        log_var.set("Connecting to Outlook...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(email_address, app_password)
        mail.select(FOLDER)

        log_var.set("Searching emails in Inbox...")
        result, data = mail.search(None, "ALL")
        if result != "OK":
            messagebox.showerror("Error", "Failed to search Inbox")
            return

        ids = data[0].split()
        log_var.set(f"Found {len(ids)} emails. Processing attachments...")

        for num in ids:
            res, msg_data = mail.fetch(num, "(RFC822)")
            if res != "OK":
                continue
            msg = email.message_from_bytes(msg_data[0][1])

            for part in msg.walk():
                # Only true attachments
                if part.get_content_disposition() == "attachment":
                    filename = part.get_filename()
                    if filename and filename.lower().endswith(IMAGE_EXTENSIONS):
                        safe_name = filename
                        counter = 1
                        while safe_name in seen_filenames:
                            dot = filename.rfind(".")
                            if dot > 0:
                                safe_name = f"{filename[:dot]}_{counter}{filename[dot:]}"
                            else:
                                safe_name = f"{filename}_{counter}"
                            counter += 1
                        seen_filenames[safe_name] = True

                        filepath = os.path.join(OUTPUT_DIR, safe_name)
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        total_count += 1
                        log_var.set(f"Downloaded: {safe_name} ({total_count})")
        
        mail.logout()

        # ZIP files
        log_var.set("Zipping attachments...")
        with zipfile.ZipFile(ZIP_FILENAME, "w") as zipf:
            for file in os.listdir(OUTPUT_DIR):
                zipf.write(os.path.join(OUTPUT_DIR, file), arcname=file)

        # Cleanup
        shutil.rmtree(OUTPUT_DIR)
        log_var.set(f"✅ Done! {total_count} images downloaded and zipped into '{ZIP_FILENAME}'")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        log_var.set("Error occurred.")

# ===== GUI SETUP =====
def start_download():
    email_address = email_var.get().strip()
    app_password = password_var.get().strip()
    if not email_address or not app_password:
        messagebox.showwarning("Input required", "Please enter email and app password")
        return
    # Run in separate thread to avoid freezing GUI
    threading.Thread(target=download_attachments, args=(email_address, app_password, log_var)).start()

root = Tk()
root.title("Outlook Image Attachment Downloader")
root.geometry("500x200")

Label(root, text="Outlook Email Address:").pack(pady=5)
email_var = StringVar()
Entry(root, textvariable=email_var, width=50).pack(pady=5)

Label(root, text="App-specific Password:").pack(pady=5)
password_var = StringVar()
Entry(root, textvariable=password_var, show="*", width=50).pack(pady=5)

Button(root, text="Download Images", command=start_download).pack(pady=10)

log_var = StringVar()
log_var.set("Enter your credentials and click 'Download Images'")
Label(root, textvariable=log_var, wraplength=480).pack(pady=10)

root.mainloop()