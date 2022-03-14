# SubwayCarPhotomosaic

Auto-matches tape colours using computer vision and stitch pictures of each side together.

Please look at "Subway Flowchart.png" for a visual description of the algorithm.

Sample result included.

For each side of the subway, the corners are found using Harris Corner detection, and the images would be cropped and perspective fixed using the corners. Then the images are passed through the KMeans clustering algorithm with n=5 as the highest number of colours that is supposedly to be found is 5 including the white colour of the subway itself. Then the sides are matched using the HSV values found.
