import os
import time
from flask import Flask, request, render_template

app = Flask(__name__)
print(app.instance_path)
print(app.root_path)
print(app.static_folder)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/uploads/", methods=['POST'])
def upload():
    # 获取文件
    file = request.files.get("pic")
    if not file:
        return render_template('index.html')
    # file_name = time.strftime("%Y-%m-%d-%H-%M-%S") + file.filename
    file_name = file.filename
    file_url = f'/static/{file_name}'
    file.save(os.path.join(
        app.root_path,
        app.static_folder,
        file_name
    ))
    return file_url


if __name__ == '__main__':
    app.run(debug=True)
