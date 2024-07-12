import os
from django.db import models

class Upload(models.Model):
    title = models.CharField(max_length=100)
    email = models.EmailField()
    file = models.FileField(upload_to='uploads/')
    description = models.TextField(default="Default Discription")
    thumbnail = models.ImageField(upload_to='thumbnails/',default='dictionary.jpg')
    video_time = models.CharField(max_length=10, blank=True,default='00:00')  # This will be set in the view

    def save(self, *args, **kwargs):
        if self.file:
            # Extract the file extension
            file_extension = os.path.splitext(self.file.name)[1]
            # Create the new filename using the title
            new_filename = f"{self.title}{file_extension}"
            # Set the new filename
            self.file.name = new_filename

        if self.thumbnail:
            # Extract the file extension
            thumb_extension = os.path.splitext(self.thumbnail.name)[1]
            # Create the new filename using the title
            new_thumb_filename = f"{self.title}_thumb{thumb_extension}"
            # Set the new filename
            self.thumbnail.name = new_thumb_filename

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
