import sys
import os
from vhdl_parser import parse_vhdl_file

def main():
    if len(sys.argv) != 3:
        print("Usage: python run_parser.py <input_vhdl_file> <output_json_file>")
        sys.exit(1)
    
    input_vhdl_file = sys.argv[1]
    output_json_file = sys.argv[2]

    if not os.path.isfile(input_vhdl_file):
        print(f"Error: Input VHDL file '{input_vhdl_file}' does not exist.")
        sys.exit(1)

    try:
        parsed_entity = parse_vhdl_file(input_vhdl_file, output_json_file)
        print(f"Parsed VHDL entity saved to JSON: {parsed_entity}")
    except Exception as e:
        print(f"Error while parsing VHDL file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

