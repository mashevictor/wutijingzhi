#-coding:utf-8-*-
import cv2
import time

save_path = './face/'
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

camera = cv2.VideoCapture(0) # 参数0表示第一个摄像头

# 判断视频是否打开
if (camera.isOpened()):
    print('Open')
else:
    print('摄像头未打开')

# 测试用,查看视频size
size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('size:'+repr(size))

fps = 5  # 帧率
pre_frame = None  # 总是取视频流前一帧做为背景相对下一帧进行比较
i = 0
while True:
    start = time.time()
    grabbed, frame_lwpCV = camera.read() # 读取视频流
    gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY) # 转灰度图
    print(gray_lwpCV.shape)
    #gray_lwpCV = cv2.resize(gray_lwpCV, (50, 50))
    # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
    gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0) 

    if pre_frame is None:
        pre_frame = gray_lwpCV
    else:
        img_delta = cv2.absdiff(pre_frame, gray_lwpCV)
        thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) < 1: # 设置敏感度
                continue
            else:
                print("咦,有什么东西在动0.0")
                break
        pre_frame = gray_lwpCV
    cv2.imshow('lwpCVWindow', frame_lwpCV)

    key = cv2.waitKey(1) & 0xFF
    # 按'q'健退出循环
    if key == ord('q'):
        break
# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()
