import os
import cv2
from crop_pictures import CropFace

file_dir = os.path.dirname(os.path.realpath(__file__))

cropped_photos_dir = os.path.join(file_dir, 
                                  'cropped_photos', 
                                  '')

eye_cascade_filepath = os.path.join(file_dir, 'haarcascade_eye.xml')
eye_classifier = cv2.CascadeClassifier(eye_cascade_filepath)

all_cropped_photos = os.listdir(cropped_photos_dir)

eye_coord_list = []
for photo_filename in all_cropped_photos:
    image = cv2.imread(photo_filename)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    eyes = eye_classifier.detectMultiScale(gray_image, 1.1, 2, 0|cv2.CASCADE_SCALE_IMAGE, (30, 30))
    if len(eyes) > 2:
        print('More eyes than you can shake a stick at!')
    if len(eyes) < 2:
        print('less eyes than you should have. Or pirate')

    # NOTE: Assumes it returns in the same order, left to right
    """
    for (x, y, w, h) in eyes:
        center_eye = (int(x + w/2), int(y+h/2))
        eye_coord_list.append(center)
    """
    if len(eyes) > 2:
        resized_image = CropImage(image, eye[0], eye[1])
        resize_image.save()
    

# Now we want to align the images by the eyeballs

