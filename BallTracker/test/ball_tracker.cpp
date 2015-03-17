/*
 * Joseph Bolling and Ankush Gola
 * C++ port of ball tracking module
 */

#include<iostream>
#include<opencv2/opencv.hpp>
#include<sys/time.h>
using namespace std;
using namespace cv;

int main()
{
    VideoCapture capture(0);
    if(!capture.isOpened()){
        cout << "Failed to connect to the camera." << endl;
    }

    for(int i = 0; i < 20; i++){
        struct timeval start, image_aquired, end;
        struct timezone tz;
        double get, process;
        gettimeofday(&start,&tz);

        //get a frame
        Mat frame, hsv, mask;
        capture >> frame;
        if(frame.empty()){
            cout << "Failed to capture an image" << endl;	
            continue;
        }
        gettimeofday(&image_aquired,&tz);

        //HSV conversion
        cvtColor(frame, hsv, CV_BGR2HSV);
    
        //Normal masking algorithm
        Vec3i lower_blue(175, 68, 126);
        Vec3i upper_blue(185, 255, 247);
        inRange(hsv,lower_blue,upper_blue,mask);
        
        //Morphological operations
        Mat kernel_close = getStructuringElement(MORPH_RECT,Size(21,21));
        Mat kernel_open = getStructuringElement(MORPH_RECT,Size(11,11));
        morphologyEx(mask,mask,MORPH_CLOSE,kernel_close);
        morphologyEx(mask,mask,MORPH_OPEN,kernel_open);
    
        //Blur image
        GaussianBlur(mask, mask, Size(15,15), 0);
        
        //Detect circles 
        vector<Vec3f> circles;
        HoughCircles(mask,circles,CV_HOUGH_GRADIENT,1,1600,50,20,0,0);
        
        gettimeofday(&end,&tz);
        long seconds, useconds;
        seconds = image_aquired.tv_sec-start.tv_sec;
        useconds = image_aquired.tv_usec-start.tv_usec;
        get = seconds * 1000 + useconds/1000.0;
        seconds = end.tv_sec - image_aquired.tv_sec;
        useconds = end.tv_usec - image_aquired.tv_usec; 
        process = seconds * 1000 + useconds/1000.0;
        cout << get << " ";
        cout << process;
        cout <<  endl;
    }
    return 0;
}
