import sys, os
from PIL import Image

def testMockup(mockuppath, framesize, framecoordinates):
  testfilepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"imageformockuptest.jpg")
  photo_im = Image.open(testfilepath)
  mockup_im = Image.open(mockuppath)

  # If trying portrait, transpose test image
  if framesize[1] > framesize[0]:
    photo_im = photo_im.transpose(Image.ROTATE_90)

  # Create result image
  framed_im = Image.new('RGB', mockup_im.size)
  # Add mockup
  framed_im.paste(mockup_im, (0,0))
  # Resize photo to space size
  resizedphoto_im = photo_im.resize(framesize)
  # Add photo to frame at coordinates
  framed_im.paste(resizedphoto_im, framecoordinates)
  # Save result in working dir
  framed_im.save(os.path.join(os.getcwd(), 'isItFramedOk.jpg'))

  # Helper for frame name in case it's good
  print("If this result is good (meaning you dimensioned the frame correctly and the photo fits perfectly in it), you should rename the frame as follows in order to use it as a frame for kshhhactivate:")
  mockupname = "landscape"
  if framesize[0] < framesize[1]:
    mockupname = "portrait"
  elif framesize[0] == framesize[1]:
    mockupname = "square"
  mockupname += "-s"+str(framesize[0])+"x"+str(framesize[1])
  mockupname += "c"+str(framecoordinates[0])+"x"+str(framecoordinates[1])
  mockupname += "-"+os.path.basename(mockuppath)
  print(mockupname)
  answer = input("Rename mockup to suggested name? y/N ")
  if answer == 'Y' or answer == 'y':
    resultfile = os.path.join(os.path.dirname(mockuppath),mockupname)
    os.rename(r''+mockuppath, r''+resultfile)
    print("File renamed, now ready to use with kshhhactivate.py")

# Will handle main here before handing off to mockup test function
if __name__ == "__main__":
  argnumber = len(sys.argv)-1
  if not 4 <= argnumber <= 5:
    raise Exception('USE THIS WAY: python kshhhtest.py path/to/mockup framewidth [frameheight] framestartx framestarty')

  # Check mockup is an image
  mockuppath = sys.argv[1]
  try:
    Image.open(mockuppath)
  except:
    raise Exception('Mockup is not an image file')

  # Check frame in mockup dimensions are all numbers
  (framewidth,frameheight,framestartx,framestarty) = (0,0,0,0)
  try:
    framewidth = int(sys.argv[2])

    # If 3 arguments, frameheight is framewidth -> square
    # If 4 arguments, different argument for framewidth
    frameheightindex = argnumber - 2

    frameheight = int(sys.argv[frameheightindex])
    framestartx = int(sys.argv[frameheightindex+1])
    framestarty = int(sys.argv[frameheightindex+2])
  except:
    raise Exception('Some frame dimensions are not numbers')

  if framewidth <= 0 or frameheight <= 0 or framestartx <= 0 or framestarty <= 0:
    raise Exception('Some frame dimensions are negative')

  # Go do the job!
  testMockup(mockuppath, (framewidth, frameheight), (framestartx, framestarty))

