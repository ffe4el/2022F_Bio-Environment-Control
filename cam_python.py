import cv2
import numpy as np
from urllib.request import urlopen

url = "http://192.168.0.72/" #ESP CAM의 영상 스트리밍 주소
stream = urlopen(url)
buffer = b''

while True:
    buffer += stream.read(4096)
    head = buffer.find(b'\xff\xd8')
    end = buffer.find(b'\xff\xd9')
    try: #가끔 비어있는 버퍼를 받아 오류가 발생함. 이를 위한 try문
        if head > -1 and end > -1:
            jpg = buffer[head:end+2]
            buffer = buffer[end+2:]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            cv2.imshow("stream", img)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        #key = cv2.waitKey(1) if문으로 buffer를 확인하는데 delay를 주어 불필요한 지연 발생
        #if key == ord('q'):
            #break
	
    except:
    	pass
cv2.destroyAllWindows()
