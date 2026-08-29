# 📷 Raspberry Pi Automated Camera Capture & PDF Email System

An automated image-capture and document-delivery system built using a **Raspberry Pi Zero W**, **Raspberry Pi Camera**, and **Raspberry Pi OS**.

The system periodically captures images using the Raspberry Pi camera, stores the captured images, combines them into a PDF document, and automatically sends the generated PDF to a specified email address.

The Raspberry Pi Zero W provides built-in Wi-Fi connectivity, allowing the system to connect to the internet and perform the entire workflow without requiring a separate computer or wired network connection.

---

## ✨ Features

* 📷 Automated image capture using a Raspberry Pi camera
* 🍓 Designed for **Raspberry Pi Zero W**
* 🐧 Runs on **Raspberry Pi OS**
* 📶 Uses the Raspberry Pi Zero W's built-in Wi-Fi
* ⏱️ Configurable image-capture interval
* 💾 Automatically stores captured images
* 📄 Converts captured images into a single PDF
* 📧 Automatically sends the PDF through Gmail
* 🔐 Email credentials are kept outside the source code
* 🤖 Minimal user interaction after the system is configured

---

# 🧠 System Overview

The system is designed to work as an automated pipeline:

```text
                    ┌──────────────────────┐
                    │   Raspberry Pi Zero W │
                    │                      │
                    │    Raspberry Pi OS   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Raspberry Pi       │
                    │      Camera          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Capture Images      │
                    │  at Fixed Intervals   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Local Storage    │
                    │       captures/       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    PDF Generation    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      notes.pdf       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Raspberry Pi     │
                    │      Wi-Fi Module     │
                    └──────────┬───────────┘
                               │
                            Internet
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Gmail SMTP       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Email Recipient    │
                    └──────────────────────┘
```

Once configured, the Raspberry Pi handles the complete workflow.

---

# 🧰 Hardware Used

| Component                       | Purpose                                    |
| ------------------------------- | ------------------------------------------ |
| **Raspberry Pi Zero W**         | Main computing unit and Wi-Fi connectivity |
| **Raspberry Pi Camera**         | Captures images                            |
| **MicroSD Card**                | Raspberry Pi OS and local storage          |
| **Wi-Fi / Internet connection** | Provides network access for email delivery |
| **Power supply**                | Powers the Raspberry Pi                    |

---

# 💻 Software Used

* **Raspberry Pi OS**
* **Python 3**
* **OpenCV**
* **img2pdf**
* **Gmail SMTP**
* Python standard libraries:

  * `os`
  * `time`
  * `smtplib`
  * `email`
  * `pathlib`

---

# 🔄 How It Works

The application consists of three main stages.

## 1. Image Capture

The Raspberry Pi accesses the connected camera and continuously displays the camera feed.

At the configured interval, the program captures an image and saves it locally.

For example:

```text
captures/
├── capture_1756451234.png
├── capture_1756451534.png
├── capture_1756451834.png
└── ...
```

The capture interval can be changed using:

```text
CAPTURE_INTERVAL_SECONDS
```

The default value is:

```text
300 seconds
```

which corresponds to approximately **5 minutes**.

For testing, a shorter interval such as:

```text
CAPTURE_INTERVAL_SECONDS=5
```

can be used.

---

# 📄 2. PDF Generation

After image capture is stopped, the program searches the image directory for:

```text
.png
.jpg
.jpeg
```

files.

The images are then combined into a single PDF using `img2pdf`.

The generated PDF is stored in:

```text
output/
```

For example:

```text
output/
└── notes.pdf
```

---

# 📧 3. Automatic Email Delivery

After the PDF has been generated, the program connects to Gmail's SMTP server:

```text
smtp.gmail.com
```

using port:

```text
587
```

The connection uses TLS.

The generated PDF is attached to an email and sent to the configured recipient.

A successful operation produces:

```text
Email sent successfully.
```

---

# 📶 Why Raspberry Pi Zero W?

The Raspberry Pi Zero W was used as the core of this project because it provides a compact computing platform with built-in wireless connectivity.

The integrated Wi-Fi allows the system to connect to an existing internet connection without requiring:

* Ethernet
* A separate Wi-Fi adapter
* A continuously connected desktop computer

This makes the system suitable for an **automated, standalone setup**.

Once the Raspberry Pi is configured and connected to Wi-Fi, the image-processing and email workflow can be performed directly on the device.

---

# ⚙️ Configuration

The program uses environment variables for configuration.

| Variable                   |               Default | Description                        |
| -------------------------- | --------------------: | ---------------------------------- |
| `CAPTURE_INTERVAL_SECONDS` |                 `300` | Time between image captures        |
| `CAMERA_INDEX`             |                   `0` | Camera index                       |
| `IMAGE_DIR`                |            `captures` | Image storage directory            |
| `PDF_DIR`                  |              `output` | PDF storage directory              |
| `PDF_FILENAME`             |           `notes.pdf` | Generated PDF filename             |
| `SENDER_EMAIL`             |                  None | Email account used to send the PDF |
| `RECEIVER_EMAIL`           |                  None | Email recipient                    |
| `EMAIL_PASSWORD`           |                  None | Gmail App Password                 |
| `EMAIL_SUBJECT`            | `Captured Images PDF` | Email subject                      |
| `EMAIL_BODY`               |       Default message | Email body                         |

---

# 🔐 Gmail Configuration

The email functionality requires a Gmail account.

For authentication, use a **Gmail App Password** rather than your normal Gmail password.

Your credentials should be supplied through environment variables:

```text
SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=recipient@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

### ⚠️ Security

**Never place your Gmail password or App Password directly inside `main.py`.**

Do not commit credentials to GitHub.

The repository should contain only an example configuration such as:

```text
.env.example
```

with placeholder values.

---

# ▶️ Running the Program

Once the Raspberry Pi and camera are configured, run:

```bash
python main.py
```

The camera feed will open and the system will begin capturing images according to the configured interval.

The program displays:

```text
============================================================
Camera Capture Started
============================================================
Capture interval: 300 seconds
Press 'q' to stop.
```

---

# ⏹️ Stopping the Capture Process

To stop the capture process, press:

```text
q
```

while the camera window is active.

After stopping, the program automatically proceeds to:

```text
Image Capture
      ↓
PDF Generation
      ↓
Email Delivery
```

No separate PDF-generation or email command is required.

---

# 📁 Project Structure

```text
camera-capture-pdf-email/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── captures/
│   └── Captured images
│
└── output/
    └── Generated PDF
```

The `captures/` and `output/` directories contain generated data and should normally be excluded from the Git repository.

---

# 🧪 Testing

For initial testing, reduce the capture interval:

```text
CAPTURE_INTERVAL_SECONDS=5
```

Run:

```bash
python main.py
```

Allow several images to be captured.

Press:

```text
q
```

The program should then:

1. Stop the camera
2. Find the captured images
3. Generate `notes.pdf`
4. Save the PDF in `output/`
5. Connect to Gmail
6. Send the PDF to the configured recipient

Once the system has been tested successfully, the interval can be increased.

For approximately five-minute intervals:

```text
CAPTURE_INTERVAL_SECONDS=300
```

---

# 🐛 Troubleshooting

## Camera does not open

If the program reports:

```text
Could not open the camera.
```

check:

* The Raspberry Pi camera is properly connected.
* The camera is enabled/configured in Raspberry Pi OS.
* The correct camera interface is available.
* No other program is currently using the camera.

If multiple cameras are available, try changing:

```text
CAMERA_INDEX=0
```

to:

```text
CAMERA_INDEX=1
```

---

## No images are captured

Check the value of:

```text
CAPTURE_INTERVAL_SECONDS
```

For testing:

```text
CAPTURE_INTERVAL_SECONDS=5
```

Also verify that the camera feed is working correctly.

---

## PDF is not generated

If the program reports:

```text
No captured images found.
```

check the `captures/` directory.

It should contain image files with one of these extensions:

```text
.png
.jpg
.jpeg
```

---

## Email authentication fails

Check:

1. Sender email address
2. Recipient email address
3. Gmail App Password
4. Internet connection
5. Gmail account security settings
6. Environment-variable configuration

Do not use your normal Gmail password.

---

# 🔒 Security Practices

This project separates configuration from application code.

Sensitive information should never be committed to Git.

Do not commit:

```text
.env
```

or files containing:

```text
Passwords
Gmail App Passwords
API keys
Private credentials
```

If a credential is accidentally pushed to a public repository, revoke it immediately and create a new credential.

---

# 🚀 Possible Future Improvements

The current system can be extended in several directions:

* [ ] Run automatically at Raspberry Pi startup
* [ ] Run as a background service
* [ ] Add automatic image cleanup
* [ ] Add timestamps to captured images
* [ ] Add date-based PDF filenames
* [ ] Add logging
* [ ] Add configurable camera resolution
* [ ] Add multiple email recipients
* [ ] Add HTML email support
* [ ] Add automatic scheduling
* [ ] Add remote monitoring
* [ ] Add a web interface
* [ ] Add failure notifications
* [ ] Add automatic retry when the internet connection is unavailable

---

# 🧩 Applications

The basic architecture can be adapted for:

* Automated document scanning
* Periodic visual monitoring
* Remote image collection
* Automated note/document creation
* Small IoT monitoring systems
* Time-based photography
* Remote data collection

The Raspberry Pi provides the local processing and camera interface, while Wi-Fi enables communication with external services.

---

# 📚 Technical Summary

This project demonstrates the integration of:

```text
Embedded Hardware
       +
Camera Interface
       +
Python Automation
       +
Image Processing
       +
PDF Generation
       +
Network Connectivity
       +
SMTP Email
```

It combines a low-power Raspberry Pi platform with Python software to create a compact automated system capable of capturing, processing, and remotely delivering image data.

---

# 👨‍💻 Author

**Your Name**

GitHub: `https://github.com/YOUR_USERNAME`

---

## 📜 License

This project is intended for educational and personal use.

If you plan to distribute the project publicly, consider adding an open-source license such as the **MIT License**.
