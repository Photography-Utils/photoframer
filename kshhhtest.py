import sys, os
from PIL import Image

def testFrame(framepath, photopath, spacesize, spacecoordinates):
  photo_im = Image.open(photopath)
  frame_im = Image.open(framepath)

  # Create result image
  framed_im = Image.new('RGB', frame_im.size)
  # Add frame
  framed_im.paste(frame_im, (0,0))
  # Resize photo to space size
  resizedphoto_im = photo_im.resize(spacesize)
  # Add photo to frame at coordinates
  framed_im.paste(resizedphoto_im, spacecoordinates)
  # Save result in working dir
  framed_im.save(os.path.join(os.getcwd(), 'test.jpg'))

  # Helper for frame name in case it's good
  print("If this result is good (meaning you dimensioned the frame correctly and the photo fits perfectly in it), you should rename the frame as follows in order to use it as a frame for kshhhactivate:")
  framename = "landscape"
  if spacesize[0] < spacesize[1]:
    framename = "portrait"
  elif spacesize[0] == spacesize[1]:
    framename = "square"
  framename += "-s"+str(spacesize[0])+"x"+str(spacesize[1])
  framename += "c"+str(spacecoordinates[0])+"x"+str(spacecoordinates[1])
  framename += "-"+os.path.basename(framepath)
  print(framename)

# Will handle main here before handing off to frame test function
if __name__ == "__main__":
  if len(sys.argv)-1 != 6:
    raise Exception('USE THIS WAY: python testframe.py path/to/frametotest path/to/anyphoto framewidth frameheight framestartx framestarty')

  # Check photo and frame are images
  framepath = sys.argv[1]
  photopath = sys.argv[2]
  try:
    Image.open(framepath)
    Image.open(photopath)
  except:
    raise Exception('Photo file and/or photo frame are not image files')

  # Check dimensions are all numbers
  (framewidth,frameheight,coordx,coordy) = (0,0,0,0)
  try:
    framewidth = int(sys.argv[3])
    frameheight = int(sys.argv[4])
    coordx = int(sys.argv[5])
    coordy = int(sys.argv[6])
  except:
    raise Exception('Some dimensions are not numbers')

  if framewidth <= 0 or frameheight <= 0 or coordx <= 0 or coordy <= 0:
    raise Exception('Some dimensions are negative')

  # Go do the job!
  testFrame(framepath, photopath, (framewidth, frameheight), (coordx, coordy))

