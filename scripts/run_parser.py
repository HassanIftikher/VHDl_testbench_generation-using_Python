from vhdl_parser import parse_vhdl_file

if __name__ == "__main__":
    input_vhdl_file = 'src/d_flip_flop.vhdl'  # Path to your VHDL file
    output_json_file = 'src/vhdl_module.json'  # Output JSON file

    # Parse the VHDL and save to JSON
    parsed_entity = parse_vhdl_file(input_vhdl_file, output_json_file)

    print("Parsed VHDL entity saved to JSON in 'src/' folder:", parsed_entity)

