# Outlook.com Image Attachment Downloader (Mac)

A simple **Mac GUI tool** to download all **image attachments** (JPG, PNG, GIF) from your Outlook.com Inbox and save them into a ZIP file.  

✅ Only downloads true attachments (inline images in email layout are ignored).  
✅ Handles duplicate filenames automatically.  
✅ Cleans up temporary folders automatically.  
✅ Logs progress in the GUI window.

---

## Features

- Download **Inbox only** from Outlook.com / Hotmail accounts  
- Supports **JPG, JPEG, PNG, GIF** attachments  
- Avoids overwriting files with duplicate names  
- Creates a single **ZIP archive** of all images  
- GUI prompts for **email** and **app-specific password**  
- Displays **download progress and logs** in the GUI  
- Fully Mac-compatible  

---

## Requirements

- **Python 3.8+** (pre-installed on macOS)  
- **Tkinter** (included with Python on macOS)  
- **App-specific password** (required if your account has 2FA enabled)  

> **Note:** You must generate an app-specific password in your Outlook.com account settings if you have two-factor authentication enabled.  

---

## Setup

1. **Clone this repository** (or download the script):

```bash
git clone https://github.com/yourusername/outlook-image-downloader.git
cd outlook-image-downloader