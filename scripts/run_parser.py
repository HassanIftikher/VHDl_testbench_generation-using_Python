
from vhdl_parser import parse_vhdl_file
import os

def get_vhdl_file_path():
    """
    Interactively prompt the user to enter the path to the VHDL file.
    Provides input validation and supports relative and absolute paths.
    """
    while True:
        # Prompt user for file path
        file_path = input("Enter the path to your VHDL file: ").strip()
        
        # Expand any user home directory shortcuts
        file_path = os.path.expanduser(file_path)
        
        # Check if file exists
        if os.path.isfile(file_path):
            # Verify file has .vhdl or .vhd extension
            if file_path.lower().endswith(('.vhdl', '.vhd')):
                return file_path
            else:
                print("Error: The file must have a .vhdl or .vhd extension.")
        else:
            print(f"Error: The file '{file_path}' does not exist. Please check the path.")

def main():
    try:
        # Get VHDL file path from user
        input_vhdl_file = get_vhdl_file_path()
        
        # Generate output JSON filename based on input file
        output_json_file = 'src/vhdl_module.json'
        
        # Parse the VHDL and save to JSON
        parsed_entity = parse_vhdl_file(input_vhdl_file, output_json_file)
        
        print(f"Parsed VHDL entity saved to JSON: {output_json_file}")
        print("Parsed Entity Details:", parsed_entity)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
