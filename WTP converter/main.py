import cv2
import time
import os
import img2pdf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#image cap part

stream = cv2.VideoCapture(0)
if not stream.isOpened():
    print("Cannot open camera")
    exit()
time_interval = 5  # 5 minutes in seconds for testing you can reduce it to 5 seconds
last_capture_time = time.time()

while True:
    ret, frame = stream.read()
    if not ret:
        print("stop")
        break
    current_time = time.time()

    if current_time - last_capture_time >= time_interval:
        save_dir = r"D:\manish\camcap" #change the path 
        os.makedirs(save_dir,exist_ok=True)
        file_path = os.path.join(save_dir,f"capture_{int(current_time)}.png")
        cv2.imwrite(file_path,frame)
        print(f"Image saved at {file_path}")
        last_capture_time = current_time

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) == ord('q'):# to close the window by press q when application is active 
        break

stream.release()
cv2.destroyAllWindows()

#pdf creation part

folder_path = r"D:\manish\camcap" #path for images
output_pdf_dir = r"D:\manish\mainsh_project\pdfs" #path for saving pdf  
pdf_filename = "notes.pdf" #pdf name 
output_pdf_path = os.path.join(output_pdf_dir,pdf_filename)

os.makedirs(output_pdf_dir,exist_ok=True) #checking if the file path exists if not create one

def create_pdf_from_images(folder_path,output_pdf_path):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png','.jpg','.jpeg'))] #collecting images 
    image_files.sort()  
    
    if not image_files:
        print("No image files found in the directory.")
        return

    # Create PDF
    with open(output_pdf_path,"wb") as f:
        f.write(img2pdf.convert([os.path.join(folder_path,img) for img in image_files]))   
    print("PDF created successfully at:",output_pdf_path)

create_pdf_from_images(folder_path,output_pdf_path) #function call

#sending email part

sender_email = "prashan2at06@gmail.com"
receiver_email = "manish2at3234@gmail.com"
password = "qyak pswe icyp ouxh"
subject = "Multiple Images from Folder" # email subject
body = ":)" #email body

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body,'plain'))

def email_images(msg,output_pdf_dir,pdf_filename):
    pdf_full_path = os.path.join(output_pdf_dir,pdf_filename)
    if os.path.exists(output_pdf_dir):
        with open(pdf_full_path,'rb') as attachment:
            part = MIMEBase('application','pdf')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        part.add_header('Content-Disposition',f'attachment; filename={pdf_filename}')
        msg.attach(part)

        try:
            with smtplib.SMTP('smtp.gmail.com',587) as server:
                server.starttls()
                server.login(sender_email,password)
                server.sendmail(sender_email,receiver_email,msg.as_string())
            print("Email sent successfully.")
        except Exception as e:
            print(f"Error sending email: {e}")

email_images(msg, output_pdf_dir,pdf_filename) #function call

