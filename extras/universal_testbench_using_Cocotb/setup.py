def create_init_file(path):
    """Create an empty __init__.py file"""
    with open(path / '__init__.py', 'w') as f:
        pass

def setup_project():
    # Get project root (where this script is located)
    root = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Create necessary directories
    dirs = ['src', 'tb', 'examples', 'generated']
    for d in dirs:
        (root / d).mkdir(exist_ok=True)
    
    # Create __init__.py files
    create_init_file(root / 'src')
    create_init_file(root / 'tb')
    
    print("Project structure created successfully!")
    print("\nYou can now run:")
    print("python3 main.py examples/counter.vhd")

if __name__ == '__main__':
    setup_project()