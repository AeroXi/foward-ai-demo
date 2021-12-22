from flask import Flask, render_template ,request, jsonify
from flask_dropzone import Dropzone
import os
import requests

app = Flask(__name__)
dropzone = Dropzone(app)

app.config["DROPZONE_DEFAULT_MESSAGE"] = "拖拽模型到这里"
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.pt, .pth, .mar' 
app.config['DROPZONE_MAX_FILE_SIZE'] = 1000  # unit: MB
app.config['DROPZONE_TIMEOUT'] = 3600000  # unit: ms
app.config['DROPZONE_REDIRECT_VIEW'] = 'models'

SAVE_DIR = "/home/ubuntu/model/"
MODEL_MANAGE_URL = "http://172.16.3.104:8081"

@app.route("/")
def index():
    return render_template("index.html")


@app.post("/upload/")
def upload():
    f = request.files.get('file')  # 获取文件对象
    f.save(os.path.join(SAVE_DIR, f.filename))  # 保存文件
    requests.post(f"{MODEL_MANAGE_URL}/models?url={f.filename}&initial_workers=2")
    return "ok"

@app.route("/models/")
def models():
    r = requests.get(f"{MODEL_MANAGE_URL}/models/")
    return render_template("models.html", data=r.text)



