# PYtoEXE Compiler 🚀

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyInstaller](https://img.shields.io/badge/PyInstaller-5.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20MacOS-lightgrey.svg)
![Auto-Dependencies](https://img.shields.io/badge/Dependencies-Auto--install-brightgreen.svg)

A professional Python application that automatically compiles Python scripts to executable files (.exe). **Requires only Python 3.8+** - all other dependencies install automatically!

## ✨ Features

- **🔍 Smart Auto-Detection** - Automatically finds `main.py` (primary) or any Python file
- **📦 Automatic Dependency Installation** - Installs PyInstaller and project dependencies from requirements.txt
- **🔗 Requirements.txt Support** - Automatically parses and installs project dependencies
- **🖥️ Multiple Interfaces** - Command-line and auto-compilation modes
- **⚡ Zero Setup Required** - Works with just Python installed
- **📊 Dependency Analysis** - AST-based import detection and hidden imports
- **📁 Clean Output** - Automatic cleanup of temporary files

## 🚀 Zero-Setup Installation

### All You Need:
- **Python 3.8 or higher** (that's it!)

### Quick Start:
```bash
# Clone the repository
git clone https://github.com/MaxKashpersky/PYtoEXE.git
cd PYtoEXE
```

# Run immediately - no pip install required!
```
python compiler.py
```

The program will:

✅ Auto-install PyInstaller if missing

✅ Auto-detect main.py or any Python file

✅ Parse requirements.txt and install dependencies

✅ Compile to EXE with all dependencies included

💻 Usage
Mode 1: Auto-Compilation (Recommended)
Simply run the script without arguments:

```bash
python compiler.py
```

The program will automatically:

Install PyInstaller if needed

Find main.py (primary) or any Python file

Parse requirements.txt and install dependencies

Show dependency analysis

Compile to EXE in the same directory

Mode 2: Command Line
Compile a specific file:

```bash
python compiler.py path/to/your_script.py
```

With custom output directory:

```bash
python compiler.py path/to/your_script.py path/to/output/directory
```

`🏗️ Project Structure Example
```text
your-project/
├── main.py              # Primary entry point (auto-detected)
├── utils.py             # Local module (auto-included)
├── config.py            # Local module (auto-included)
├── requirements.txt     # Dependencies (auto-installed)
└── data/
    └── config.json      # Data files
    
```

Example: main.py

```
def main():
    print("Hello from compiled EXE!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
```    
Example: requirements.txt
```txt
requests>=2.28.0
pygame==2.5.0
numpy
pandas
```

🔧 How It Works
Automatic Dependency Installation:
Compiler Dependencies - PyInstaller installed automatically

Project Dependencies - Packages from requirements.txt installed automatically

Import Analysis - AST parsing detects all required modules

Hidden Imports - Auto-configured for PyInstaller

Dependency Detection:
✅ requirements.txt parsing with version support

✅ AST-based import analysis for hidden imports

✅ Standard library filtering to avoid unnecessary installs

✅ Interactive confirmation before installation

🛠️ Technical Details
Primary Entry Point: main.py is prioritized in auto-detection

Compiler Engine: PyInstaller 5.0+ with hidden imports support

Dependency Management: Automatic pip installation

Import Analysis: AST-based parsing for automatic dependency detection

Supported Platforms: Windows, Linux, macOS

Python Version: 3.8+

📋 Compilation Process
```text
1. Check PyInstaller → Auto-install if missing
2. Find main.py → Fallback to any .py file
3. Parse requirements.txt → Auto-install dependencies
4. Analyze imports → Configure hidden imports
5. Compile with PyInstaller → Generate EXE
6. Cleanup → Remove temporary files
```

🤝 Contributing
Fork the repository

Create a feature branch:

```bash
git checkout -b feature/YourFeature
```

Commit your changes:

```bash
git commit -m 'Add YourFeature'
```

Push to the branch:

```bash
git push origin feature/YourFeature
```

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Author
Max Kashpersky

GitHub: @MaxKashpersky

Email: 220718354+MaxKashpersky@users.noreply.github.com

🐛 Bug Reports & Support
If you encounter any issues:

Check existing Issues

Create a New Issue

❓ Frequently Asked Questions
Q: What do I need to run this?
A: Just Python 3.8+ - everything else installs automatically!

Q: How are dependencies handled?
A: The program automatically installs PyInstaller and any packages from requirements.txt

Q: Can I use it without requirements.txt?
A: Yes! It will still work and only install PyInstaller

Q: What if I have network restrictions?
A: You'll need to install PyInstaller manually first: pip install pyinstaller

⭐ If you find this project useful, please give it a star on GitHub!