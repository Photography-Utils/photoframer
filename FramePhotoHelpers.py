


SQUARE_RATIO_DEFAULT_TOLERANCE = 0.02

def getOrientation(width, height, squaretolerance = SQUARE_RATIO_DEFAULT_TOLERANCE):
  if 1-squaretolerance <= height/width <= 1+squaretolerance:
    return  "square"
  elif width >= height:
    return "portrait"
  elif height <= width:
    return "landscape"
