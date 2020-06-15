from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import itertools
import time

vs = VideoStream(src=1).start()

blueLower = np.array([99, 104, 86])
blueUpper = np.array([128, 188, 176])

yellowLower = np.array([22, 101, 100])
yellowUpper = np.array([39, 255, 255])

yellowBounds = (yellowLower, yellowUpper)
blueBounds = (blueLower, blueUpper)


def loop(colorBounds, iterator):
    counter = 0

    text_found_ball = "Ball found"
    text_caught = "Ball caught"
    text_found_goal = "Goal found"
    text_scorred = "Ball scorred"

    while True:
        frame = vs.read()

        if frame is None:
            break

        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, colorBounds[0], colorBounds[1])

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if len(cnts) > 0:
            for cnt in cnts:
                ((x, y), rayon) = cv2.minEnclosingCircle(cnt)

                if rayon > 60:
                    cv2.circle(frame, (int(x), int(y)), int(rayon),
                               (0, 0, 255), 3)

                    if (colorBounds[0] == blueBounds[0]).all():
                        print(text_found_ball)
                    else:
                        print(text_found_goal)

                if rayon > 250:
                    if (colorBounds[0] == blueBounds[0]).all():
                        print(text_caught)
                        time.sleep(2.0)
                    else:
                        print(text_scorred)
                        time.sleep(2.0)

                    loop(iterator(), iterator)

            cv2.imshow("Frame", frame)

            key = cv2.waitKey(1) & 0xFF
            counter += 1

            if key == ord("q"):
                break


toggle = itertools.cycle([yellowBounds, blueBounds]).__next__
loop(blueBounds, toggle)

vs.stop()
cv2.destroyAllWindows()
