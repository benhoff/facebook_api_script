import os
import csv
import numpy
import cv2

if __name__ == '__main__':

    if not os.path.exists("pictures"):
        # FIXME: find some way to break out of the program
        print("the pictures directory does not exist, have you run get_pictures_from_facebook.py yet?")

    os.chdir('pictures')    
    _, _, filenames = next(os.walk("."))
    if 'face_coordinates.txt' in filenames:
        face_coord_txt_index = filenames.index('face_coordinates.txt')
        face_coord_txt_file = filenames.pop(face_coord_txt_index)
    else:
        face_coord_txt_file = raw_input("Enter Text Coordinate File Name,\
                                        or hit enter if None")

        # Allow user to decide if using a face coordinate text file
        # TODO: Decide if hit enter if this is not iterable
        if len(face_coord_txt_file) < 1:
            face_coord_txt_file = None
    
    face_coordinate_list = []
    if not face_coord_txt_file is None:
        with open(face_coord_txt_file, 'r') as csvfile:
            linereader = csv.reader(csvfile, delimiter=',', quotechar='\n')
            for row in linereader:
                result = []
                for item in row:
                    try:
                        result.append(float(item))
                    except ValueError:
                        result.append(None)
                face_coordinate_list.append(result)
    if not os.path.exists('../haarcascade_frontalface_default.xml'):
        print("Could not find haarcascade file!")
    face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(filenames[0])
   
    # Reads the image out of the file
    return_value, cv_frame = video_capture.read()

    # Turns image from BGR (color scheme) into gray!
    gray_image = cv2.cvtColor(cv_frame, cv2.COLOR_BGR2GRAY)
     
    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(cv_frame, (x,y),(w+w, y+h), (255, 0, 0), 2)
    
    # NOTE: This is the coordinates from facebook!
    if face_coordinate_list:
        image_height, image_width, _ = cv_frame.shape 

        # These are percentages!
        x_and_y_coordinates = face_coordinate_list[0][-2:]
        transformed_coords = (int(image_width/100 * x_and_y_coordinates[0]), 
                              int(image_height/100 * x_and_y_coordinates[1]))

        print(x_and_y_coordinates, transformed_coords, image_height, image_width)
        cv2.circle(cv_frame, transformed_coords, 20, (255, 106, 255))
        #cv2.rectangle(cv_frame, x_and_y_coordinates,(), (0, 255, 0), 2)


    while(True):
        cv2.imshow('{}'.format(filenames[0]), cv_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
