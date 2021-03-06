from utility import *

# A class concerning the PID controller
class PID:
    # @param kp: the value of the proportional action
    # @param kd: the value of the differential action
    # @param ki: the value of the integral action
    # @param precision: Stop the PID controller when a the error is less then the precission
    def __init__(self,kp,ki,kd,precision):
        try:
            self.__kp = float(kp)
            self.__kd = float(kd)
            self.__ki = float(ki)
            self.__precision = float(precision)
            self.__integral = 0
            self.__previous_error = 0
        except:
            raise Error()
    # If the absolute vaule of the error is less then the precision 0 is returned
    # Else the new value is calculated
    def value(self,error,dt):
        if abs(error) < self.__precision:
             return 0
        self.__integral +=  error *dt
        integral = self.__integral
        differential = (error - self.__previous_error)/dt
        proportional = error
        self.__previous_error = error
        return self.__kp*proportional + self.__ki * integral + self.__kd*differential
# A class concerning the PD controller
class PD:
    # @param kp: the value of the proportional action
    # @param kd: the value of the differential action
    # @param precision: Stop the PID controller when a the error is less then the precission
    def __init__(self,kp,kd,precision):
        try:
            self.__kp = float(kp)
            self.__kd = float(kd)
            self.__precision = float(precision)
            self.__previous_error = 0
        except:
            raise Error()
    # If the absolute vaule of the error is less then the precision 0 is returned
    # Else the new value is calculated
    def value(self,error,dt):
        if abs(error) < self.__precision:
             return 0
        differential = (error - self.__previous_error)/dt
        proportional = error
        self.__previous_error = error
        return self.__kp*proportional + self.__kd*differential
