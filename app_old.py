from flask import Flask, render_template ,request, jsonify
from flask_dropzone import Dropzone
import os

app = Flask(__name__)
dropzone = Dropzone(app)

app.config["DROPZONE_DEFAULT_MESSAGE"] = "拖拽模型到这里"
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.pt, .pth' 

import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

Net.load_state_dict(state_dict="./saved_model/cifar_net.pth")
cifar = Net()
cifar.eval()

import io

import torchvision.transforms as transforms
from PIL import Image

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(32, 32),
                                        
                                        transforms.ToTensor(),
                                        ])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

import torch



def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = cifar(tensor)
    _, y_hat = outputs.max(1)
    return y_hat

@app.route("/")
def index():
    return render_template("index.html")


@app.post("/upload/")
def upload():
    f = request.files.get('file')  # 获取文件对象
    f.save(os.path.join('saved_model', f.filename))  # 保存文件
    return "ok"

@app.post("/cifar/")
def cifar():
    file = request.files.get('file')  # 获取文件对象
    img_bytes = file.read()
    class_id, class_name = get_prediction(image_bytes=img_bytes)
    return jsonify({'class_id': class_id, 'class_name': class_name})




