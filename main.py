import cv2
from flask import Flask, request, send_file

from LaneLineDetector import lane_finding_pipeline
from videoDetector import videodetect

app = Flask(__name__,
            static_url_path='',
            static_folder='/static')


@app.route('/')
def home():
    return send_file('frontEnd/home.html', attachment_filename='home.html')


@app.route('/image', methods=['POST'])
def image():
    if (request.method == 'POST'):
        # print('in post')
        f = request.files['file']
        f.save('test.jpg')
        image = cv2.imread('test.jpg')
        resimage = lane_finding_pipeline(image)
        cv2.imwrite('result/result1.jpg', resimage)
        return send_file('result.jpg', attachment_filename='result.jpg')


@app.route('/video', methods=['POST'])
def video():
    if (request.method == 'POST'):
        # print('in post')
        f = request.files['file']
        f.save('test2.mp4')
        videodetect();
        return send_file('frontEnd/videodisplay.html', attachment_filename='videodisplay.html')


if __name__ == "__main__":
    app.run()
