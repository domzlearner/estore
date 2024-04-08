from django.contrib import admin
from .models import Category, Product

import shutil
import os
import logging
from django.core.files.storage import default_storage

class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Call the parent class's save_model method to save the object
        super().save_model(request, obj, form, change)

        # Check if an image file is associated with the product
        if obj.image:
            # Get the file's path in the media storage
            media_path = obj.image.path  # Use obj.image.path to get the file's absolute path

            # Construct the destination path in the static storage
            static_path = os.path.join('images', os.path.basename(media_path))

            # Remove the old image file if it exists
            if change and form.initial['image']:
                old_media_path = form.initial['image'].path  # Use .path to get the absolute path of the old image
                old_static_path = os.path.join('images', os.path.basename(old_media_path))
                try:
                    default_storage.delete(old_static_path)
                except FileNotFoundError:
                    pass

            # Copy the image file from media to static directory
            try:
                with default_storage.open(media_path, 'rb') as source_file:
                    with default_storage.open(static_path, 'wb') as dest_file:
                        shutil.copyfileobj(source_file, dest_file)
            except FileNotFoundError:
                # Handle the case where the file does not exist in media storage
                pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)