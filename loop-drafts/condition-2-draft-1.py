import pandas as pd

def extract_pressure_values(file_path):
    """
    Reads an Excel file and extracts relevant pressure values.
    """
    try:
        # Load the Excel file
        xls = pd.ExcelFile(file_path)
        
        # Load sheets
        gas_composition_df = pd.read_excel(xls, sheet_name="Gas Composition")
        cycle_times_df = pd.read_excel(xls, sheet_name="Cycle Times")
        
        # Extract RECYCLE_TANK_Pressure from Cycle Times (Assuming it's labeled as 'Online Pressure')
        recycle_tank_pressure = cycle_times_df.loc[cycle_times_df.iloc[:, 0] == "Online Pressure", "Unnamed: 1"].values
        recycle_tank_pressure = recycle_tank_pressure[0] if len(recycle_tank_pressure) > 0 else None
        
        # Extract BTA_Pressure and BTB_Pressure from Gas Composition (Assumption needed)
        # Searching for pressure-related values in the gas composition sheet
        bta_pressure = gas_composition_df.loc[gas_composition_df.iloc[:, 0] == "BTA Pressure", "Unnamed: 1"].values
        btb_pressure = gas_composition_df.loc[gas_composition_df.iloc[:, 0] == "BTB Pressure", "Unnamed: 1"].values
        
        bta_pressure = bta_pressure[0] if len(bta_pressure) > 0 else None
        btb_pressure = btb_pressure[0] if len(btb_pressure) > 0 else None
        
        return {
            "RECYCLE_TANK_Pressure": recycle_tank_pressure,
            "BTA_Pressure": bta_pressure,
            "BTB_Pressure": btb_pressure
        }
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Example usage:
# file_path = "PSA Flows (Updated).xlsx"
# pressure_values = extract_pressure_values(file_path)
# print(pressure_values)
