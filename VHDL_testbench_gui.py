import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import os
import re
import json
import subprocess
from scripts.vhdl_parser import parse_vhdl
# Import the testbench generation functions from the new script
from scripts.testbench_generator import generate_testbench, load_vhdl_data

class VHDLTestbenchGenerator:
    def __init__(self, master):
        self.master = master
        master.title("VHDL Testbench Generator")
        master.geometry("800x700")

        # Create main frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # VHDL Module Input Section
        self.input_label = tk.Label(self.main_frame, text="Paste VHDL Module:", font=("Arial", 12))
        self.input_label.pack(anchor="w")

        self.input_text = scrolledtext.ScrolledText(self.main_frame, height=15, wrap=tk.WORD)
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Buttons Frame
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(0, 10))

        self.parse_button = tk.Button(self.button_frame, text="Parse Module", command=self.parse_vhdl_module)
        self.parse_button.pack(side=tk.LEFT, padx=(0, 5))

        self.generate_button = tk.Button(self.button_frame, text="Generate Testbench", command=self.generate_testbench)
        self.generate_button.pack(side=tk.LEFT, padx=(0, 5))

        self.save_button = tk.Button(self.button_frame, text="Save Testbench", command=self.save_testbench)
        self.save_button.pack(side=tk.LEFT, padx=(0, 5))

        self.run_simulation_button = tk.Button(self.button_frame, text="Run Simulation", command=self.run_simulation)
        self.run_simulation_button.pack(side=tk.LEFT)

        # Output Section
        self.output_label = tk.Label(self.main_frame, text="Testbench Preview:", font=("Arial", 12))
        self.output_label.pack(anchor="w")

        self.output_text = scrolledtext.ScrolledText(self.main_frame, height=10, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Simulation Log Section
        self.sim_log_label = tk.Label(self.main_frame, text="Simulation Log:", font=("Arial", 12))
        self.sim_log_label.pack(anchor="w")

        self.sim_log_text = scrolledtext.ScrolledText(self.main_frame, height=5, wrap=tk.WORD)
        self.sim_log_text.pack(fill=tk.BOTH, expand=True)

        # Class variables to store parsed data
        self.parsed_vhdl_data = None
        self.entity_name = None

    def parse_vhdl_module(self):
        """Parse the VHDL module and create a JSON representation"""
        vhdl_content = self.input_text.get("1.0", tk.END).strip()

        if not vhdl_content:
            messagebox.showerror("Error", "Please paste a VHDL module first.")
            return

        try:
            # Create src directory if it doesn't exist
            os.makedirs("src", exist_ok=True)
            
            # First parse the content to get the entity name
            temp_vhdl_file = os.path.join("src", "temp_module.vhdl")
            with open(temp_vhdl_file, "w") as f:
                f.write(vhdl_content)
            
            # Use the parse_vhdl function
            parsed_data = parse_vhdl(temp_vhdl_file)
            
            # Extract entity name
            self.entity_name = parsed_data.get('name', '')
            
            if not self.entity_name:
                messagebox.showerror("Error", "Could not extract entity name from VHDL module.")
                return
                
            # Save the actual VHDL module file with entity name
            module_file = os.path.join("src", f"{self.entity_name}.vhdl")
            with open(module_file, "w") as f:
                f.write(vhdl_content)
            
            # Store the parsed data
            self.parsed_vhdl_data = {
                "vhdl_entity": parsed_data,
                "metadata": {
                    "parser_version": "1.0"
                }
            }
            
            messagebox.showinfo("Success", f"VHDL module parsed and saved as: {module_file}\nEntity name: {self.entity_name}")

        except Exception as e:
            messagebox.showerror("Parsing Error", str(e))
    def generate_testbench(self):
        """Generate testbench based on parsed VHDL module"""
        if not self.parsed_vhdl_data:
            messagebox.showerror("Error", "Please parse the VHDL module first.")
            return

        try:
            # Create src directory if it doesn't exist
            if not os.path.exists("src"):
                os.makedirs("src")
                
            # Generate testbench filename
            tb_file = f"{self.entity_name}_tb.vhdl"
            tb_path = os.path.join("src", tb_file)
            
            # First ensure the parsed data is saved to a JSON file
            json_path = os.path.join("src", "vhdl_module.json")
            with open(json_path, 'w') as f:
                json.dump(self.parsed_vhdl_data, f, indent=4)
            
            # Use the generate_testbench function from the testbench generator script
            generate_testbench(self.parsed_vhdl_data, tb_path)
            
            # Check if the file was created successfully
            if os.path.exists(tb_path):
                # Read the generated testbench
                with open(tb_path, "r") as f:
                    testbench_content = f.read()
                
                # Display the generated testbench in the output area
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, testbench_content)

                messagebox.showinfo("Success", f"Testbench generated: {tb_file}")
            else:
                messagebox.showerror("Error", f"Failed to generate testbench file at {tb_path}")

        except Exception as e:
            messagebox.showerror("Testbench Generation Error", str(e))

    def save_testbench(self):
        """Save the edited testbench file"""
        if not self.entity_name:
            messagebox.showerror("Error", "No testbench to save. Generate a testbench first.")
            return

        try:
            # Get the edited testbench content from the output_text
            tb_file = f"{self.entity_name}_tb.vhdl"
            testbench_content = self.output_text.get("1.0", tk.END).strip()

            # Save the edited content to the file
            with open(os.path.join("src", tb_file), "w") as f:
                f.write(testbench_content)

            messagebox.showinfo("Success", f"Testbench saved: {tb_file}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def run_simulation(self):
        """Run the simulation script"""
        if not self.entity_name:
            messagebox.showerror("Error", "Please parse and generate a testbench first.")
            return

        try:
            # Ensure the testbench is saved before running the simulation
            self.save_testbench()

            # Example simulation command
            simulation_command = f"ENTITY_NAME={self.entity_name} bash scripts/run_simulation.sh"

            # Run the simulation command
            process = subprocess.Popen(simulation_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Update simulation log
            self.sim_log_text.delete("1.0", tk.END)
            self.sim_log_text.insert(tk.END, stdout.decode("utf-8") + stderr.decode("utf-8"))

            if process.returncode == 0:
                messagebox.showinfo("Simulation", "Simulation completed successfully!")
            else:
                messagebox.showerror("Simulation Error", "Simulation failed. Check the log for details.")

        except Exception as e:
            messagebox.showerror("Simulation Error", str(e))


def main():
    root = tk.Tk()
    app = VHDLTestbenchGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()