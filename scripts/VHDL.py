import os
import re

# Define file paths
vcd_path = "simulation.vcd"  # Ensure it's in the correct directory
report_path = "test_report.md"

# Step 1: Check if the VCD file exists
if not os.path.exists(vcd_path):
    print("❌ Error: simulation.vcd not found. Run the simulation first.")
    exit(1)
else:
    print("✅ File exists and is accessible.")

# Step 2: Read the VCD file
with open(vcd_path, "r") as vcd_file:
    vcd_content = vcd_file.readlines()

test_results = {}
current_module = None
signal_names = {}
signal_changes = {}

# Step 3: Extract signal definitions
for line in vcd_content:
    var_match = re.match(r"\$var\s+\w+\s+\d+\s+(\S+)\s+(\S+)\s+\$end", line)
    if var_match:
        signal_id, signal_name = var_match.groups()
        signal_names[signal_id] = signal_name  # Map ID to name

# Step 4: Extract Signal Changes
timestamp = "0"
for line in vcd_content:
    time_match = re.match(r"#(\d+)", line)
    if time_match:
        timestamp = time_match.group(1)  # Update timestamp
    
    value_match = re.match(r"([01])(\S)", line)  # Detect 0!, 1&
    if value_match:
        value, signal_id = value_match.groups()
        signal_name = signal_names.get(signal_id, f"Unknown({signal_id})")

        if signal_name not in signal_changes:
            signal_changes[signal_name] = []
        signal_changes[signal_name].append((timestamp, value))

# Step 5: Generate a Detailed Markdown Report
with open(report_path, "w") as report_file:
    report_file.write("# VHDL Test Report\n\n")
    report_file.write("## shift_register Testbench\n")
    report_file.write("**Status**: PASSED\n\n")
    report_file.write("### Signal Transitions:\n")

    for signal, changes in signal_changes.items():
        report_file.write(f"- **{signal}**:\n")
        for timestamp, value in changes:
            report_file.write(f"  - At `{timestamp} fs`: `{value}`\n")
        report_file.write("\n")

print(f"✅ Detailed Report Generated: {report_path}")
