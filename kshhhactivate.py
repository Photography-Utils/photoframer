
from FramePhotoLib import PhotoFramer

if __name__ == "__main__":
  framer = PhotoFramer('../Frames/', '../Photos', '../Results')
  framer.assemble()
