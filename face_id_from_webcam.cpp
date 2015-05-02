#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/face/facerec.hpp>
#include <iostream>
#include <stdio.h>

int main(int argc, const char *argv[])
{

    cv::String haarcascade_string("/home/hoff/swdev/facebook_haar_generator/haarcascade_frontalface_default.xml");
    cv::CascadeClassifier face_classifier;
    bool loaded = face_classifier.load(haarcascade_string);
    cv::VideoCapture video_capture(1);
    cv::RNG rng(12345);

    cv::Mat frame;
    // This loops you in the GUI until you're ready to run!
    while(true)
    {
        cv::Mat gray_frame;
        std::vector<cv::Rect> faces;

        video_capture.read(frame);
        cv::cvtColor(frame, gray_frame, cv::COLOR_BGR2GRAY);

        face_classifier.detectMultiScale(gray_frame, faces, 1.1, 2,
                                         0|cv::CASCADE_SCALE_IMAGE,
                                         cv::Size(frame.cols/4, frame.rows/4));

        for(size_t i=0; i<faces.size(); i++)
        {
            cv::rectangle(frame, faces[i], cv::Scalar( 255, 0, 255 ));
            cv::Mat face_region_of_interest = gray_frame(faces[i]);
        }

        cv::imshow("image", frame);
        int c = cv::waitKey(10);
        if ((char)c == 'q')
            break;
    }

    std::vector<cv::Mat> images;
    std::vector<int> labels;
    cv::Ptr<cv::face::FaceRecognizer> model = cv::face::createLBPHFaceRecognizer();

    // Right now defaulting to 20 images.
    for(size_t i=0; i<20; i++)
    {
		std::vector<cv::Rect> faces;
        labels.push_back(i);
        cv::Mat gray_frame;
        video_capture.read(frame);
        cv::cvtColor(frame, gray_frame, cv::COLOR_BGR2GRAY);

        face_classifier.detectMultiScale(gray_frame, faces, 1.1, 2,
                                         0|cv::CASCADE_SCALE_IMAGE,
                                         cv::Size(frame.cols/4, frame.rows/4));

        for(size_t i=0; i<faces.size(); i++)
        {
            cv::rectangle(frame, faces[i], cv::Scalar( 255, 0, 255 ));
            cv::Mat face_region_of_interest = gray_frame(faces[i]);
            images.push_back(face_region_of_interest);
        }
    }
    model->train(images, labels);
    model->save("individual_face.xml");
    video_capture.~VideoCapture();
    face_classifier.~CascadeClassifier();
    cv::destroyAllWindows();
}
