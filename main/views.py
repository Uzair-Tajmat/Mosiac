import base64
from django.shortcuts import render,redirect # type: ignore
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.http import JsonResponse
from moviepy.editor import VideoFileClip
import asyncio
import cv2
import numpy as np
import pytesseract
import json
import re
import logging
import base64
from collections import defaultdict
import time
from .models import Upload
from .forms import UploadForm
from .task import performExtraction
# from .task import add
# import openai 
import google.generativeai as genai
from django.contrib.sessions.backends.db import SessionStore
from asgiref.sync import sync_to_async
from django.core.files.storage import default_storage
from cleantext import clean
import re
import spacy
import yake

nlp = spacy.load("en_core_web_sm")
genai.configure(api_key="AIzaSyD_WbFuq-anTyje-zbQ3PIOcs1OcyPWfc4")
chat_log=[]


@csrf_exempt
async def closingWindow(request):
    if request.method == 'POST':
        playback_time_seconds = float(request.POST.get('playback_time', 0))
        total_duration = float(request.POST.get('total_duration', 0))
        title = str(request.POST.get('title'))
        session_title = await sync_to_async(lambda: request.session.get('title', ''))()
        actualTitle = session_title.replace(' ', '_') if session_title else title.replace(' ', '_')
        print(actualTitle)
        if playback_time_seconds > 60: 
            
            folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'video_sections')
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
            original_video_path = f'./media/uploads/{actualTitle}.mp4'
            print(original_video_path)
            i = 1
            startPos = 0
            
            async def split_video(startPos, endPos, i):
                clip = VideoFileClip(original_video_path).subclip(startPos, endPos)
                part_name = os.path.join(folder_path, f"{actualTitle}_part_" + str(i) + ".mp4")
                clip.write_videofile(part_name, codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
                print("part ", i, "done")
                
            tasks = []
            while True:
                endPos = startPos + playback_time_seconds
                print("Done", i)
                if endPos > total_duration:
                    endPos = total_duration

                task = asyncio.ensure_future(split_video(startPos, endPos, i))
                tasks.append(task)
                i += 1
                startPos = endPos  # jump to next clip
                
                if startPos >= total_duration:
                    break

            await asyncio.gather(*tasks)
            chat_log.clear()
            await sync_to_async(lambda: request.session.pop('title', None))()
            return JsonResponse({'success': True})
           
        else:
            print('Playback time is less than or equal to 1 minute:')
            await sync_to_async(lambda: request.session.pop('title', None))()
            return JsonResponse({'success': False, 'error': 'Playback time is less than or equal to 1 minute'})
        
        
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})



def home(request):
    return render(request,'index.html')

def First(request):
    return render(request,'First.html')

@csrf_exempt
def Main(request):
    if request.method == "POST":
        video_path=request.POST.get('video_path')
        title=request.POST.get('title')
        discrip=request.POST.get('dis')
        request.session['title'] = title
        print(title)
        print(video_path)
        return render(request, 'main.html', {'video_path': video_path,'title':title,'dis':discrip})
    
@csrf_exempt
def OpenMain(request):
    if request.method=="POST":
        data = json.loads(request.body)
        video_path = data.get('path', '')
        modified_video_path = video_path[1:] if len(video_path) > 1 else ''
        
        print(modified_video_path)
        print(video_path)
        return render(request, 'Main.html', {'video_path': modified_video_path})

@csrf_exempt
def pausedContent(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        print(status)
        image_data = request.FILES.get('image_data')
        
        return HttpResponse({'message': 'Status updated successfully'})
    else:
        return HttpResponse({'error': 'Invalid request method'}, status=400)




@csrf_exempt 
def fetch_videos(request):
    query = request.GET.get('title', '') 
    print(query)
    video_folder = './static/video_sections'
    videos = []
    for filename in os.listdir(video_folder):
        if filename.endswith(('.mp4', '.avi', '.mov', '.wmv')) and query.lower() in filename.lower():
            videos.append({'name': filename, 'path': os.path.join(video_folder, filename)})
    return JsonResponse(videos, safe=False)

logger = logging.getLogger(__name__)

def custom_clean(text):
    return clean(text,
                 fix_unicode=True,       # Fix various unicode errors
                 to_ascii=True,          # Transliterate to closest ASCII representation
                 lower=False,            # Keep the text case unchanged
                 no_line_breaks=False,   # Preserve line breaks
                 no_urls=True,           # Remove URLs
                 no_emails=True,         # Remove email addresses
                 no_phone_numbers=True,  # Remove phone numbers
                 no_numbers=False,       # Keep numbers
                 no_digits=False,        # Keep digits
                 no_currency_symbols=True, # Remove currency symbols
                 no_punct=False,         # Keep punctuation
                 replace_with_url="<URL>",
                 replace_with_email="<EMAIL>",
                 replace_with_phone_number="<PHONE>",
                 replace_with_number="<NUMBER>",
                 replace_with_digit="0",
                 replace_with_currency_symbol="<CUR>",
                 lang="en"               # Set to your language
                 )

def clean_text(text):
    # Use spaCy for tokenization
    doc = nlp(text)
    cleaned_tokens = [custom_clean(token.text) for token in doc]
    cleaned_text = ' '.join(cleaned_tokens)
    return cleaned_text




def extract_keywords_yake(text, top_n=10):
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)
    return [keyword for keyword, score in keywords[:top_n]]


gpt_response=[]

@csrf_exempt
def handle_pause_time(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        paused_time = data.get('paused_time')
        session_title = request.session.get('title', '')
        actualTitle = session_title.replace(' ', '_') if session_title else title.replace(' ', '_')
        # Load JSON data
        try:
            with open(f'./ExtractedText_Files/{actualTitle}_extracted_text.json', 'r') as json_file:
                json_data = json.load(json_file)
                
            # Construct the key
            key = f"{actualTitle}_second_{paused_time}"
            # Get the corresponding text
            text = json_data.get(key, "No text available for this second.")
            updated=clean_text(text)
            print(updated)

            

            model = genai.GenerativeModel("gemini-1.5-flash")
            chat = model.start_chat()
            response = chat.send_message(updated)
            title="Introduction to Python Dictionary"
            print(response.text)

            gpt_response.append({'title':title , "response":response.text})
            
           
            

            
           

            return JsonResponse({'status': 'success', 'generatedResponse':gpt_response})
        except FileNotFoundError:
            logger.error('JSON file not found.')
            return JsonResponse({'status': 'error', 'message': 'JSON file not found.'}, status=500)
        except json.JSONDecodeError:
            logger.error('Error decoding JSON file.')
            return JsonResponse({'status': 'error', 'message': 'Error decoding JSON file.'}, status=500)
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)





@csrf_exempt
def Upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        print("Done")
        global title
        title=" "
        if form.is_valid():
            title = form.cleaned_data['title']
            email = form.cleaned_data['email']
            upload=form.save(commit=False)
           
            video = request.FILES['file']
            print("FIle Recieved")
            video_path = default_storage.save(f'uploads/{title}.mp4', video)
            video_full_path = default_storage.path(video_path)
            print(video_full_path)
            video_clip = VideoFileClip(video_full_path)
            upload.video_time = f"{int(video_clip.duration // 60)}:{str(int(video_clip.duration % 60)).zfill(2)}"
            print("Video Done")
            video_clip.close()

            thumbnail = request.FILES['thumbnail']
            print("Thumbnail Recieved and started")
            thumbnail_path = default_storage.save(f'thumbnails/{thumbnail.name}', thumbnail)
            print(thumbnail_path)
            print("Done Thumbanil")
            # Update file paths in the model instance
            upload.file = video_path
            upload.thumbnail = thumbnail_path
            
            # Save the modified instance to the database
            upload.save()
            json_data = {
                "thumbnail": f"/media/{thumbnail_path}",
                "video_time": upload.video_time,
                "channel_pic": "/static/dist/images/trig_account.jpg",
                "title": upload.title,
                "description": upload.description,
                "video_path": f"/media/{video_path}"
            }
            print("Datat ready")
            json_file_path = './static/dist/data/videos.json'
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r') as json_file:
                    data = json.load(json_file)
            else:
                data = []
            print("Data added")
            data.append(json_data)
            
            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file, indent=2)
             
            # print(title)
            print("Sending further")
            performExtraction.delay(title)
            # Check task status
            print("Done 2")
            return redirect('First') 
        
    else:
        form = UploadForm()
    return render(request, 'first.html', {'form': form})
        

@csrf_exempt 
def AllContent(request):
    title = None
    content = None
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('data')
        print(title)
        print(content)
    return render(request, 'AllContent.html', {'title': title, 'content': content})