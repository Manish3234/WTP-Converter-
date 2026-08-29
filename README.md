# Camera Capture → PDF → Email Automation

A Python automation project that captures images from a webcam at a fixed time interval, combines the captured images into a single PDF, and sends the PDF as an email attachment using Gmail SMTP.

This project is designed to be simple to set up and can be adapted for applications such as automatic document capture, monitoring, note collection, and image-to-PDF workflows.

---

## 📌 Features

* 📷 Capture images using a webcam
* ⏱️ Capture images automatically at a configurable interval
* 💾 Save captured images locally
* 📄 Combine captured images into a single PDF
* 📧 Send the generated PDF through Gmail
* 🔐 Keep email credentials outside the source code
* ⚙️ Configure the application using environment variables
* 🖥️ Works on Windows, macOS, and Linux with Python and a compatible webcam

---

# 🔄 How the Program Works

The program follows this workflow:

```text
             ┌──────────────┐
             │    Webcam    │
             └──────┬───────┘
                    │
                    ▼
          ┌───────────────────┐
          │  Capture Images   │
          │  at Fixed Interval│
          └─────────┬─────────┘
                    │
                    ▼
             ┌─────────────┐
             │  captures/  │
             └──────┬──────┘
                    │
                    ▼
          ┌───────────────────┐
          │   Create PDF      │
          └─────────┬─────────┘
                    │
                    ▼
             ┌─────────────┐
             │   output/   │
             │  notes.pdf  │
             └──────┬──────┘
                    │
                    ▼
          ┌───────────────────┐
          │    Gmail SMTP     │
          └─────────┬─────────┘
                    │
                    ▼
             ┌─────────────┐
             │  Recipient  │
             └─────────────┘
```

The application has three main stages:

1. **Image Capture**
2. **PDF Generation**
3. **Email Delivery**

---

# 🛠️ Requirements

Before installing the project, make sure you have:

* Python **3.10 or newer**
* A working webcam
* Internet connection for sending email
* A Gmail account
* A Gmail **App Password**

> You should not use your normal Gmail password for SMTP authentication.

---

# 📥 Installation

## 1. Clone the Repository

Open PowerShell, Terminal, or Command Prompt and run:

```bash
git clone https://github.com/YOUR_USERNAME/camera-capture-pdf-email.git
```

Then enter the project directory:

```bash
cd camera-capture-pdf-email
```

---

## 2. Create a Virtual Environment

Using a virtual environment keeps the project's Python packages separate from your system Python installation.

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can use Command Prompt instead:

```cmd
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

After activation, your terminal should show something similar to:

```text
(.venv)
```

---

# 📦 3. Install Dependencies

With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

The project requires:

```text
opencv-python
img2pdf
```

### What these packages do

| Package         | Purpose                                 |
| --------------- | --------------------------------------- |
| `opencv-python` | Accesses the webcam and captures images |
| `img2pdf`       | Converts the captured images into a PDF |

---

# 📧 Gmail Setup

The application uses Gmail's SMTP server to send the generated PDF.

## 4. Create a Gmail App Password

You need a Gmail **App Password**.

An App Password is different from your normal Gmail password and should be used specifically for applications such as this.

Make sure your Google account has **2-Step Verification enabled**.

Then create an App Password through your Google Account security settings.

Google will provide a password similar to:

```text
abcd efgh ijkl mnop
```

Keep this password private.

### ⚠️ Security Warning

**Never put your Gmail password or App Password directly inside `main.py`.**

Do not upload it to GitHub.

Do not put it in:

```text
README.md
main.py
.env.example
```

---

# 🔐 5. Configure Email Credentials

Create a file named:

```text
.env
```

in the root of the project.

Your project should look like:

```text
camera-capture-pdf-email/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
└── .env
```

Your `.env` file should contain:

```text
SENDER_EMAIL=your_sender@gmail.com
RECEIVER_EMAIL=recipient@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

For example:

```text
SENDER_EMAIL=myemail@gmail.com
RECEIVER_EMAIL=receiver@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop
```

Use your own credentials.

### 🚨 Do NOT commit `.env`

The `.gitignore` file should prevent `.env` from being uploaded to GitHub.

Check before committing:

```bash
git status
```

Make sure `.env` does not appear as a file to be committed.

---

# ⚙️ Configuration

The program can be configured using environment variables.

The available settings are:

| Variable                   |               Default | Description                          |
| -------------------------- | --------------------: | ------------------------------------ |
| `CAPTURE_INTERVAL_SECONDS` |                 `300` | Time between image captures          |
| `CAMERA_INDEX`             |                   `0` | Camera/webcam index                  |
| `IMAGE_DIR`                |            `captures` | Directory where images are saved     |
| `PDF_DIR`                  |              `output` | Directory where the PDF is saved     |
| `PDF_FILENAME`             |           `notes.pdf` | Name of the generated PDF            |
| `SENDER_EMAIL`             |                  None | Gmail address used to send the email |
| `RECEIVER_EMAIL`           |                  None | Email address receiving the PDF      |
| `EMAIL_PASSWORD`           |                  None | Gmail App Password                   |
| `EMAIL_SUBJECT`            | `Captured Images PDF` | Email subject                        |
| `EMAIL_BODY`               |      Built-in message | Email body                           |

---

# 🧪 Recommended Test Configuration

For your first test, you probably don't want to wait five minutes between photographs.

Use:

```text
CAPTURE_INTERVAL_SECONDS=5
```

This means the program will capture an image approximately every **5 seconds**.

Once everything works, change it back to:

```text
CAPTURE_INTERVAL_SECONDS=300
```

which is approximately **5 minutes**.

---

# 📷 Camera Configuration

By default, the program uses:

```text
CAMERA_INDEX=0
```

This normally corresponds to the computer's default webcam.

If you have multiple cameras, try:

```text
CAMERA_INDEX=1
```

or:

```text
CAMERA_INDEX=2
```

depending on which camera you want to use.

---

# ▶️ Running the Program

Once installation and configuration are complete, activate your virtual environment and run:

```bash
python main.py
```

The program will display a camera window.

You should see a message similar to:

```text
============================================================
Camera Capture Started
============================================================
Capture interval: 5 seconds
Press 'q' to stop.
```

The webcam feed will remain visible while the program is running.

---

# ⏹️ Stopping the Program

To stop image capture:

**Press `q` while the camera window is active.**

The program will then:

1. Stop the webcam
2. Release the camera
3. Search for captured images
4. Create the PDF
5. Send the PDF by email

---

# 📁 Output Files

During execution, captured images are stored in:

```text
captures/
```

For example:

```text
captures/
├── capture_1756451234.png
├── capture_1756451239.png
├── capture_1756451244.png
└── ...
```

After capture is stopped, the images are combined into:

```text
output/
└── notes.pdf
```

The generated PDF is then attached to the email.

---

# 📧 Email Workflow

After the PDF is created, the program connects to:

```text
smtp.gmail.com
```

using port:

```text
587
```

The connection uses TLS encryption.

The generated PDF is then sent to the configured recipient.

A successful run will display:

```text
Email sent successfully.
```

---

# 🧩 Complete Example

A typical `.env` configuration could look like:

```text
SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=destination@gmail.com
EMAIL_PASSWORD=your_app_password

CAPTURE_INTERVAL_SECONDS=5
CAMERA_INDEX=0

IMAGE_DIR=captures
PDF_DIR=output
PDF_FILENAME=notes.pdf

EMAIL_SUBJECT=Captured Images PDF
EMAIL_BODY=Please find the captured images attached.
```

Then simply run:

```bash
python main.py
```

---

# 🐛 Troubleshooting

## Camera does not open

If you see:

```text
Could not open the camera.
```

try changing:

```text
CAMERA_INDEX=0
```

to:

```text
CAMERA_INDEX=1
```

Also make sure another application such as Zoom, Teams, or a browser is not currently using the webcam.

---

## No images are being captured

Check:

```text
CAPTURE_INTERVAL_SECONDS
```

For testing, use:

```text
CAPTURE_INTERVAL_SECONDS=5
```

Also make sure the camera window is active.

---

## PDF is not created

If you see:

```text
No captured images found.
```

check that the `captures/` directory contains:

```text
.png
.jpg
.jpeg
```

image files.

---

## Email authentication fails

If you receive an authentication error:

1. Verify `SENDER_EMAIL`
2. Verify `RECEIVER_EMAIL`
3. Make sure you are using a **Gmail App Password**
4. Make sure 2-Step Verification is enabled
5. Make sure there are no accidental spaces or quotation marks in `.env`
6. Generate a new App Password if necessary

Do not use your normal Gmail account password.

---

## `.env` accidentally appears in Git

Stop before running:

```bash
git push
```

Check:

```bash
git status
```

If `.env` has already been committed, removing it from the folder is **not enough** because Git history may still contain the credential.

Revoke the exposed Gmail App Password and create a new one.

---

# 📂 Project Structure

The recommended repository structure is:

```text
camera-capture-pdf-email/
│
├── main.py
│
├── requirements.txt
│
├── README.md
│
├── .gitignore
│
├── .env.example
│
├── captures/
│   └── Generated images
│
└── output/
    └── Generated PDF
```

The `captures/` and `output/` directories are generated during execution and should not normally be uploaded to GitHub.

---

# 🔒 Security

This project intentionally keeps sensitive information outside the Python source code.

Never commit:

```text
.env
```

or any file containing:

```text
Gmail passwords
App Passwords
API keys
Private credentials
```

The repository should contain only:

```text
.env.example
```

with placeholder values.

For example:

```text
SENDER_EMAIL=your_sender@gmail.com
RECEIVER_EMAIL=your_recipient@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

---

# 🚀 Future Improvements

Possible improvements for future versions include:

* [ ] Add command-line arguments
* [ ] Add timestamp information to images
* [ ] Automatically delete old images
* [ ] Add logging
* [ ] Add configuration through a proper `.env` loader
* [ ] Add multiple email recipients
* [ ] Add HTML email support
* [ ] Add image resolution configuration
* [ ] Add automatic scheduled execution
* [ ] Add unit tests
* [ ] Add a graphical user interface
* [ ] Add automatic PDF naming based on date and time

---

# 📚 Technologies Used

This project is built using:

* **Python**
* **OpenCV**
* **img2pdf**
* **SMTP**
* **Gmail**

### Python Standard Library

The project also uses Python's built-in modules:

```text
os
time
smtplib
email
pathlib
```

---

# 📜 License

This project is provided for educational and personal use.

If you intend to distribute or modify this project publicly, consider adding an open-source license such as the MIT License.

---

# 👨‍💻 Author

**Your Name**

GitHub: `https://github.com/YOUR_USERNAME`

---

## ⭐ If You Find This Project Useful

If this project helped you, consider giving the repository a ⭐ on GitHub.
