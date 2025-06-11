import os
import argparse
import json
from pathlib import Path
from src.vhdl_parser import parse_vhdl_file
from src.testbench_generator import TestBenchGenerator
from src.makefile_generator import generate_makefile

def main():
    parser = argparse.ArgumentParser(
        description='Generate VHDL testbench, Makefile, and JSON output'
    )
    parser.add_argument('vhdl_file', help='Input VHDL file')
    parser.add_argument(
        '--output-dir',
        default='generated',
        help='Output directory'
    )
    parser.add_argument(
        '--json-only',
        action='store_true',
        help='Only generate JSON output'
    )
    args = parser.parse_args()

    try:
        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Parse VHDL and generate JSON
        vhdl_file = Path(args.vhdl_file)
        json_output = output_dir / f"{vhdl_file.stem}_parsed.json"
        
        print(f"Parsing VHDL file: {vhdl_file}")
        entity_dict = parse_vhdl_file(vhdl_file, json_output)
        print(f"Generated JSON output: {json_output}")
        
        if args.json_only:
            return
            
        # Generate testbench
        tb_dir = Path('tb')
        tb_dir.mkdir(exist_ok=True)
        
        print("Generating testbench")
        print(f"JSON output file: {json_output}")
        print(f"JSON file exists: {json_output.exists()}")
        
        if json_output.exists():
            with open(json_output, 'r') as f:
                print(f"JSON content: {json.load(f)}")
        
        # Pass the string representation of the JSON file path
        tb_generator = TestBenchGenerator(str(json_output))
        tb_output = tb_dir / f"test_{vhdl_file.stem}.py"
        tb_generator.save_testbench(tb_output)
        print(f"Generated testbench: {tb_output}")
        print(f"Testbench file exists: {tb_output.exists()}")
        
        # Generate Makefile
        print("Generating Makefile")
        generate_makefile(
            entity_dict=entity_dict,
            vhdl_file=vhdl_file,
            output_dir=str(output_dir)
        )
        print("Generated Makefile")

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == '__main__':
    main()
