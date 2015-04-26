import os
import csv
import numpy
import cv2
def parse_face_coord_file(face_coord_txt_file=None):
    result = []
    if not face_coord_txt_file is None:
        with open(face_coord_txt_file, 'r') as csvfile:
            linereader = csv.reader(csvfile, delimiter=',', quotechar='\n')
            result = []
            for row in linereader:
                temp = []
                for item in row:
                    try:
                        temp.append(float(item))
                    except ValueError:
                        temp.append(None)
                result.append(tuple(temp))
    return result

def display_images(filenames, face_cascade, face_coordinate_list=None):
    for index, file in enumerate(filenames):
        # Reads the image out of the file
        cv_frame = cv2.imread(file)
        # Turns image from BGR (color scheme) into gray!
        gray_image = cv2.cvtColor(cv_frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)
        print(faces)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(cv_frame, (x,y),(w+w, y+h), (255, 0, 0), 2)
        
        # NOTE: This is the coordinates from facebook!
        if face_coordinate_list:
            image_height, image_width, _ = cv_frame.shape 

            # Facebook keeps coords as percentages!
            if face_coordinate_list:
                x_and_y_coordinates = face_coordinate_list[index][-2:]
                if not x_and_y_coordinates[0] is None:
                    transformed_coords = (int(image_width/100 * x_and_y_coordinates[0]), 
                                          int(image_height/100 * x_and_y_coordinates[1]))

                    cv2.circle(cv_frame, transformed_coords, 20, (255, 106, 255))


        while(True):
            cv2.imshow('{}'.format(filenames[index]), cv_frame)
            cv2.imshow('gray', gray_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyWindow(filenames[index])

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
    
    face_coordinate_list = parse_face_coord_file(face_coord_txt_file)

    if not os.path.exists('../haarcascade_frontalface_default.xml'):
        print("Could not find haarcascade file!")

    face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')

    # this functionality needs to be looped/changed
    display_images(filenames, face_cascade, face_coordinate_list)
    
    cv2.destroyAllWindows()
