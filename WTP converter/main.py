import os
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import cv2
import img2pdf


# ============================================================
# CONFIGURATION
# ============================================================

CAPTURE_INTERVAL_SECONDS = int(
    os.getenv("CAPTURE_INTERVAL_SECONDS", "300")
)

CAMERA_INDEX = int(
    os.getenv("CAMERA_INDEX", "0")
)

IMAGE_DIR = Path(
    os.getenv("IMAGE_DIR", "captures")
)

PDF_DIR = Path(
    os.getenv("PDF_DIR", "output")
)

PDF_FILENAME = os.getenv(
    "PDF_FILENAME",
    "notes.pdf"
)

# Email configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

EMAIL_SUBJECT = os.getenv(
    "EMAIL_SUBJECT",
    "Captured Images PDF"
)

EMAIL_BODY = os.getenv(
    "EMAIL_BODY",
    "Please find the captured images compiled into a PDF attached."
)


# ============================================================
# IMAGE CAPTURE
# ============================================================

def capture_images():
    """
    Capture images from the webcam at a fixed time interval.

    Press 'q' in the camera window to stop capturing.
    """

    IMAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    stream = cv2.VideoCapture(CAMERA_INDEX)

    if not stream.isOpened():
        raise RuntimeError(
            "Could not open the camera."
        )

    last_capture_time = time.time()

    print("=" * 60)
    print("Camera Capture Started")
    print("=" * 60)
    print(
        f"Capture interval: "
        f"{CAPTURE_INTERVAL_SECONDS} seconds"
    )
    print("Press 'q' to stop.")
    print()

    try:
        while True:

            ret, frame = stream.read()

            if not ret:
                print(
                    "Could not read a frame from the camera."
                )
                break

            current_time = time.time()

            # Check whether it is time to capture
            if (
                current_time - last_capture_time
                >= CAPTURE_INTERVAL_SECONDS
            ):

                filename = (
                    f"capture_{int(current_time)}.png"
                )

                file_path = IMAGE_DIR / filename

                success = cv2.imwrite(
                    str(file_path),
                    frame
                )

                if success:
                    print(
                        f"Image saved: {file_path}"
                    )

                    last_capture_time = current_time

                else:
                    print(
                        f"Failed to save image: "
                        f"{file_path}"
                    )

            # Display camera feed
            cv2.imshow(
                "Camera Capture",
                frame
            )

            # Press q to quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        stream.release()
        cv2.destroyAllWindows()

        print()
        print("Camera capture stopped.")


# ============================================================
# PDF CREATION
# ============================================================

def create_pdf_from_images():
    """
    Combine all captured images into a single PDF.

    Returns:
        Path to the generated PDF, or None if
        no images were found.
    """

    PDF_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not IMAGE_DIR.exists():
        print(
            "Image directory does not exist."
        )
        return None

    image_files = sorted(
        path
        for path in IMAGE_DIR.iterdir()
        if path.suffix.lower()
        in {".png", ".jpg", ".jpeg"}
    )

    if not image_files:
        print(
            "No captured images found."
        )
        print(
            "PDF was not created."
        )
        return None

    output_pdf_path = (
        PDF_DIR / PDF_FILENAME
    )

    print()
    print("=" * 60)
    print("Creating PDF")
    print("=" * 60)

    print(
        f"Images found: {len(image_files)}"
    )

    with output_pdf_path.open(
        "wb"
    ) as pdf_file:

        pdf_file.write(
            img2pdf.convert(
                [
                    str(image)
                    for image in image_files
                ]
            )
        )

    print(
        f"PDF created successfully:"
        f"\n{output_pdf_path}"
    )

    return output_pdf_path


# ============================================================
# EMAIL
# ============================================================

def send_email(pdf_path):
    """
    Send the generated PDF as an email attachment
    using Gmail SMTP.
    """

    if not SENDER_EMAIL:
        raise RuntimeError(
            "SENDER_EMAIL is not configured."
        )

    if not RECEIVER_EMAIL:
        raise RuntimeError(
            "RECEIVER_EMAIL is not configured."
        )

    if not EMAIL_PASSWORD:
        raise RuntimeError(
            "EMAIL_PASSWORD is not configured."
        )

    message = MIMEMultipart()

    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = EMAIL_SUBJECT

    message.attach(
        MIMEText(
            EMAIL_BODY,
            "plain"
        )
    )

    # Attach PDF
    with pdf_path.open(
        "rb"
    ) as attachment:

        part = MIMEBase(
            "application",
            "pdf"
        )

        part.set_payload(
            attachment.read()
        )

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{pdf_path.name}"'
    )

    message.attach(part)

    print()
    print("=" * 60)
    print("Sending Email")
    print("=" * 60)

    try:

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                SENDER_EMAIL,
                EMAIL_PASSWORD
            )

            server.sendmail(
                SENDER_EMAIL,
                RECEIVER_EMAIL,
                message.as_string()
            )

        print(
            "Email sent successfully."
        )

    except smtplib.SMTPAuthenticationError:

        raise RuntimeError(
            "Gmail authentication failed. "
            "Check your email address and "
            "Gmail App Password."
        )

    except Exception as error:

        raise RuntimeError(
            f"Failed to send email: {error}"
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    """
    Run the complete workflow:

        Webcam
           ↓
        Image Capture
           ↓
        PDF Generation
           ↓
        Email Delivery
    """

    print()
    print("=" * 60)
    print(" CAMERA → PDF → EMAIL AUTOMATION")
    print("=" * 60)
    print()

    # Step 1: Capture images
    capture_images()

    # Step 2: Create PDF
    pdf_path = create_pdf_from_images()

    # Step 3: Send email
    if pdf_path is not None:

        send_email(pdf_path)

    else:

        print(
            "No PDF was generated, "
            "so no email was sent."
        )

    print()
    print("=" * 60)
    print("Process completed.")
    print("=" * 60)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()