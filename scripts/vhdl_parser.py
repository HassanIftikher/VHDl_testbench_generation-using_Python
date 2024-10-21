import re
import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Union
from enum import Enum
from pathlib import Path

class VHDLType(Enum):
    STD_LOGIC = "std_logic"
    STD_LOGIC_VECTOR = "std_logic_vector"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    NATURAL = "natural"
    POSITIVE = "positive"
    SIGNED = "signed"
    UNSIGNED = "unsigned"
    REAL = "real"
    BIT = "bit"
    BIT_VECTOR = "bit_vector"
    TIME = "time"
    STRING = "string"

@dataclass
class PortRange:
    left: Union[int, str]
    right: Union[int, str]
    direction: str = "downto"  # or "to"

    def to_dict(self):
        return {
            "left": str(self.left),  # Convert to string to handle both int and str
            "right": str(self.right),
            "direction": self.direction
        }

@dataclass
class Port:
    name: str
    direction: str
    data_type: str
    width: Optional[PortRange] = None
    default_value: Optional[str] = None

    def to_dict(self):
        return {
            "name": self.name,
            "direction": self.direction,
            "data_type": self.data_type,
            "width": self.width.to_dict() if self.width else None,
            "default_value": self.default_value
        }

@dataclass
class Generic:
    name: str
    data_type: str
    default_value: Optional[str] = None

    def to_dict(self):
        return {
            "name": self.name,
            "data_type": self.data_type,
            "default_value": self.default_value
        }

@dataclass
class Entity:
    name: str
    ports: List[Port]
    generics: List[Generic]

    def to_dict(self):
        return {
            "name": self.name,
            "generics": [g.to_dict() for g in self.generics],
            "ports": [p.to_dict() for p in self.ports]
        }

class VHDLParser:
    def __init__(self, content: str):
        self.content = self._preprocess_vhdl(content)
        self.entity: Optional[Entity] = None
        
    def _preprocess_vhdl(self, content: str) -> str:
        # Remove single-line comments
        content = re.sub(r'--.*$', '', content, flags=re.MULTILINE)
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        # Normalize whitespace
        content = ' '.join(content.split())
        return content

    def _parse_range(self, type_str: str) -> Optional[PortRange]:
        range_match = re.search(r'\((.*?)\)', type_str)
        if not range_match:
            return None
            
        range_str = range_match.group(1)
        try:
            if 'downto' in range_str:
                left, right = range_str.split('downto')
                direction = "downto"
            elif 'to' in range_str:
                left, right = range_str.split('to')
                direction = "to"
            else:
                return None
                
            left = left.strip()
            right = right.strip()
            
            # Try to convert to integers if possible
            try:
                left = int(left)
            except ValueError:
                pass
                
            try:
                right = int(right)
            except ValueError:
                pass
                
            return PortRange(left, right, direction)
        except:
            return None

    def _parse_generics(self, entity_text: str) -> List[Generic]:
        generics = []
        generic_match = re.search(r'generic\s*\((.*?)\);', entity_text, re.IGNORECASE | re.DOTALL)
        
        if not generic_match:
            return generics
            
        generic_text = generic_match.group(1)
        generic_declarations = generic_text.split(';')
        
        for decl in generic_declarations:
            decl = decl.strip()
            if not decl:
                continue
                
            try:
                if ':=' in decl:
                    name_type, default = decl.split(':=')
                    default = default.strip()
                else:
                    name_type = decl
                    default = None
                    
                name_part, type_part = name_type.split(':')
                names = [n.strip() for n in name_part.split(',')]
                data_type = type_part.strip()
                
                for name in names:
                    if name:
                        generics.append(Generic(name=name, data_type=data_type, default_value=default))
            except:
                continue
                
        return generics

    def _parse_ports(self, entity_text: str) -> List[Port]:
        ports = []
        port_match = re.search(r'port\s*\((.*?)\);', entity_text, re.IGNORECASE | re.DOTALL)
        
        if not port_match:
            return ports
            
        port_text = port_match.group(1)
        port_declarations = port_text.split(';')
        
        for decl in port_declarations:
            decl = decl.strip()
            if not decl:
                continue
                
            try:
                if ':=' in decl:
                    name_type, default = decl.split(':=')
                    default = default.strip()
                else:
                    name_type = decl
                    default = None
                    
                name_part, type_part = name_type.split(':')
                names = [n.strip() for n in name_part.split(',')]
                
                type_parts = type_part.strip().split()
                direction = type_parts[0].lower()
                data_type = ' '.join(type_parts[1:])
                
                width = self._parse_range(data_type)
                data_type = re.sub(r'\(.*?\)', '', data_type).strip()
                
                for name in names:
                    if name:
                        ports.append(Port(
                            name=name,
                            direction=direction,
                            data_type=data_type,
                            width=width,
                            default_value=default
                        ))
            except:
                continue
                
        return ports

    def parse(self) -> Entity:
        entity_pattern = r'entity\s+(\w+)\s+is(.*?)end\s+(?:entity\s+)?\1\s*;'
        entity_match = re.search(entity_pattern, self.content, re.IGNORECASE | re.DOTALL)
        
        if not entity_match:
            raise ValueError("No valid entity found in VHDL file")
            
        entity_name = entity_match.group(1)
        entity_body = entity_match.group(2)
        
        generics = self._parse_generics(entity_body)
        ports = self._parse_ports(entity_body)
        
        self.entity = Entity(name=entity_name, ports=ports, generics=generics)
        return self.entity

    def save_to_json(self, output_path: str) -> None:
        """Save the parsed entity to a JSON file"""
        if not self.entity:
            raise ValueError("No entity has been parsed yet. Call parse() first.")
            
        output_path = Path(output_path)
        
        # Create directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert entity to dictionary
        entity_dict = self.entity.to_dict()
        
        # Add metadata
        json_data = {
            "vhdl_entity": entity_dict,
            "metadata": {
                "supported_types": [t.value for t in VHDLType],
                "parser_version": "1.0"
            }
        }
        
        # Write to JSON file with proper formatting
        with open(output_path, 'w') as f:
            json.dump(json_data, f, indent=2)

def parse_vhdl_file(input_file: str, output_file: str = None) -> Dict:
    """Convenience function to parse a VHDL file and optionally save to JSON"""
    
    # Read VHDL file
    with open(input_file, 'r') as f:
        vhdl_content = f.read()
    
    # Parse VHDL
    parser = VHDLParser(vhdl_content)
    entity = parser.parse()
    
    # Set the default output file path in the src/ folder if not provided
    if not output_file:
        output_file = 'src/vhdl_module.json'  # Save the JSON file to the 'src/' folder
    
    # Save to JSON if output file is specified
    parser.save_to_json(output_file)
    
    return entity.to_dict()