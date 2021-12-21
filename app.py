from flask import Flask, render_template ,request, jsonify
from flask_dropzone import Dropzone
import os

app = Flask(__name__)
dropzone = Dropzone(app)

app.config["DROPZONE_DEFAULT_MESSAGE"] = "拖拽模型到这里"
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.pt, .pth, .mar' 
app.config['DROPZONE_MAX_FILE_SIZE'] = 1000  # unit: MB

SAVE_DIR = "saved_model"

@app.route("/")
def index():
    return render_template("index.html")


@app.post("/upload/")
def upload():
    f = request.files.get('file')  # 获取文件对象
    f.save(os.path.join(SAVE_DIR, f.filename))  # 保存文件
    return "ok"






