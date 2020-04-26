
import sys, os
from FramePhotoLib import PhotoFramer

if __name__ == "__main__":
  argnumber = len(sys.argv)-1
  if not 3 <= argnumber <= 4:
    raise Exception('USE THIS WAY: python kshhhactivate.py path/to/mockupdir path/to/photodir path/to/resultdir [blunt]')

  # Check all arguments are directories
  if not os.path.isdir(sys.argv[1]) or not os.path.isdir(sys.argv[2]) or not os.path.isdir(sys.argv[3]):
    raise Exception('Not all path are directories')

  # Format directories to absolute path
  mockupdir = os.path.abspath(sys.argv[1])
  photodir = os.path.abspath(sys.argv[2])
  resultdir = os.path.abspath(sys.argv[3])
  print("Use following directories:")
  print("Mockup: "+mockupdir)
  print("Photo: "+photodir)
  print("Result: "+resultdir)

  useBluntTransformation = False
  try:
    a = sys.argv[4]
    if a == "blunt":
      useBluntTransformation = True
  except:
    useBluntTransformation = False

  # Go do the job!
  framer = PhotoFramer(mockupdir, photodir, resultdir, useBluntTransformation)
  framer.assemble()
