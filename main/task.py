# myapp/tasks.py
import os
from celery import shared_task
import cv2
import pytesseract
import json
from collections import defaultdict
import time
import ssl
import smtplib
from email.message import EmailMessage
def save_to_json(data, filename):
    """
    Saves the given data dictionary to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def process_video(video_path, title):
    """
    Processes the video at the given path, extracts text from each frame at one-second intervals,
    and stores the text in a dictionary if the text is not repeated.
    """
    video_name = title
    print(video_path)
    print(video_name)
    print("Processsing Started")
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None

    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / frame_rate

    text_per_second = defaultdict(str)
    previous_text = ""

    start_time = time.time()

    for sec in range(int(duration) + 1):
        # Set the video position to the current second
        cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        ret, frame = cap.read()
        if not ret:
            break

        text = extract_text_from_frame(frame)
        
        if text != previous_text:
            key = f"{video_name}_second_{sec}"
            text_per_second[key] = text
            previous_text = text

    cap.release()
    end_time = time.time()
    print(f"Processing time: {end_time - start_time} seconds")
    return text_per_second



@shared_task
def performExtraction(title,email):
    video_path_temp = f"./media/uploads/{title}.mp4"
    video_path = video_path_temp.replace(" ","_")
    print(video_path)
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract executable path
    text_data = process_video(video_path, title)

    if text_data:
        output_directory = "./ExtractedText_Files"

        # Save the dictionary to a JSON file
        json_filename = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(video_path))[0]}_extracted_text.json")
        save_to_json(text_data, json_filename)
        sendMail(email,title)
        print(f"Extracted text saved to {json_filename}")

def extract_text_from_frame(frame):
    """
    Extracts text from a given video frame using Tesseract OCR.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip()


def sendMail(email,title):
    email_sender="uniquemart0810@gmail.com"
    email_pas="ekpi imvk upzl zvzx"
    email_reciever=email

    subject = f"Your Video Have been Successfully Uploaded"
    body=f"""
        Hello User,

        I hope this message finds you well.

        I am pleased to inform you that your video {title} has been successfully uploaded to our platform . The upload process has been completed without any issues, and your content is now available for viewing.

        Should you have any questions or require further assistance, please do not hesitate to contact us. We are here to support you and ensure your experience with our service is smooth and satisfactory.

        Thank you for choosing our platform.

        Best regards,
        Uzair Tajmat
        Mosiac :An Adaptive Learning Platform
"""
    em=EmailMessage()
    em['From']=email_sender
    em['To']=email_reciever
    em['Subject']=subject
    em.set_content(body)

    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_pas)
        smtp.sendmail(email_sender,email_reciever,em.as_string())