from vhdl_parser import parse_vhdl_file
import os
if __name__ == "__main__":
    input_vhdl_file = 'src/counter_with_enable.vhdl'  # Path to your VHDL file
    output_json_file = 'src/vhdl_module.json'  # Output JSON file

    # Ensure that the src directory exists
    if not os.path.exists('src'):
        print("Error: 'src' directory does not exist.")
        exit(1)

    # Ensure that the input VHDL file exists
    if not os.path.exists(input_vhdl_file):
        print(f"Error: VHDL file '{input_vhdl_file}' does not exist.")
        exit(1)

    try:
        # Parse the VHDL file and save the JSON output
        parsed_entity = parse_vhdl_file(input_vhdl_file, output_json_file)

        # Check if the output JSON file was successfully created
        if os.path.exists(output_json_file):
            print(f"Success: Parsed VHDL entity saved to JSON in '{output_json_file}'")
        else:
            print(f"Error: JSON file '{output_json_file}' was not created.")
    except Exception as e:
        print(f"An error occurred: {e}")

