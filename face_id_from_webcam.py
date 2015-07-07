import os
import numpy
import cv2

VIDEO_DEVICE_INT = 1
LBPH_LABEL_NUM = 0

def _get_color_and_gray_frame_helper(capture_device):
        ret, frame = capture_device.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame, gray

def _detect_faces_helper(face_classifier, gray_frame):
    """
    Using shameful helper to make universal changes to the 
    detect method
    """
    height, width = gray_frame.shape
    min_size = (int(height/4), int(width/4)) 
    return face_classifier.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=2, flags=cv2.CASCADE_SCALE_IMAGE, minSize=min_size)


if __name__ == '__main__':
    haarcascade_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                        'haarcascade_frontalface_default.xml')

    face_classifier = cv2.CascadeClassifier(haarcascade_filepath)
    
    # should really test here and see if this number works
    print('Using device number: {}'.format(VIDEO_DEVICE_INT))
    capture_device = cv2.VideoCapture(VIDEO_DEVICE_INT)
    
    #FIXME:
    train_face = True
    print('If you want to train face, press `P`. else press `Q`')

    # This is the best loop ever! So much control
    while True:
        frame, gray = _get_color_and_gray_frame_helper(capture_device)
        faces = _detect_faces_helper(face_classifier, gray) 

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('YOUR FACE', frame)

        c = cv2.waitKey(1) & 0xFF

        if c == ord('q'):
            break
        elif c == ord('p'):
            train_face = True

    face_recognizer = cv2.face.createLBPHFaceRecognizer()
    
    # If training for face
    if (train_face):
        print('Training for Yo Face!')
        images = []
        number_of_images = 35
        labels = numpy.zeros(shape=(1, number_of_images), dtype=numpy.int32)
        
        # loop, 35 (?) times
        for _ in range(number_of_images):
            # don't really need the color frame here, just get gray
            _, gray = _get_color_and_gray_frame_helper(capture_device)
            # check for faces
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            
            # since we're assuming one face, if more assume bad data
            if len(faces) > 1:
                break
            (x, y, w, h) = faces[0]
            # This gets the region of interest out using the gray scale
            face_region_of_interest = gray[x:x+w, y:y+h]
            images.append(face_region_of_interest)

        face_recognizer.train(images, labels)
        face_recognizer.save('individual_face.xml')

    if not train_face:
        train_face_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                        'individual_face.xml')
        """
        if os.getenv("TRAINED_FACE"):
            print('Loading trained face from environmental variable')
            train_face_filepath = os.getenv("TRAINED_FACE")
        """
        face_recognizer.load(trained_face_filepath)

    print("Identifying your face!")
    while True:
        color, gray = _get_color_and_gray_frame_helper(capture_device)
        faces = _detect_faces_helper(face_classifier, gray)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
            face_region_of_interest = gray[x:x+w, y:y+h]
            precision, label = face_recognizer.predict(face_region_of_interest)
            print('Estimated Trained Face : {}'.format(precision))
        cv2.imshow('FACE', color)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
