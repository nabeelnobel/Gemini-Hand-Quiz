# hand_quiz.py
import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time

class QuizSystem:
    def __init__(self, csv_path="output_mcqs.csv"):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        self.detector = HandDetector(detectionCon=0.8)

        # Load questions
        with open(csv_path, newline='\n') as f:
            reader = csv.reader(f)
            dataAll = list(reader)[1:]

        self.mcqList = [self.MCQ(q) for q in dataAll]
        self.qNo = 0
        self.qTotal = len(dataAll)

        self.waitNext = False
        self.cooldownStart = 0

    class MCQ():
        def __init__(self, data):
            self.question = data[0]
            self.choice1 = data[1]
            self.choice2 = data[2]
            self.choice3 = data[3]
            self.choice4 = data[4]
            self.answer = int(data[5])
            self.userAns = None

        def update(self, cursor, bboxs, img):
            for x, bbox in enumerate(bboxs):
                x1, y1, x2, y2 = bbox
                if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                    self.userAns = x + 1
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)

    def get_frame(self):
        success, img = self.cap.read()
        if not success:
            return None
        img = cv2.flip(img, 1)
        hands, img = self.detector.findHands(img, flipType=False)

        if self.qNo < self.qTotal:
            mcq = self.mcqList[self.qNo]
            img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=30, border=3)
            img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=30, border=3)
            img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [550, 250], 2, 2, offset=30, border=3)
            img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=30, border=3)
            img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [550, 400], 2, 2, offset=30, border=3)

            if hands and not self.waitNext:
                lmList = hands[0]['lmList']
                cursor = lmList[8]
                length, info, _ = self.detector.findDistance(lmList[8][:2], lmList[12][:2])
                if length < 50:
                    mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4], img)
                    if mcq.userAns is not None:
                        self.waitNext = True
                        self.cooldownStart = time.time()

            if self.waitNext:
                elapsedTime = time.time() - self.cooldownStart
                if elapsedTime > 2:
                    self.qNo += 1
                    self.waitNext = False
        else:
            score = 0
            for mcq in self.mcqList:
                if mcq.answer == mcq.userAns:
                    score += 1
            score = round((score / self.qTotal) * 100, 2)
            img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=50, border=5)
            img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [700, 300], 2, 2, offset=50, border=5)

        barValue = 150 + (950 // self.qTotal) * self.qNo
        cv2.rectangle(img, (150, 600), (barValue, 650), (0, 255, 0), cv2.FILLED)
        cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
        img, _ = cvzone.putTextRect(img, f'{round((self.qNo / self.qTotal) * 100)}%', [1130, 635], 2, 2, offset=16)

        return img
