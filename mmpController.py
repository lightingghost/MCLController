__author__ = 'lighting'

from ctypes import *

class MMPStage:

    mmpStage = False

    def __init__(self, driverPath):

        #Load driver
        mmpStage = cdll.LoadLibrary(driverPath)

        #Get stage handle
        self.handle = mmpStage.MCL_InitHandleOrGetExisting()
        if self.handle == 0:
            print("No Stage")

    def getInformation(self):
        encoderResolution = c_double()
        stepSize = c_double()
        maxVelocity = c_double()
        maxVelocityTwoAxis = c_double()
        maxVelocityThreeAxis = c_double()
        minVelocity = c_double()
        mmpStage.MCL_MicroDriveInformation(
            encoderResolution,
            stepSize,
            maxVelocity,
            maxVelocityTwoAxis,
            maxVelocityThreeAxis,
            minVelocity
        )
        return (
            encoderResolution.value,
            stepSize.value,
            maxVelocity.value,
            maxVelocityTwoAxis.value,
            maxVelocityThreeAxis.value,
            minVelocity.value
        )


    #Move a specific axis of a specific distance at a specific velocity
    #axis: X=1, Y=2, Z=3
    def moveDist(self,axis,distance,velocity):
        dict = {'X':1,'Y':2,'Z':3,'x':1,'y':2,'z':3,1:1,2:2,3:3}
        rounding = 0
        mmpStage.MCL_MicroDriveMoveProfile(
            c_uint(dict[axis]),
            c_double(velocity),
            c_double(distance),
            c_int(rounding)
            self.handle
        )
        return 0

    def getPosition(self):
        x = c_double()
        y = c_double()
        z = c_double()
        mmpStage.MCL_MicroDriveReadEncoder(x,y,z,self.handle)

        return (x.value,y.value,z.value)

    def moveTo(self,axis,position,velocity):
        dict = {'X':1,'Y':2,'Z':3,'x':1,'y':2,'z':3,1:1,2:2,3:3}
        instPos = self.getPosition()
        distance = position - instPos[dict[axis]]
        self.moveDist(axis,distance,velocity)
        return 0

    def exit(self):
        for i range(1,4):
            self.moveTo(i,0.0,1.0)
        mmpStage.MCL_ReleaseHandle(self.handle)



if __name__ == '__main__':

    drivePath = ''
    stage = MMPStage(drivePath)
    stage.moveTo(x,1,1)
    stage.moveTo(y,1,1)
    stage.moveTo(z,1,1)

