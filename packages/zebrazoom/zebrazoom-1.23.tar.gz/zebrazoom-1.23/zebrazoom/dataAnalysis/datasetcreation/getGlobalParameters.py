import numpy as np
from scipy.interpolate import UnivariateSpline
import math

def getGlobalParameters(curbout, fps, pixelSize, frameStepForDistanceCalculation):

  BoutDuration = (curbout["BoutEnd"] - curbout["BoutStart"] + 1) / fps
  
  if "Bend_Timing" in curbout and type(curbout["Bend_Timing"]) == list:
    NumberOfOscillations = len(curbout["Bend_Timing"]) / 2
  else:
    NumberOfOscillations = float('NaN')
  
  TotalDistance = 0
  posX = curbout["HeadX"]
  posY = curbout["HeadY"]
  rangeUsedForDistanceCalculation   = [frameStepForDistanceCalculation*i for i in range(0, int(len(posX)/frameStepForDistanceCalculation))]
  if len(rangeUsedForDistanceCalculation) == 0:
    rangeUsedForDistanceCalculation = [0, len(posX) - 1]
  else:
    rangeUsedForDistanceCalculation = rangeUsedForDistanceCalculation + [len(posX) - 1]
  posX = [posX[i] for i in rangeUsedForDistanceCalculation]
  posY = [posY[i] for i in rangeUsedForDistanceCalculation]
  for j in range(0, len(posX)-1):
      TotalDistance = TotalDistance + math.sqrt((posX[j+1] - posX[j])**2 + (posY[j+1] - posY[j])**2)
  TotalDistance = TotalDistance * pixelSize
  
  
  Speed = TotalDistance / BoutDuration
  
  meanTBF = NumberOfOscillations / BoutDuration
  
  if "TailAngle_smoothed" in curbout and len(curbout["TailAngle_smoothed"]):
    maxAmplitude = max([abs(ta) for ta in curbout["TailAngle_smoothed"]])
  else:
    if "TailAngle_Raw" in curbout and len(curbout["TailAngle_Raw"]):
      maxAmplitude = max([abs(ta) for ta in curbout["TailAngle_Raw"]]) # Maybe this value should be "reduced" in some way to be consistent with the previous smoothed tail angle
    else:
      maxAmplitude = float('NaN')
  
  if "Bend_Timing" in curbout and type(curbout["Bend_Timing"]) == list and len(curbout["Bend_Timing"]):
    firstBendTime = curbout["Bend_Timing"][0]
  else:
    firstBendTime = float('NaN')
  
  if "Bend_Amplitude" in curbout and type(curbout["Bend_Amplitude"]) == list and len(curbout["Bend_Amplitude"]):
    firstBendAmplitude = abs(curbout["Bend_Amplitude"][0])
  else:
    firstBendAmplitude = float('NaN')
  
  if len(posY) >= 1:
    return [BoutDuration, TotalDistance, Speed, NumberOfOscillations, meanTBF, maxAmplitude, posY[0], posY[len(posY)-1], np.mean(posY), firstBendTime, firstBendAmplitude]
  else:
    return [BoutDuration, TotalDistance, Speed, NumberOfOscillations, meanTBF, maxAmplitude, 0, 0, 0, firstBendTime, firstBendAmplitude]
