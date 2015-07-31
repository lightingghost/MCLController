__author__ = 'lighting'

from ctypes import *
import time

#define pointer types for pointers using ctypes
p_int = POINTER(c_int)
p_uint = POINTER(c_uint)
p_double = POINTER(c_double)

class MMPStage:



    def __init__(self, driverPath):
        #Load driver
        self.mmpStage = cdll.LoadLibrary(driverPath)

        #Get stage handle
        self.handle = self.mmpStage.MCL_InitHandleOrGetExisting()
        if self.handle == 0:
            print("No Stage")

    def getInformation(self):
        encoderResolution = c_double()
        stepSize = c_double()
        maxVelocity = c_double()
        maxVelocityTwoAxis = c_double()
        maxVelocityThreeAxis = c_double()
        minVelocity = c_double()

        #The function need double* type in C lang.
        #ctypes.cast(adr,typ) can do this
        self.mmpStage.MCL_MicroDriveInformation(
            cast(addressof(encoderResolution),p_double),
            cast(addressof(stepSize),p_double),
            cast(addressof(maxVelocity),p_double),
            cast(addressof(maxVelocityTwoAxis),p_double),
            cast(addressof(maxVelocityThreeAxis),p_double),
            cast(addressof(minVelocity),p_double),
            self.handle
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
    #Distance: in mm
    #Velocity: in mm/s

    def moveDist(self,axis,distance,velocity):
        dict = {'X':1,'Y':2,'Z':3,'x':1,'y':2,'z':3,1:1,2:2,3:3}
        rounding = 2
        para = c_uint(dict[axis])
        status = self.mmpStage.MCL_MicroDriveMoveProfile(
            c_uint(dict[axis]),
            c_double(velocity),
            c_double(distance),
            c_int(rounding),
            self.handle
        )
        self.mmpStage.MCL_MicroDriveWait(self.handle)
        print(status)
        return 0

    def getPosition(self):
        x = c_double()
        y = c_double()
        z = c_double()
        self.mmpStage.MCL_MicroDriveReadEncoders(
            cast(addressof(x),p_double),
            cast(addressof(y),p_double),
            cast(addressof(z),p_double),
            self.handle
        )
        self.mmpStage.MCL_MicroDriveWait(self.handle)

        return (x.value,y.value,z.value)

    def moveTo(self,axis,position,velocity):
        dict = {'X':1,'Y':2,'Z':3,'x':1,'y':2,'z':3,1:1,2:2,3:3}
        instPos = self.getPosition()
        distance = position - instPos[dict[axis]-1]
        self.moveDist(axis,distance,velocity)
        return 0

    def exit(self):
        for i in range(1,4):
            self.moveTo(i,0.0,3.0)
        self.mmpStage.MCL_ReleaseHandle(self.handle)



if __name__ == '__main__':

    driverPath = 'C:\\Program Files\\Mad City Labs\\MicroDrive\\MicroDrive'
    stage = MMPStage(driverPath)
    stage.exit()
    #stage.moveDist('x',1,3)
    #stage.moveTo('z',0,3)

    list = stage.getPosition()
    for var in list:
        print(var)



