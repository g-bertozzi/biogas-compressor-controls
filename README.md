Project Solution Description:
- 8 condition simulation
- aggressive response style; binary choice, extreme thresholds
- implementation in Python3
- read input data from Excel for testing

Ideal condition: low pressure in Recycle Tank, Buffer Tank A, Buffer Tank B
Threshold for compressor speed [25:100]

Example loop:

For (recycle_tank = low, BTA = high, BTB = low):
  
  If BTA valve is closed: open
  
  If Comp_speed < lowest_speed  + 5:  	! if comp_speed can be lowered then lower
    comp_speed = comp_speed - 5
    
  Temp = current pressure in BTA   ! section to test change in pressure in Buffer Tank A
  
  WAIT 10
  
  Derivative = Temp - current pressure in BTA   ! check BTA derivative of pressure
  If derivative < 0: WAIT 10 		! pressure is lowering, allow it to continue
  Else if > 0: open exhaust line from BTA 			! pressure is continuing to rise thus must alleviate build up

END
