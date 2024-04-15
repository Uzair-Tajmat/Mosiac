import base64
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.http import JsonResponse
from moviepy.editor import VideoFileClip
import asyncio
import cv2
import numpy as np
import pytesseract

import re
import base64



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

@csrf_exempt
def pausedContent(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        print(status)
        image_data = request.FILES.get('image_data')
        save_folder = './static'
        os.makedirs(save_folder, exist_ok=True)

            # Generate a unique filename
        filename = "one"

            # Save the image to the folder
        with open(os.path.join(save_folder, filename), 'wb') as f:
            for chunk in image_data.chunks():
                f.write(chunk)
        # try:
        #     image_data = base64.b64decode(image_data)
            
        # except TypeError:
        #     return JsonResponse({'error': 'Invalid base64-encoded image data'}, status=400)
        # nparr = np.frombuffer(image_data, np.uint8)
        # print("Done")
        # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
        # print(data)
        
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


def handle_uploaded_image(image_data):
    # Define the path where you want to save the image
    # Make sure the directory exists and is writable
    save_path = './static/image.jpg'
    
    # Write the image data to the specified path
    with open(save_path, 'wb') as destination:
        for chunk in image_data.chunks():
            destination.write(chunk)