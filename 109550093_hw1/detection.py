import os
import cv2
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    # raise NotImplementedError("To be implemented")

    '''
    explanation of Part 4:
    First, open the txt file which contains the filenames, number of faces, position/width/height of faces.
    set the variable filename as filename, nFace as number of faces.
    Second, since there will be nFace lines of information, use a for loop to run nFace times.
    For each loop, get the information from the txt file, x,y,w,h. 
    Turn them into integers, so as to use them to slice lists.
    Crop the file(with the filename) into 19x19 gray scale list.(crop_img1)
    Third, check if clf.classify(crop_img1) is True.
    If it's true, then draw a green grid on the formal image;otherwise, red grid.
    Finally, show the picture with grids drawn.
    '''
    fd = open(dataPath, 'r')
    while True:
        line = fd.readline()
        if len(line)==0:
            break
        filename, nFace = line.split()
        filename = 'data/detect/'+filename
        img = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
        img1 = cv2.imread(filename)

        dataset = []
        for times in range(int(nFace)):
            line = fd.readline()
            x,y,w,h = line.split()
            x=int(x)
            y=int(y)
            w=int(w)
            h=int(h)
            crop_img = img[y:y+h, x:x+w]
            crop_img1 = cv2.resize(crop_img,(19,19), interpolation=cv2.INTER_AREA)
            if clf.classify(crop_img1):
                cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 255, 0), 4, cv2.LINE_AA)
                '''
                for i in range(h):
                    for j in range(w):
                        if i!=0 and i!=h-1:
                            if j!=0 and j!=w-1:
                                continue
                            else:
                                pass
                                #img1[y+i][x+j] = [0,255,0]
                        else:
                            pass
                            #img1[y+i][x+j] = [0,255,0]
                '''
                        
            else:
                cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 0, 255), 4, cv2.LINE_AA)
                '''
                for i in range(h):
                    for j in range(w):
                        if i!=0 and i!=h-1:
                            if j!=0 and j!=w-1:
                                continue
                            else:
                                pass
                                #img1[y+i][x+j] = [0,0,255]
                        else:
                            pass
                            #img1[y+i][x+j] = [0,0,255]
                '''
        img_rgb = img1[:,:,::-1]
        plt.imshow(img_rgb)
        plt.show()

    fd.close()

    # End your code (Part 4)
