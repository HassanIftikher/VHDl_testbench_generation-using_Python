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
class Port:
    name: str
    direction: str
    data_type: str
    width: Optional[str] = None
    default_value: Optional[str] = None
    range: Optional[str] = None

    def to_dict(self):
        return {
            "name": self.name,
            "direction": self.direction,
            "data_type": self.data_type,
            "width": self.width,
            "default_value": self.default_value,
            "range": self.range
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
        content = re.sub(r'--.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = ' '.join(content.split())
        return content

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
                    name_type, default = decl.split(':=', 1)
                    default = default.strip()
                else:
                    name_type = decl
                    default = None

                name_part, type_part = name_type.split(':', 1)
                names = [n.strip() for n in name_part.split(',')]
                data_type = type_part.strip()

                for name in names:
                    if name:
                        generics.append(Generic(name=name, data_type=data_type, default_value=default))
            except Exception as e:
                print(f"Error parsing generic: {decl}, Error: {str(e)}")
                continue

        return generics

    def _parse_ports(self, entity_text: str) -> List[Port]:
        ports = []
        port_match = re.search(r'port\s*\((.*)\)\s*;', entity_text, re.IGNORECASE | re.DOTALL)

        if not port_match:
            return ports

        port_text = port_match.group(1)
        port_declarations = [decl.strip() for decl in port_text.split(';') if decl.strip()]

        for decl in port_declarations:
            try:
                name_part, type_part = decl.split(':', 1)
                names = [n.strip() for n in name_part.split(',')]
                
                type_parts = type_part.strip().split(maxsplit=1)
                direction = type_parts[0].lower()
                data_type_full = type_parts[1] if len(type_parts) > 1 else ""

                vector_match = re.match(
                    r'(std_logic_vector|bit_vector|signed|unsigned)\s*\((.*?)\)', 
                    data_type_full, 
                    re.IGNORECASE
                )
                
                if vector_match:
                    data_type = vector_match.group(1).lower()
                    range_expr = vector_match.group(2).strip()
                    
                    for name in names:
                        if name:
                            ports.append(Port(
                                name=name,
                                direction=direction,
                                data_type=data_type,
                                width=range_expr,
                                default_value=None,
                                range=None
                            ))
                else:
                    data_type = data_type_full.lower()
                    for name in names:
                        if name:
                            ports.append(Port(
                                name=name,
                                direction=direction,
                                data_type=data_type,
                                width=None,
                                default_value=None,
                                range=None
                            ))

            except Exception as e:
                print(f"Error parsing port: {decl}, Error: {str(e)}")
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
        if not self.entity:
            raise ValueError("No entity has been parsed yet. Call parse() first.")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        entity_dict = self.entity.to_dict()

        json_data = {
            "vhdl_entity": entity_dict,
            "metadata": {
                "supported_types": [t.value for t in VHDLType],
                "parser_version": "1.0"
            }
        }

        with open(output_path, 'w') as f:
            json.dump(json_data, f, indent=2)

def parse_vhdl_file(input_file: str, output_file: str = None) -> Dict:
    with open(input_file, 'r') as f:
        vhdl_content = f.read()

    parser = VHDLParser(vhdl_content)
    entity = parser.parse()

    if not output_file:
        output_file = 'src/vhdl_module.json'

    parser.save_to_json(output_file)
    return entity.to_dict()

parse_vhdl = parse_vhdl_file
