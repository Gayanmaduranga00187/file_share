from flask import Flask, request, render_template_string, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

# Save Uploaded Files to 'uploads' Folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# HTML Template with Delete, Download, and Styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Share App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #1e90ff, #f0e68c); /* Blue and yellow gradient */
            color: #333;
            padding: 20px;
            text-align: center;
        }
        h2 {
            color: #d9534f;
        }
        form {
            margin: 20px 0;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin: 5px 0;
        }
        a {
            text-decoration: none;
            color: #337ab7;
        }
        button {
            margin-left: 10px;
            background-color: #d9534f;
            color: white;
            border: none;
            padding: 5px 10px;
            cursor: pointer;
        }
        button:hover {
            background-color: #c9302c;
        }
        .download-btn {
            background-color: #5cb85c;
        }
        .download-btn:hover {
            background-color: #4cae4c;
        }
        input[type="file"] {
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <h2>Upload Files</h2>
    <form method="POST" action="/" enctype="multipart/form-data">
        <input type="file" name="file" multiple>
        <button type="submit">Upload</button>
    </form>
    <h2>Uploaded Files</h2>
    <ul>
        {% for file in files %}
        <li>
            <a href="/uploads/{{ file }}" target="_blank">{{ file }}</a>
            <form method="POST" action="/delete/{{ file }}" style="display:inline;">
                <button type="submit">Delete</button>
            </form>
            <a href="/download/{{ file }}">
                <button class="download-btn">Download</button>
            </a>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
'''

# Home Route for File Upload
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        uploaded_files = request.files.getlist("file")
        for file in uploaded_files:
            if file:
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML_TEMPLATE, files=files)

# Route to Serve Uploaded Files
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Route to Download a File
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# Route to Delete a File
@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for("upload_file"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
