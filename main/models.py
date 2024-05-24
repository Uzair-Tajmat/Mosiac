import os
from django.db import models

class Upload(models.Model):
    title = models.CharField(max_length=100)
    email = models.EmailField()
    file = models.FileField(upload_to='uploads/')

    def save(self, *args, **kwargs):
        if self.file:
            # Extract the file extension
            file_extension = os.path.splitext(self.file.name)[1]
            # Create the new filename using the title
            new_filename = f"{self.title}{file_extension}"
            # Set the new filename
            self.file.name = new_filename

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
