"""
Auto PYtoEXE Compiler
Enhanced version with automatic dependency installation from requirements.txt
"""

import os
import sys
import subprocess
import shutil
import ast
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path


class DependencyManager:
    """Handles automatic installation of required dependencies from requirements.txt"""

    REQUIRED_PACKAGES = ['pyinstaller']  # Base requirement for the compiler itself

    @staticmethod
    def check_package_installed(package_name):
        """
        Check if a Python package is installed

        Args:
            package_name (str): Name of the package to check

        Returns:
            bool: True if package is installed, False otherwise
        """
        try:
            # Handle packages with different import names (e.g., PyQt5 vs pyqt5)
            import_name = package_name.lower().replace('-', '_')
            __import__(import_name)
            return True
        except ImportError:
            return False

    @staticmethod
    def install_package(package_name):
        """
        Install a Python package using pip

        Args:
            package_name (str): Name of the package to install

        Returns:
            bool: True if installation successful, False otherwise
        """
        try:
            print(f"📦 Installing {package_name}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✅ {package_name} installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package_name}: {e}")
            return False
        except Exception as e:
            print(f"❌ Error installing {package_name}: {e}")
            return False

    @staticmethod
    def parse_requirements_file(requirements_path):
        """
        Parse requirements.txt file and extract package names

        Args:
            requirements_path (str): Path to requirements.txt file

        Returns:
            list: List of package names
        """
        packages = []
        try:
            if os.path.exists(requirements_path):
                with open(requirements_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if not line or line.startswith('#') or line.startswith('-'):
                            continue
                        # Extract package name (remove version specifiers)
                        package_name = line.split('>=')[0].split('==')[0].split('<=')[0].strip()
                        if package_name:
                            packages.append(package_name)
                print(f"📋 Found {len(packages)} packages in requirements.txt")
            else:
                print("📋 No requirements.txt file found")
        except Exception as e:
            print(f"❌ Error reading requirements.txt: {e}")

        return packages

    @staticmethod
    def find_requirements_file(script_path):
        """
        Find requirements.txt in the same directory as the script

        Args:
            script_path (str): Path to the main Python script

        Returns:
            str or None: Path to requirements.txt if found
        """
        script_dir = os.path.dirname(script_path)
        requirements_path = os.path.join(script_dir, "requirements.txt")
        return requirements_path if os.path.exists(requirements_path) else None

    @staticmethod
    def ensure_compiler_dependencies():
        """
        Ensure compiler dependencies are installed (PyInstaller)

        Returns:
            bool: True if all dependencies are available, False otherwise
        """
        missing_packages = []

        for package in DependencyManager.REQUIRED_PACKAGES:
            if not DependencyManager.check_package_installed(package):
                missing_packages.append(package)

        if not missing_packages:
            return True

        print("=" * 50)
        print("COMPILER DEPENDENCIES REQUIRED")
        print("=" * 50)
        print(f"Required for compilation: {', '.join(missing_packages)}")
        print("This program will automatically install them.")

        # Install missing packages
        for package in missing_packages:
            if not DependencyManager.install_package(package):
                print("❌ Compiler setup failed. Please install PyInstaller manually:")
                print("   pip install pyinstaller")
                return False

        return True

    @staticmethod
    def ensure_project_dependencies(script_path):
        """
        Ensure project dependencies from requirements.txt are installed
        """
        requirements_path = DependencyManager.find_requirements_file(script_path)
        if not requirements_path:
            print("📋 No requirements.txt found - skipping project dependencies")
            return True

        required_packages = DependencyManager.parse_requirements_file(requirements_path)
        if not required_packages:
            return True

        # ФИКС: Исключи PyInstaller из установки проектных зависимостей
        required_packages = [pkg for pkg in required_packages if pkg.lower() != 'pyinstaller']

        if not required_packages:
            print("✅ Only PyInstaller in requirements - already handled")
            return True
        requirements_path = DependencyManager.find_requirements_file(script_path)
        if not requirements_path:
            print("📋 No requirements.txt found - skipping project dependencies")
            return True

        required_packages = DependencyManager.parse_requirements_file(requirements_path)
        if not required_packages:
            return True

        missing_packages = []
        for package in required_packages:
            if not DependencyManager.check_package_installed(package):
                missing_packages.append(package)

        if not missing_packages:
            print("✅ All project dependencies are already installed")
            return True

        print("=" * 50)
        print("PROJECT DEPENDENCIES REQUIRED")
        print("=" * 50)
        print(f"Packages needed: {', '.join(missing_packages)}")
        print("This program will automatically install them.")

        # Ask for user confirmation in interactive mode
        if len(sys.argv) == 1:  # Auto/GUI mode
            try:
                response = input("Install project dependencies? (y/n): ").strip().lower()
                if response not in ['y', 'yes', '']:
                    print("⚠️  Project dependencies not installed - compilation may fail")
                    return False
            except (EOFError, KeyboardInterrupt):
                return False

        # Install missing packages
        success_count = 0
        for package in missing_packages:
            if DependencyManager.install_package(package):
                success_count += 1

        if success_count == len(missing_packages):
            print("✅ All project dependencies installed successfully!")
            return True
        else:
            print(f"⚠️  Only {success_count}/{len(missing_packages)} packages installed successfully")
            print("Compilation may fail due to missing dependencies")
            return True  # Continue anyway, user can install manually later


class ImportAnalyzer:
    """Analyzes Python files to detect all imports and dependencies"""

    @staticmethod
    def extract_imports(file_path):
        """
        Extract all imports from a Python file using AST parsing

        Args:
            file_path (str): Path to Python file

        Returns:
            list: List of imported module names
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            tree = ast.parse(content)
            imports = []

            for node in ast.walk(tree):
                # Handle import x
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                # Handle from x import y
                elif isinstance(node, ast.ImportFrom):
                    if node.module:  # module could be None for relative imports
                        imports.append(node.module)

            return list(set(imports))  # Remove duplicates

        except Exception as e:
            print(f"Warning: Could not parse imports from {file_path}: {e}")
            return []

    @staticmethod
    def find_local_modules(main_script_path):
        """
        Find all local Python modules in the same directory

        Args:
            main_script_path (str): Path to main script

        Returns:
            list: List of local module file paths
        """
        script_dir = os.path.dirname(main_script_path)
        local_modules = []

        for file in os.listdir(script_dir):
            if (file.endswith('.py') and
                file != os.path.basename(main_script_path) and
                not file.startswith('compiler')):
                local_modules.append(os.path.join(script_dir, file))

        return local_modules

    @staticmethod
    def analyze_dependencies(main_script_path):
        """
        Analyze all dependencies including imports from local modules

        Args:
            main_script_path (str): Path to main script

        Returns:
            dict: Analysis results with imports and modules
        """
        # Get imports from main script
        main_imports = ImportAnalyzer.extract_imports(main_script_path)

        # Find local modules
        local_modules = ImportAnalyzer.find_local_modules(main_script_path)

        # Get imports from all local modules
        all_imports = set(main_imports)
        for module_path in local_modules:
            module_imports = ImportAnalyzer.extract_imports(module_path)
            all_imports.update(module_imports)

        # Filter out standard library imports (basic filtering)
        stdlib_modules = {
            'os', 'sys', 'math', 'json', 'datetime', 'time', 're',
            'random', 'pathlib', 'collections', 'itertools', 'functools'
        }
        external_imports = [imp for imp in all_imports if imp not in stdlib_modules]

        return {
            'main_imports': main_imports,
            'local_modules': local_modules,
            'all_imports': list(all_imports),
            'external_imports': external_imports,
            'local_module_names': [os.path.basename(mod) for mod in local_modules]
        }


class PyToExeCompiler:
    """Enhanced compiler with module import support and dependency management"""

    @staticmethod
    def compile_to_exe(python_script_path, output_dir=None):
        """
        Compile Python script to EXE with module import support

        Args:
            python_script_path (str): Path to Python script
            output_dir (str): Output directory for EXE file

        Returns:
            bool: True if compilation successful, False otherwise
        """
        try:
            if output_dir is None:
                output_dir = os.path.dirname(python_script_path)

            # Step 1: Ensure compiler dependencies are installed
            if not DependencyManager.ensure_compiler_dependencies():
                return False

            # Step 2: Ensure project dependencies are installed
            if not DependencyManager.ensure_project_dependencies(python_script_path):
                return False

            # Step 3: Analyze code dependencies
            print("🔍 Analyzing dependencies...")
            analysis = ImportAnalyzer.analyze_dependencies(python_script_path)

            # Get script name without extension for EXE naming
            script_name = os.path.splitext(os.path.basename(python_script_path))[0]

            # Build PyInstaller command with hidden imports
            cmd = [
                'pyinstaller',
                '--onefile',
                '--console',
                '--distpath', output_dir,
                '--workpath', os.path.join(output_dir, 'build'),
                '--specpath', output_dir,
                '--name', script_name,
                '--clean',
            ]

            # Add hidden imports for external dependencies
            for external_import in analysis['external_imports']:
                cmd.extend(['--hidden-import', external_import])

            # Add local modules to the command (they should be in same directory)
            cmd.append(python_script_path)

            print(f"🚀 Compiling {python_script_path}...")
            print(f"📦 Detected local modules: {analysis['local_module_names']}")
            print(f"🔗 Detected external imports: {analysis['external_imports']}")
            print(f"⚙️  Command: {' '.join(cmd)}")

            # Execute compilation process
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            print("✅ Compilation completed successfully!")

            # Clean up temporary files
            PyToExeCompiler._cleanup_temp_files(output_dir, script_name)

            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Compilation error: {e}")
            print(f"Error output: {e.stderr}")
            return False
        except FileNotFoundError:
            print("❌ Error: PyInstaller not found. Install with: pip install pyinstaller")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False

    @staticmethod
    def _cleanup_temp_files(output_dir, script_name):
        """
        Remove temporary files created during compilation

        Args:
            output_dir (str): Output directory path
            script_name (str): Name of the script
        """
        spec_file = os.path.join(output_dir, f"{script_name}.spec")
        build_dir = os.path.join(output_dir, 'build')

        try:
            if os.path.exists(spec_file):
                os.remove(spec_file)
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
        except Exception as e:
            print(f"⚠️  Warning: Could not clean up temporary files: {e}")


class FileManager:
    """Handles file operations and discovery"""

    @staticmethod
    def find_main_py(directory):
        """
        Search for main.py file in directory (primary entry point)

        Args:
            directory (str): Directory to search in

        Returns:
            str or None: Full path to main.py if found, None otherwise
        """
        main_py_path = os.path.join(directory, "main.py")
        return main_py_path if os.path.exists(main_py_path) else None

    @staticmethod
    def find_any_python_file(directory):
        """
        Find any Python file in directory (excluding current script)

        Args:
            directory (str): Directory to search in

        Returns:
            str or None: Full path to Python file if found, None otherwise
        """
        for file in os.listdir(directory):
            if (file.endswith('.py') and
                file != os.path.basename(__file__) and
                not file.startswith('compiler')):
                return os.path.join(directory, file)
        return None

    @staticmethod
    def select_file_dialog():
        """
        Open file selection dialog for user to choose Python file

        Returns:
            str or None: Selected file path or None if canceled
        """
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Select Python File to Compile",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )

        root.destroy()
        return file_path if file_path else None


class AutoCompiler:
    """Handles automatic compilation workflow"""

    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    def run_auto_mode(self):
        """
        Run automatic compilation mode with user interaction

        Returns:
            bool: True if compilation successful, False otherwise
        """
        print("=" * 50)
        print("Auto Python to EXE Compiler")
        print("Primary entry point: main.py")
        print("=" * 50)

        # Priority 1: Look for main.py (primary entry point)
        main_py = FileManager.find_main_py(self.current_dir)
        if main_py and self._ask_for_compilation(main_py, "main.py (primary entry point)"):
            return PyToExeCompiler.compile_to_exe(main_py, self.current_dir)

        # Priority 2: Try to find any Python file
        any_py_file = FileManager.find_any_python_file(self.current_dir)
        if any_py_file and self._ask_for_compilation(any_py_file, os.path.basename(any_py_file)):
            return PyToExeCompiler.compile_to_exe(any_py_file, self.current_dir)

        # Priority 3: Manual file selection
        return self._manual_file_selection()

    def _ask_for_compilation(self, file_path, file_description):
        """
        Ask user confirmation for file compilation

        Args:
            file_path (str): Path to file proposed for compilation
            file_description (str): Description of the file

        Returns:
            bool: True if user confirms, False otherwise
        """
        print(f"✅ Found {file_description}: {file_path}")

        # Show dependency analysis
        analysis = ImportAnalyzer.analyze_dependencies(file_path)
        if analysis['local_modules']:
            print(f"📦 Detected local modules: {analysis['local_module_names']}")
        if analysis['external_imports']:
            print(f"🔗 Detected external imports: {analysis['external_imports']}")

        # Check for requirements.txt
        requirements_path = DependencyManager.find_requirements_file(file_path)
        if requirements_path:
            packages = DependencyManager.parse_requirements_file(requirements_path)
            if packages:
                print(f"📋 Dependencies from requirements.txt: {', '.join(packages)}")

        choice = input("Compile this file? (y/n): ").strip().lower()
        return choice == 'y'

    def _manual_file_selection(self):
        """
        Handle manual file selection process

        Returns:
            bool: True if compilation successful, False otherwise
        """
        print("❌ No Python files found in current directory.")
        choice = input("Select file manually? (y/n): ").strip().lower()

        if choice == 'y':
            file_path = FileManager.select_file_dialog()
            if file_path:
                return PyToExeCompiler.compile_to_exe(file_path, os.path.dirname(file_path))
            else:
                print("No file selected.")
                return False
        else:
            print("Compilation canceled.")
            return False


# GUI class would be similar but with enhanced dependency messages
# [GUI code remains largely the same as previous version]

def main():
    """
    Main application entry point
    """
    if len(sys.argv) > 1:
        # Command line mode
        script_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        success = PyToExeCompiler.compile_to_exe(script_path, output_dir)
        sys.exit(0 if success else 1)

    elif len(sys.argv) == 1:
        # Auto-compilation mode
        compiler = AutoCompiler()
        if compiler.run_auto_mode():
            print("✅ Compilation completed successfully!")
        else:
            print("❌ Compilation failed")
            sys.exit(1)

    else:
        # GUI mode (simplified for this example)
        print("GUI mode not implemented in this version")
        sys.exit(1)


if __name__ == "__main__":
    main()