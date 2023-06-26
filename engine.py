import numpy as np
import math as m

class engine:
    
    
    def __init__(self, number, location, maxthrust, maxGimble = False, restAngle = m.pi/2):
        """# Engine class
        
        Defines parameters for engines on vehicle. 
        
        To specify multiple unique parameters (i.e. position) enter a list of positions. If a parameter is global it must be not iterable (i.e. maxthrust = 100 [N]) or of length 1 (i.e. gimble [[15,15]]).
        
        Goal is to make this generalised for 2 or 3 dimensions (which is why gimble can require two values)
        
        This is recursive class. Engine is called with parameters for all individual engines and it calls itself and specifies the parameters for all individual engines. Individual engines should ever be created by input unless there is 1.
        
        Right now if you want a single engine vehicle it won't work :/ so create 2 engines with half max thrust in the same position. #Feature not a bug
        also Gimble is symetrical by default complex mapping is for later
        And no negative thrust
        But think about what you do have

        Args:
            number (int): Number of engines on vehicle
            location (list): location of engines relative to vehicle datum
            maxthrust (int or list): Maximum allowed thrust [N] can be different for different engines
            gimble (bool, int or list): Can allow engines to gimble to some angle relative to rest angle. For 2D angle in degree, for 3D (azimuthal angle, radial angle)
            restAngle (bool, int or list): Set resting angle of engine relative to plain of vehicle
        """
        
        if number == 1:
            if maxGimble == False:
                maxGimble = 0
            if restAngle == False:
                restAngle = 0
            
            self.location = location
            self.maxThrust = maxthrust
            self.maxGimble = maxGimble
            self.throttle = 0
            self.restAngle = restAngle
            self.gimble = 0
        else:
            if maxGimble == False:
                maxGimble = [0] * number
            if restAngle == False:
                restAngle = [0] * number
            
            location,maxthrust,maxGimble = [[i] * number if not iterable(i)  else i for i in [location,maxthrust,maxGimble]]
            location,maxthrust,maxGimble = [i * number if len(i) == 1 else i for i in [location,maxthrust,maxGimble]]

            
            self.engine = [engine(1, i,j,k) for i,j,k in zip(location, maxthrust, maxGimble)]
            self.count = number
        
    def set_Throttle(self, throttle):
        # Get argument throttle and make it or make sure it is a list of length engine.count
        if not iterable(throttle):
            throttle = [throttle] * self.count
        elif len(throttle) != self.count:
            raise SyntaxError(f'Incorrect amount of throttle positions given [{len(throttle)}] expected {self.count}')
        
        # Ensure correctly bounded in [0,1]
        throttle = [max(i,0) for i in throttle]
        throttle = [min(i,1) for i in throttle]
        
        # Assign individual engines their throttle values
        for idx, throtPos in enumerate(throttle):
            self.engine[idx].throttle = throtPos
        
    def set_Gimble(self, gimble):
        # Get argument gimble and make it or make sure it is a list of length engine.count
        if not iterable(gimble):
            gimble = [gimble] * self.count
        elif len(gimble) != self.count:
            raise SyntaxError(f'Incorrect amount of gimble positions given [{len(gimble)}] expected {self.count}')
        elif len(gimble) == self.count:
            # Check for engines without gimble (i.e. gimble False)
            for idx, gim in enumerate(gimble):
                if gim > self.engine[idx].maxGimble:
                    
                    gimble[idx] = False
                    print(f'Warning: Engine number {idx} cannot gimble')
                
        for idx, gim in enumerate(gimble):
            self.engine[idx].gimble = gim

    def get_Throttle(self):
        return [i.throttle for i in self.engine]
    
    def get_Thrust(self):
        """ # Get Thrust
        Returns thrust vector [N] relative to vehicle
        """
        F = np.array([0,0])
        
        for eng in self.engine:
            F = np.add(np.matmul([eng.throttle * eng.maxThrust,0], rotMat(eng.restAngle + eng.gimble)), F)
        
        return F

    def increment_Throttle(self, inc):
        # Get argument throttle and make it or make sure it is a list of length engine.count
        if not iterable(inc):
            inc = [inc] * self.count
        elif len(inc) != self.count:
            raise SyntaxError(f'Incorrect amount of throttle positions given [{len(inc)}] expected {self.count}')
        
        self.set_Throttle([i+j for i,j in zip(inc, self.get_Throttle())])
            
    
    def get_Torque(self):
        """ # Get Torque
        Returns torque provided by the engines [N*M] on the vehicle
        """
        τ = 0
        for eng in self.engine:
            τ = np.add(np.cross(eng.location, np.matmul([eng.throttle * eng.maxThrust,0], rotMat(eng.restAngle + eng.gimble))), τ)
            
        return τ
                
def iterable(a):
    try:
        iter(a)
        return True
    except TypeError:
        return False
    
rotMat = lambda x: np.array([[m.cos(x), -m.sin(x)],[m.sin(x), m.cos(x)]])

if __name__ == '__main__':
    eng = engine(number= 4, location = [[-2,1, 0 ], [2,1, 0],[-2,-1, 0 ], [2,-1, 0]],maxthrust= 100, maxGimble= False)
    eng.set_Throttle([0.9,1])
    print(eng.get_Throttle())
    print(eng.get_Torque())
