from pwm_calibrate import PWMCalibrator

PIN_CALIBRATION_FILES = ((1, 'pin1_calibration.json'), (5, 'pin5_calibration.json'), (6, 'pin6_calibration.json'))

def calibrate():
   for (pin, filename) in PIN_CALIBRATION_FILES:
      calibrator = PWMCalibrator(pin, filename)
      print "Preparing to calibrate pin %d..." % pin
      x = raw_input('[press <enter> to continue]')
      calibrator.calibrate()
      calibrator.save()

def load_calibrators():
   calibrators = {}
   for (pin, filename) in PIN_CALIBRATION_FILES:
      calibrators[pin] = PWMCalibrator(pin, filename)
      calibrators[pin].load()
   return calibrators

if __name__=='__main__':
   calibrate()
