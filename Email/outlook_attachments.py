import imaplib
import email
import os
import zipfile
from datetime import datetime, timedelta

# ===== CONFIGURATION =====
EMAIL = "your_outlook_address@outlook.com"
APP_PASSWORD = "your_app_password"  # generate one in Outlook settings if using 2FA
IMAP_SERVER = "outlook.office365.com"
FOLDERS = ["Inbox"]  # add more folders if needed: ["Inbox", "Sent", "Archive"]
OUTPUT_DIR = "outlook_attachments"
ZIP_FILENAME = "outlook_image_attachments.zip"

# Optional filters
DAYS_BACK = None  # e.g., 30 to only download attachments from the last 30 days
FROM_SENDER = None  # e.g., "friend@example.com" to filter by sender

# ===== HELPER FUNCTIONS =====
def format_imap_date(days_back):
    if days_back is None:
        return None
    date = datetime.now() - timedelta(days=days_back)
    return date.strftime("%d-%b-%Y")  # IMAP date format

# ===== MAIN SCRIPT =====
os.makedirs(OUTPUT_DIR, exist_ok=True)
seen_filenames = {}
total_count = 0

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, APP_PASSWORD)

for folder in FOLDERS:
    mail.select(folder)
    
    # Build IMAP search query
    search_criteria = ['ALL']
    if DAYS_BACK:
        search_criteria.append(f'SINCE {format_imap_date(DAYS_BACK)}')
    if FROM_SENDER:
        search_criteria.append(f'FROM "{FROM_SENDER}"')
    search_str = ' '.join(search_criteria)
    
    result, data = mail.search(None, search_str)
    if result != "OK":
        print(f"Failed to search folder: {folder}")
        continue

    ids = data[0].split()
    print(f"Found {len(ids)} emails in folder '{folder}' matching criteria.")

    for num in ids:
        res, msg_data = mail.fetch(num, "(RFC822)")
        if res != "OK":
            continue
        msg = email.message_from_bytes(msg_data[0][1])

        for part in msg.walk():
            if part.get_content_disposition() == "attachment":
                filename = part.get_filename()
                if not filename:
                    continue
                if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                    # Avoid duplicates
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

                    # Save attachment
                    with open(os.path.join(OUTPUT_DIR, safe_name), "wb") as f:
                        f.write(part.get_payload(decode=True))
                    total_count += 1

mail.logout()

# ===== ZIP THE ATTACHMENTS =====
with zipfile.ZipFile(ZIP_FILENAME, "w") as zipf:
    for file in os.listdir(OUTPUT_DIR):
        zipf.write(os.path.join(OUTPUT_DIR, file), arcname=file)

print(f"✅ Downloaded {total_count} image attachments from {len(FOLDERS)} folder(s).")
print(f"✅ All images zipped into '{ZIP_FILENAME}'.")