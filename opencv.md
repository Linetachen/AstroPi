How openCV works:
from https://www.youtube.com/watch?v=wlYPhdTbRmk
- when you load an image it extracts the pixels and loads them into a numPy array
- numpy - high performance array library within python
- when you print(img.shape) it gives the channels which is used for colour in an rgb format (bgr)
- in format [0,0,0]
- for colour anylasis (future reference): https://www.youtube.com/watch?v=ddSo8Nb0mTw
- it uses the openCV ORB (oriented fast and rotated brief) https://www.youtube.com/watch?v=0sPlnrEMyYk
- Runs FAST detector to get a selection of features
- Narrows down to N keypoints by using Harris corners
- Applies scale pyramid
- moments are computed
- uses BRIEF to obtain feature descriptor
- Steers BREIF to find the correct orientation at 12 degree increments using a lookup table
- Runs greedy algorithm to find unique features by finding features with high variance and mean close to 0.5
- Uses LSH to approximate nearest neighbor search - groups similar items
- hamming distance - used to compare distance between two descriptors
