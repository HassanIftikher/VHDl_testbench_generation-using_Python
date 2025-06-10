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
class Signal:
    name: str
    data_type: str
    width: Optional[str] = None
    default_value: Optional[str] = None

    def to_dict(self):
        return {
            "name": self.name,
            "data_type": self.data_type,
            "width": self.width,
            "default_value": self.default_value
        }

@dataclass
class Process:
    name: Optional[str]
    sensitivity_list: List[str]
    code: str

    def to_dict(self):
        return {
            "name": self.name,
            "sensitivity_list": self.sensitivity_list,
            "code": self.code
        }

@dataclass
class Architecture:
    name: str
    entity_name: str
    signals: List[Signal]
    processes: List[Process]
    concurrent_statements: List[str]

    def to_dict(self):
        return {
            "name": self.name,
            "entity_name": self.entity_name,
            "signals": [s.to_dict() for s in self.signals],
            "processes": [p.to_dict() for p in self.processes],
            "concurrent_statements": self.concurrent_statements
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
        self.content = content
        self.clean_content = self._preprocess_vhdl(content)
        self.entity: Optional[Entity] = None
        self.architecture: Optional[Architecture] = None

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

    def _parse_signals(self, arch_body: str) -> List[Signal]:
        signals = []
        # Extract signal declarations
        signal_pattern = r'signal\s+(.*?)\s*:\s*(.*?)\s*(?:;\s*|$)'
        signal_matches = re.finditer(signal_pattern, arch_body, re.IGNORECASE)
        
        for match in signal_matches:
            signal_names = match.group(1).split(',')
            signal_type = match.group(2).strip()
            
            # Check for vector types
            vector_match = re.match(
                r'(std_logic_vector|bit_vector|signed|unsigned)\s*\((.*?)\)', 
                signal_type, 
                re.IGNORECASE
            )
            
            # Check for default value
            default_value = None
            if ':=' in signal_type:
                signal_type, default_value = signal_type.split(':=', 1)
                signal_type = signal_type.strip()
                default_value = default_value.strip()
            
            if vector_match:
                data_type = vector_match.group(1).lower()
                width = vector_match.group(2).strip()
                
                for name in signal_names:
                    if name.strip():
                        signals.append(Signal(
                            name=name.strip(),
                            data_type=data_type,
                            width=width,
                            default_value=default_value
                        ))
            else:
                data_type = signal_type.lower()
                for name in signal_names:
                    if name.strip():
                        signals.append(Signal(
                            name=name.strip(),
                            data_type=data_type,
                            width=None,
                            default_value=default_value
                        ))
        
        return signals

    def _parse_processes(self, arch_body: str) -> List[Process]:
        processes = []
        
        # Extract processes
        process_pattern = r'(?:(\w+)\s*:\s*)?process\s*\((.*?)\)(.*?)end\s+process\s*(?:\1)?\s*;'
        process_matches = re.finditer(process_pattern, arch_body, re.IGNORECASE | re.DOTALL)
        
        for match in process_matches:
            process_name = match.group(1) if match.group(1) else None
            sensitivity_list = [s.strip() for s in match.group(2).split(',') if s.strip()]
            process_body = match.group(3).strip()
            
            processes.append(Process(
                name=process_name,
                sensitivity_list=sensitivity_list,
                code=process_body
            ))
        
        return processes

    def _parse_concurrent_statements(self, arch_body: str) -> List[str]:
        # This is a simplified approach - would need more complex parsing for full accuracy
        statements = []
        
        # Remove signal declarations
        cleaned_body = re.sub(r'signal\s+.*?;', '', arch_body, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove process blocks
        cleaned_body = re.sub(r'(?:\w+\s*:\s*)?process\s*\(.*?\).*?end\s+process\s*(?:\w+)?\s*;', '', cleaned_body, flags=re.IGNORECASE | re.DOTALL)
        
        # Split remaining statements
        stmt_pattern = r'(.*?);'
        stmt_matches = re.finditer(stmt_pattern, cleaned_body)
        
        for match in stmt_matches:
            stmt = match.group(1).strip()
            if stmt and not stmt.lower().startswith(('begin', 'end')):
                statements.append(stmt)
        
        return statements

    def parse(self) -> Dict:
        # Parse entity
        entity_pattern = r'entity\s+(\w+)\s+is(.*?)end\s+(?:entity\s+)?\1\s*;'
        entity_match = re.search(entity_pattern, self.clean_content, re.IGNORECASE | re.DOTALL)

        if not entity_match:
            raise ValueError("No valid entity found in VHDL file")

        entity_name = entity_match.group(1)
        entity_body = entity_match.group(2)

        generics = self._parse_generics(entity_body)
        ports = self._parse_ports(entity_body)

        self.entity = Entity(name=entity_name, ports=ports, generics=generics)
        
        # Parse architecture
        arch_pattern = r'architecture\s+(\w+)\s+of\s+(\w+)\s+is(.*?)begin(.*?)end\s+(?:architecture\s+)?\1\s*;'
        arch_match = re.search(arch_pattern, self.clean_content, re.IGNORECASE | re.DOTALL)
        
        if arch_match:
            arch_name = arch_match.group(1)
            arch_entity = arch_match.group(2)
            arch_declaration = arch_match.group(3)
            arch_body = arch_match.group(4)
            
            signals = self._parse_signals(arch_declaration)
            processes = self._parse_processes(arch_body)
            concurrent_statements = self._parse_concurrent_statements(arch_body)
            
            self.architecture = Architecture(
                name=arch_name,
                entity_name=arch_entity,
                signals=signals,
                processes=processes,
                concurrent_statements=concurrent_statements
            )
            
            return {"entity": self.entity, "architecture": self.architecture}
        
        return {"entity": self.entity}

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
                "parser_version": "1.1"
            }
        }
        
        if self.architecture:
            json_data["vhdl_architecture"] = self.architecture.to_dict()

        with open(output_path, 'w') as f:
            json.dump(json_data, f, indent=2)

def parse_vhdl_file(input_file: str, output_file: str = None) -> Dict:
    with open(input_file, 'r') as f:
        vhdl_content = f.read()

    parser = VHDLParser(vhdl_content)
    parse_result = parser.parse()

    if not output_file:
        output_file = 'src/vhdl_module.json'

    parser.save_to_json(output_file)
    
    # Return the entity dict to maintain backward compatibility
    return parse_result.get("entity").to_dict() if isinstance(parse_result.get("entity"), Entity) else parse_result.get("entity")

parse_vhdl = parse_vhdl_file