import os
from flask import Flask, render_template, request, redirect, url_for, send_file, session
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gallery.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['THUMBNAIL_FOLDER'] = 'static/thumbnails'
app.secret_key = "secret"
db = SQLAlchemy(app)

class ImageGallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    thumbnail_path = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    images = ImageGallery.query.all()
    return render_template("index.html", images=images)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        creator_name = request.form["creator_name"]
        caption = request.form["caption"]
        image = request.files["image"]

        if len(caption) < 50:
            return "Caption must be at least 50 characters long!", 400

        if not image.filename.endswith(('png', 'jpg', 'jpeg')):
            return "Only PNG and JPEG images are allowed!", 400

        img = Image.open(image)
        if img.width < 1024 or img.height < 1024 or img.width != img.height:
            return "Image must be square and at least 1024x1024px!", 400

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        img.save(image_path)

        img.thumbnail((250, 250))
        thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], "thumb_" + image.filename)
        img.save(thumbnail_path)

        new_image = ImageGallery(creator_name=creator_name, image_path=image_path, thumbnail_path=thumbnail_path, caption=caption)
        db.session.add(new_image)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("upload.html")

@app.route("/download/<int:image_id>")
def download(image_id):
    image = ImageGallery.query.get(image_id)
    
    if not image:
        return "Image not found!", 404

    if "downloaded_images" not in session:
        session["downloaded_images"] = []
    
    downloads = session["downloaded_images"]
    now = datetime.utcnow()
    downloads = [d for d in downloads if now - datetime.strptime(d["timestamp"], "%Y-%m-%d %H:%M:%S") < timedelta(hours=24)]

    if len(downloads) >= 2:
        return "You can only download 2 images within 24 hours!", 403

    downloads.append({"id": image_id, "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")})
    session["downloaded_images"] = downloads

    return send_file(image.image_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
