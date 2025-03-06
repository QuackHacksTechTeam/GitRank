
LINE_THRESHOLD = 1000 
EXCLUDED_PATHS = [
    "node_modules",  # Node.js dependencies
    "dist",           # Distribution files
    "build",          # Build directory
    "out",            # Output files
    "bin",            # Binary files
    ".git",           # Git internal metadata
    ".github",        # GitHub-specific configuration
    ".vscode",        # VSCode-specific settings
    "__pycache__",
    "bower_components",  # Bower dependencies
    "pip-cache",      # Python pip cache
    "tmp",            # Temporary files
    "temp",           # Temporary files
    "*.log",          # Log files
    "*.bak",          # Backup files
    "*.swp",          # Vim swap files
    "docs",           # Documentation directory
    "README.md",      # Documentation file
    ".idea",          # JetBrains project files
    ".project",       # Eclipse project file
    ".settings",      # Eclipse settings
    ".DS_Store",      # macOS system files
    "Thumbs.db",      # Windows system files
    "*.exe", "*.dll", "*.pdb",  # Executables and binaries
    ".env",           # Environment variables
    "*.sqlite", "*.db"  # Database files
]

def is_excluded_file(file) -> bool: 
    """
    Used to check if a file commitment was likely to come from a 
    source that should not contribute to line count, e.g. pushing node modules 
    """
    if not file.name.endswith(('.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c')):  
        return True

    if file.additions + file.deletions > LINE_THRESHOLD: 
        return True 

    if any(excluded_path in file.filename for excluded_path in EXCLUDED_PATHS):
        return True 

    return False
    
