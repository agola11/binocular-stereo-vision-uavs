/*
 * Joseph Bolling and Ankush Gola
 * C++ port of ball tracking module
 */

#include<iostream>
#include<opencv2/opencv.hpp>
using namespace std;
using namespace cv;

int main()
{
    VideoCapture capture(0);
    if(!capture.isOpened()){
	    cout << "Failed to connect to the camera." << endl;
    }
    Mat frame, hsv, mask;
    vector<Vec3f> circles;
    capture >> frame;
    if(frame.empty()){
		cout << "Failed to capture an image" << endl;
		return -1;
    }
    cvtColor(frame, hsv, CV_BGR2HSV);

    //Normal masking algorithm
    Vec3i lower_blue(175, 68, 126);
    Vec3i upper_blue(185, 255, 247);
    inRange(hsv,lower_blue,upper_blue,mask);

    //other stuff here
    
    //blur image
    GaussianBlur(mask, mask, Size(15,15), 0);

    //detect circles
    return 0;
}
