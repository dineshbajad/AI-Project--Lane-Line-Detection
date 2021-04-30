import cv2

from LaneLineDetector import lane_finding_pipeline

def videodetect():
    cap = cv2.VideoCapture('test2.mp4')
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    size = (frame_width, frame_height)
    result = cv2.VideoWriter('result/result2.mp4',
                             cv2.VideoWriter_fourcc(*"H264"),
                             10, size)
    i = 0;
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = lane_finding_pipeline(frame)
            result.write(frame)
            # cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
        i = i + 1
        if (i == 50):
            break

    cap.release()
    result.release()
    cv2.destroyAllWindows()

