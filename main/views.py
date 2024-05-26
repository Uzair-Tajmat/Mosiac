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
            time.sleep(3)
            gpt_response_simulation="Introduction to Python Dictionaries\n\nPython dictionaries are powerful, flexible, and efficient data structures that allow you to store and manage data using key-value pairs. Unlike lists, which are indexed by a range of numbers, dictionaries are indexed by keys, which can be any immutable type, typically strings or numbers. This structure makes dictionaries ideal for looking up and retrieving data efficiently.\n\nKey Features of Python Dictionaries\n\nKey-Value Pairs: Each element in a dictionary is a pair consisting of a key and a corresponding value. Keys must be unique within a dictionary, and values can be of any type.\n\nUnordered: Dictionaries are unordered collections, meaning that items are stored and retrieved by key, not by position. As of Python 3.7, dictionaries maintain the insertion order of keys, but this behavior should not be relied upon for program logic in earlier versions.\n\nMutable: Dictionaries are mutable, meaning that you can change their contents (add, modify, or remove key-value pairs) without creating a new dictionary.\n\nEfficient: Dictionaries offer average-case constant time complexity, O(1), for lookups, insertions, and deletions, making them very efficient for these operations.\n\nCreating and Using Dictionaries\n\nCreating a dictionary is straightforward. You can use curly braces {} with key-value pairs separated by colons, or you can use the dict function.\n\n```python\n# Creating a dictionary with curly braces\nmy_dict = {\n    'name': 'Alice',\n    'age': 30,\n    'city': 'New York'\n}\n\n# Creating a dictionary with the dict() function\nmy_dict = dict(name='Alice', age=30, city='New York')\n```\n\nAccessing and Modifying Elements\n\nYou can access dictionary values using their keys and modify them similarly.\n\n```python\n# Accessing values\nprint(my_dict['name'])  # Output: Alice\n\n# Modifying values\nmy_dict['age'] = 31\nprint(my_dict['age'])  # Output: 31\n```\n\nAdding and Removing Elements\n\nYou can add new key-value pairs and remove existing ones easily.\n\n```python\n# Adding a new key-value pair\nmy_dict['email'] = 'alice@example.com'\nprint(my_dict)\n\n# Removing a key-value pair using del\ndel my_dict['city']\nprint(my_dict)\n\n# Removing a key-value pair using pop\nemail = my_dict.pop('email')\nprint(email)\nprint(my_dict)\n```\n\nDictionary Methods\n\nPython dictionaries come with a variety of useful methods for manipulating their contents:\n\n- keys(): Returns a view object that displays a list of all the keys in the dictionary.\n- values(): Returns a view object that displays a list of all the values in the dictionary.\n- items(): Returns a view object that displays a list of dictionary's key-value tuple pairs.\n- update(): Updates the dictionary with elements from another dictionary object or from an iterable of key-value pairs.\n\n```python\n# Using dictionary methods\nkeys = my_dict.keys()\nvalues = my_dict.values()\nitems = my_dict.items()\n\nprint(keys)    # Output: dict_keys(['name', 'age'])\nprint(values)  # Output: dict_values(['Alice', 31])\nprint(items)   # Output: dict_items([('name', 'Alice'), ('age', 31)])\n\n# Updating a dictionary\nmy_dict.update({'city': 'Boston', 'age': 32})\nprint(my_dict)  # Output: {'name': 'Alice', 'age': 32, 'city': 'Boston'}\n```\n\nConclusion\n\nDictionaries are an essential part of Python, offering a versatile and efficient way to store and manage data. Their ability to quickly access, modify, and store key-value pairs makes them ideal for a wide range of applications, from simple data storage to complex data manipulation and retrieval tasks. Understanding how to effectively use dictionaries is crucial for any Python programmer."

            
            title="Introduction to Dictionary"
            return JsonResponse({'status': 'success', 'generatedResponse':gpt_response_simulation , 'title':title})
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
            performExtraction.delay(title)
            # Check task status
            print("Done 2")
            return redirect('First') 
        
    else:
        form = UploadForm()
    return render(request, 'first.html', {'form': form})
        

      
    