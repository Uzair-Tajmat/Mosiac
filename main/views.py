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



@csrf_exempt
async def closingWindow(request):
    if request.method == 'POST':
        playback_time_seconds = float(request.POST.get('playback_time', 0))
        total_duration = float(request.POST.get('total_duration', 0))
        
        if playback_time_seconds > 60: 
            
            folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'video_sections')
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
            original_video_path = './static/Test1.mp4'
            i = 1
            startPos = 0
            
            async def split_video(startPos, endPos, i):
                clip = VideoFileClip(original_video_path).subclip(startPos, endPos)
                part_name = os.path.join(folder_path, "part_" + str(i) + ".mp4")
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
            
            return JsonResponse({'success': True})
           
        else:
            print('Playback time is less than or equal to 1 minute:')
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
        print(video_path)
        return render(request, 'main.html', {'video_path': video_path})
    


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
    video_folder = './static/video_sections'
    videos = []
    for filename in os.listdir(video_folder):
        if filename.endswith(('.mp4', '.avi', '.mov', '.wmv')):
            videos.append({'name': filename, 'path': os.path.join(video_folder, filename)})
    return JsonResponse(videos, safe=False)

logger = logging.getLogger(__name__)

@csrf_exempt
def handle_pause_time(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        paused_time = data.get('paused_time')
        
        # Load JSON data
        try:
            with open('./static/Test2_extracted_text.json', 'r') as json_file:
                json_data = json.load(json_file)
                
            # Construct the key
            key = f"Test2_second_{paused_time}"
            
            # Get the corresponding text
            text = json_data.get(key, "No text available for this second.")
            print(text)
            
            # Print the text to the server logs
            logger.info(f"Paused at {paused_time} seconds: {text}")
            
            return JsonResponse({'status': 'success', 'paused_time': paused_time})
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
            form.save()
            result = performExtraction(title).delay()
            # Check task status
            print(f"Task status: {result.status}")  # Should print 'PENDING' initially and then 'SUCCESS'

            # Wait for the task to complete and get the result
            task_result = result.get(timeout=10)  # This will block until the task completes or timeout
            print(f"Task result: {task_result}") 
            print("Done 2")
            return redirect('First') 
        
    else:
        form = UploadForm()
    return render(request, 'first.html', {'form': form})
        

      
    