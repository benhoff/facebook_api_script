#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/face/facerec.hpp>
#include <iostream>
#include <stdio.h>
#include <tuple> // std::tuple<type1, type2>

// Global!
cv::Mat frame;

std::vector<cv::Rect> detect_faces(cv::Mat gray_frame,
                                   cv::CascadeClassifier classifier)
{
    std::vector<cv::Rect> result;
    classifier.detectMultiScale(gray_frame, result, 1.1, 2,
                                0|cv::CASCADE_SCALE_IMAGE,
                                cv::Size(frame.cols/4, frame.rows/4));

    return result;
}

std::tuple<cv::Mat, cv::Mat> get_color_and_gray_frame(cv::VideoCapture video_capture)
{
    cv::Mat gray_frame;

    video_capture.read(frame);
    cv::cvtColor(frame, gray_frame, cv::COLOR_BGR2GRAY);
    return std::make_tuple(frame, gray_frame);
}

int main(int argc, const char *argv[])
{
    cv::String haarcascade_string("/home/hoff/swdev/facebook_haar_generator/haarcascade_frontalface_default.xml");
    cv::CascadeClassifier face_classifier(haarcascade_string);

    cv::VideoCapture video_capture(0);

    std::cout << "Running initial face detect!" << std::endl;
    bool train_face;

    while(true)
    {
        // 0 index is color, 1 index is gray
        auto frames = get_color_and_gray_frame(video_capture);

        std::vector<cv::Rect> faces = detect_faces(std::get<1>(frames),
                                                   face_classifier);
        for(size_t i=0; i<faces.size(); i++)
            cv::rectangle(std::get<0>(frames), faces[i], cv::Scalar( 255, 0, 255 ));

        cv::imshow("image", frame);
        int c = cv::waitKey(10);
        if (c == 1113864)
        {
            train_face = true;
            break;
        }
        if (c == 1048586)
            break;
    }
    cv::Ptr<cv::face::FaceRecognizer> model = cv::face::createLBPHFaceRecognizer();

    if (train_face)
    {
        std::cout << "Training LPBH for your Face!" << std::endl;
        std::vector<cv::Mat> images;
        std::vector<int> labels;
    // Right now defaulting to 20 images.

        for(size_t i=0; i<150; i++)
        {
           // Assume that there is only one face
            labels.push_back(0);
            // 0 index is color, 1 index is gray
            auto frames = get_color_and_gray_frame(video_capture);

            std::vector<cv::Rect>faces = detect_faces(std::get<1>(frames),
                                                      face_classifier);

            for(size_t i=0; i<faces.size(); i++)
            {
                cv::Mat face_region_of_interest = std::get<1>(frames)(faces[i]);
                images.push_back(face_region_of_interest);
            }
        }
        model->train(images, labels);
        model->save("individual_face.xml");
    }
    if (!train_face)
        model->load("/home/hoff/swdev/facebook_haar_generator/individual_face.xml");
    std::cout << "Indentifying your Face!" << std::endl;
    while(true)
    {
        double percision;
        int label = 0;

        // 0 index is color, 1 index is gray
        auto frames = get_color_and_gray_frame(video_capture);

        std::vector<cv::Rect> faces = detect_faces(std::get<1>(frames),
                                                   face_classifier);

        for(size_t i=0; i<faces.size(); i++)
        {
            cv::rectangle(std::get<0>(frames),
                          faces[i],
                          cv::Scalar( 255, 0, 255 ));

            cv::Mat face_region_of_interest = std::get<1>(frames)(faces[i]);
            model->predict(face_region_of_interest, label, percision);
            std::cout << "Estimated Match: " << percision << std::endl;
        }

        cv::imshow("image", frame);
        int c = cv::waitKey(10);
        if ((char)c == 'q')
            break;
    }

    video_capture.~VideoCapture();
    face_classifier.~CascadeClassifier();
    cv::destroyAllWindows();
}
