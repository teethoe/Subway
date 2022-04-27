# SubwayCarPhotomosaic  
  
Auto-matches tape colours using computer vision and stitch pictures of each side together.  
  
[!alt text](https://github.com/teethoe/SubwayCarPhotomosaic/blob/master/sample%202%20(2).png?ref=true)  
  
For each side of the subway, the corners are found using Harris Corner detection, and the images would be cropped and perspective fixed using the corners. Then the images are passed through the KMeans clustering algorithm with n=5 as the highest number of colours that is supposedly to be found is 5 including the white colour of the subway itself. Then the sides are matched using the HSV values found.  
  
[!alt text](https://github.com/teethoe/SubwayCarPhotomosaic/blob/master/Subway%20Flowchart.png?ref=true)  
