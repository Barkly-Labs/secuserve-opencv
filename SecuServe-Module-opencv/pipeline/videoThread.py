"""
this class is for hopefully geting opencv camera to thread correctly
"""

import util.const as const
import cv2
import queue
import threading

class ThreadingClass:

    # initiate threading class
    def __init__(self, name):

        if const.isdevpc:
            self.cap = cv2.VideoCapture(2)

        if const.isdevpc == False:
            self.cap = cv2.VideoCapture(name, cv2.CAP_GSTREAMER)

        # define an empty queue and thread
        self.q = queue.Queue()
        
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read the frames as soon as they are available
    # this approach removes OpenCV's internal buffer and reduces the frame lag
    def _reader(self):
        while True:
            ret, frame = self.cap.read()  # read the frames and ---
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)  # --- store them in a queue (instead of the buffer)

    def read(self):
        return self.q.get()  # fetch frames from the queue one by one

    def release(self):
        return self.cap.release()  # release the hw resource
