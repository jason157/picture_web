from flask import Flask
from flask import render_template
import os
import base64

app = Flask(__name__)


@app.route('/')
def index():
    base_path = ".\\static\\images".replace("\\", "/")

    dir_links, image_tags = whatever(base_path)

    return render_template('index.html', path_list=dir_links, file_list=image_tags)


@app.route("/<clicked_path>" , methods=['GET', 'POST'])
def dealing_dir_input(clicked_path):
    """
    处理传进来的路径, 是这样的 base64.encode(/static/images/xxx)
    :return:
    """
    the_path = base64.b64decode(clicked_path.replace("*", "/")).decode()
    # print('the_path', the_path)
    dir_links, image_tags = whatever(the_path)

    return render_template('index.html', path_list=dir_links, file_list=image_tags)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


def whatever(base_path):
    dirs, files = get_content_list(base_path)
    # print("-------", dirs, files)
    image_tags = []
    for file in files:
        if file.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
            image_tag = '<p><img style="%s" alt="%s" src="/static/images/%s"></p>' % ("width:100%", file, file)
            image_tags.append(image_tag)
    # print(image_tags)

    dir_links = []
    for d in dirs:
        url = base64.b64encode(d.encode(encoding="utf-8")).decode(encoding='utf-8').replace("/", "*")
        title = d.split('/')[-1]
        link = """<p><a href="%s">%s</a></p>""" % (url, title)
        dir_links.append(link)
    return dir_links, image_tags


def get_content_list(base_path):
    """
    读取目录下的文件和目录
    :param base_path:
    :return: dir_list, file_list
    """
    if os.path.isfile(base_path):
        return [], [base_path]
    contents = os.listdir(base_path)
    file_list = []
    dir_list = []
    for c in contents:
        f = os.path.join(base_path, c)
        file_list.append(f.replace("\\", "/")) if os.path.isfile(f) else dir_list.append(f.replace("\\", "/"))

    tmp = []
    for file in file_list:
        tmp.append(file.split('images')[-1])
    file_list = tmp

    return dir_list, file_list


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")
