Project Solution Description:
- 12 condition simulation
- aggressive response style; extreme increments in compressor speed, long wait times

---------------------------------------------------------------------------------------------------------
Non Variable PSA Output Flows (Intermittent): 
  PSA Section 1:
  Evac NA
  Blowdown goes to recycle tank
  
  PSA Section 2:
  Evacuation goes to BTA
  Blowdown goes to recycle tank
  
  PSA Section 3: 
  Evacuation goes to BTA
  Blowdown goes to recycle tank
  
  PSA New (Rotary):
  Evacuation NA
  Blowdown goes to BTB

Non Variable System Input Flows (Intermittent): 
  Buffer Tank A (BTA) – Evacuation from PSA 2 & 3
  Buffer Tank B (BTB) – Blowdown from Rotary PSA
  Recycle Tank – Blowdown from PSA 1, 2, and 3

-------------------------------------------------------------------------------------------------------
Volume Range States:

1. Recycle tank
   - maximum capacity of 7 cubic meters
   - Low (LO): 0.0 - 2.0 m³
   - Moderate (MOD): 2.0 - 4.5 m³
   - High (HI): 4.5 - 6.5 m³
   - High-High (HIHI): 6.5 - 7.0 m³
  
2. Buffer Tanks A & B
   - Low (LO): 0.0 - 1.1 m³
   - High (HI): 1.2 - 2.3 m³
   - High-High (HIHI): 2.3 - 2.5 m³
  
Chosen Compressor (from mechanical subteam 1): Bauer Gru 15 Biogas Compressor
  - Power: 100 - 125 HP (75 - 90 kW)
  - Flow rate: 144 - 537 scfm (245-997 m^3/hr)
  - Max discharge pressure: 232 psig (16 bar)
  - L X W X H: 100” x 130” x 117” (2.540 m x 3.886 m x 2.971 m)

  At 130 psi, the output flow rate from the Bauer GRU® 15 is   approximately 0.0313 m³/s.


Estimated Value Considerations:
- max output flow from buffer tanks
- max output flow from compressor

-------------------------------------------------------------------------------------------------------- 

Example pseudo code basic:

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
