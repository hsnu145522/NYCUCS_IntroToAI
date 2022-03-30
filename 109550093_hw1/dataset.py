import os
import cv2

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")
    
    
    '''
    explaintation of part 1:
    First, set the datapath to dataPath/face.
    Second, use a for loop to put all the files under dataPath/face in to the list(dataset).
    For each file, use cv2.imread to get the image's information, which gives us a numpy array(img).
    Notice that I give imread an argument "cv2.IMREAD_GRAYSCALE", in order to get grayscale data.
    For files in dataPath/face, set the tuple's second element to 1.
    Reapeat the above steps with datapath set to dataPath/non-face.
    Finally, return dataset.
    '''
    dataset = []
    dataPath1 = dataPath+"/face"
    for filename in os.listdir(dataPath1):
        img = cv2.imread(os.path.join(dataPath1,filename),cv2.IMREAD_GRAYSCALE)
        if img is not None:
            tup = (img,1)
            dataset.append(tup)
        
    dataPath1 = dataPath+"/non-face"
    for filename in os.listdir(dataPath1):
        img = cv2.imread(os.path.join(dataPath1,filename),cv2.IMREAD_GRAYSCALE)
        if img is not None:
            tup = (img,0)
            dataset.append(tup)
    # End your code (Part 1)
    return dataset
