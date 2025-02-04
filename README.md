# Image Gallery Web Application

This is a simple image gallery web application built using Flask and SQLAlchemy. 

Users can upload images, view thumbnails, and download images with a limit on how many images can be downloaded within a 24-hour period. 

![image](https://github.com/user-attachments/assets/26670332-d02a-4a98-a224-c303a0078b5a)

![image](https://github.com/user-attachments/assets/6b32325f-180f-4c49-9d36-aacb2a38d195)

Features:

Flask App: Build a responsive image upload system using python(flask).
Image Validation: Allow only PNG/JPEG, square-shaped (1024px min), and 50+ character captions.
Thumbnail: Create a 250x250px thumbnail and store paths in the database.
Image List: Display images with captions, creator names, and thumbnails.
Download: Add a download button for each image.
Download Limit: Restrict users to 2 downloads within 24 hours.
