# A class concerning the PID controller
class PID:
    # @param kp: the value of the proportional action
    # @param kd: the value of the differential action
    # @param ki: the value of the integral action
    # @param precision: Stop the PID controller when a the error is less then the precission
    def __init__(self,kp,kd,ki,precision):
        try:
            self.__kp = float(kp)
            self.__kd = float(kd)
            self.__ki = float(ki)
            self.__precision = float(precision)
            self.__integral = 0
            self.__error = 0
        except:
            raise Error()
    # If the absolute vaule of the error is less then the precision 0 is returned
    # Else the new value is calculated
    def new_value(self,error,dt):
        if abs(error) < self.__precision:
             return 0 
        self.__integral += error *dt
        integral = self.__integral
        differential = (error - self.__error)/dt
        proportional = error
        self.__error = error
        return self.__kp*proportional + self.__kd*differential + self.__ki * integral


