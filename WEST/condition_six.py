import time
import pandas as pd
from system import System 
from sensor_data import parse_input

# Define constants for system settings
FILE_PATH = 'non-variable-input-flows.xlsx'

# Valve positions (%)
FULLY_OPEN = 1
FULLY_CLOSED = 0

# Compressor speed settings (%)
SPEED_INCREMENT = 20

# Valve settings for tanks
BTA_VALVE_INITIAL = 0.5
BTB_VALVE_INITIAL = 0.5

def main():
    """Main function to simulate the system's operation using the System class."""
    # Initialize the system with initial volumes and valve positions
    system = System(
        recycling_volume = 4.0,
        bta_volume = 0.3,
        btb_volume = 2.0,
        compressor_speed = 50,
        valve_BA = BTA_VALVE_INITIAL,
        valve_BB = BTB_VALVE_INITIAL
    )

    # Simulating sensor data reading from an Excel file
    flowrates = parse_input(FILE_PATH)
    flow_rate_index = 1

    # Main loop: Continue operation while conditions hold
    while (system.volume_threshold('recycling') == 'MOD' and
           system.volume_threshold('bta') == 'LO' and
           system.volume_threshold('btb') == 'HI'):
        
        # Check the BTB valve and make sure it is fully open because the tank is full
        if system.valve_BB != FULLY_OPEN:
            system.adjust_valve_position('BB', FULLY_OPEN)

        # Check if we can increase comp speed, then increase it
        if system.compressor_speed < (system.max_compressor_speed - SPEED_INCREMENT):
            system.adjust_compressor_speed(SPEED_INCREMENT)
       
        # Check the BTA valve and make sure it is fully closed because the tank is low
        if system.valve_BA != FULLY_CLOSED:
            system.adjust_valve_position('BA', FULLY_CLOSED)

        # Store the initial pressure to track change in BTB and Recycle tank
        orginal_btb_volume = system.btb_volume
        original_recycle_volume = system.recycling_volume

        # Wait for the pressure to change
        system.changes_in_tanks(flowrates, flow_rate_index)
        flow_rate_index += 10

        # Simulate pressure changes (replace this with actual sensor data later)
        recycle_volume_change = system.recycling_volume - original_recycle_volume
        btb_volume_change = system.btb_volume - orginal_btb_volume

        # CASE 1: BTB DEC & Recycle Tank DEC
        # CASE 2: BTB DEC & Recycle Tank INC
        # CASE 3: BTB INC & Recycle Tank DEC
        # CASE 4: BTB INC & Recycle Tank INC

        # CASE 1: BTB DEC & Recycle Tank DEC - ideal, wait
        if recycle_volume_change < 0 and btb_volume_change < 0:
            print(f"Ideal: Recycle tank pressure decreased by {abs(recycle_volume_change)} units.")
            system.changes_in_tanks(flowrates, flow_rate_index)
            flow_rate_index += 10
        
        # CASE 2: BTB DEC & Recycle Tank INC - bad, do something or switch conditions?
        elif recycle_volume_change >= 0 and btb_volume_change < 0:
            print(f"Condition Change: Recycle tank pressure increased by {abs(recycle_volume_change)} units, but BTB pressure decreased by {abs(btb_volume_change)} units.")
            print(f"Switching to Condition 9: Recycle tank pressure high, BTA & BTB pressure low.")

        # CASE 3: BTB INC & Recycle Tank DEC - bad, purge BTB or switch conditions?
        elif recycle_volume_change < 0 and btb_volume_change >= 0:
            print(f"Not ideal: Recycle tank pressure decreased by {abs(recycle_volume_change)} units, but BTB pressure increased by {abs(btb_volume_change)} units.")
            
            # if BTB is HIHI then purge
            if system.volume_threshold('btb') == 'HIHI':
                system.purge_tank('btb')

        # CASE 4: BTB INC & Recycle Tank INC - worst case, 
        elif recycle_volume_change >= 0 and system.compressor_speed <= (system.max_compressor_speed - SPEED_INCREMENT):
            print(f"Not ideal: Pressure increased by {abs(recycle_volume_change)} units.")
            system.adjust_compressor_speed(SPEED_INCREMENT)
            print(f"Compressor speed increased to {system.compressor_speed}%")

            # if BTB is HIHI then purge
            if system.volume_threshold('btb') == 'HIHI':
                system.purge_tank('btb')

            # if Recycle Tank is HIHI then purge
            if system.volume_threshold('recycling') == 'HIHI':
                system.purge_tank('recycling')

if __name__ == "__main__":
    main()
