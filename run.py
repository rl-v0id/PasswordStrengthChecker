
import os
import sys
import subprocess
import platform
from pathlib import Path
import getpass
import secrets
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Enable Unicode support on Windows
if os.name == 'nt':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# ANSI color codes for terminal output
RESET = '\033[0m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_python_command():
    commands = ['python3', 'python', 'py']
    for cmd in commands:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True, check=True)
            if 'Python 3.' in result.stdout or 'Python 3.' in result.stderr:
                return cmd
        except Exception:
            continue
    raise RuntimeError("Python 3.7+ not found. Please install Python and try again.")

def show_progress_checklist():
    """Display the setup progress checklist"""
    print(f"\n{CYAN}📋 Setup Progress Checklist:{RESET}")
    print("=" * 40)
    return {
        'python': False,
        'venv': False,
        'dependencies': False,
        'ready': False
    }

def safe_print(text):
    """Print text with fallback for unicode issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback for Windows console issues
        safe_text = text.encode('ascii', errors='replace').decode('ascii')
        print(safe_text)

# --- Master Password Management Functions ---
def get_master_password_file():
    """Get the path to the master password file"""
    user_data_dir = os.path.join(os.path.dirname(__file__), "user_data")
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
    return os.path.join(user_data_dir, "master_password.hash")

def get_salt_file():
    """Get the path to the salt file"""
    user_data_dir = os.path.join(os.path.dirname(__file__), "user_data")
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
    return os.path.join(user_data_dir, "salt.bin")

def create_master_password():
    """Create a new master password"""
    print(f"\n{CYAN}🔑 CREATE MASTER PASSWORD{RESET}")
    print("=" * 50)
    print("Your master password protects your password history.")
    print("Choose a strong password you can remember!")
    print()
    
    while True:
        password = getpass.getpass("Enter master password: ")
        if len(password) < 8:
            print(f"{RED}❌ Password must be at least 8 characters long.{RESET}")
            continue
        
        confirm = getpass.getpass("Confirm master password: ")
        if password != confirm:
            print(f"{RED}❌ Passwords do not match. Please try again.{RESET}")
            continue
        
        # Generate a random salt
        salt = secrets.token_bytes(32)
        
        # Create hash using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        password_hash = kdf.derive(password.encode())
        
        # Save salt and hash
        try:
            with open(get_salt_file(), "wb") as f:
                f.write(salt)
            with open(get_master_password_file(), "wb") as f:
                f.write(password_hash)
            
            print(f"\n{GREEN}✨ Master password created successfully!{RESET}")
            return True
        except Exception as e:
            print(f"{RED}❌ Error creating master password: {e}{RESET}")
            return False

def verify_master_password():
    """Verify the master password"""
    if not os.path.exists(get_master_password_file()) or not os.path.exists(get_salt_file()):
        return False
    
    print(f"\n{CYAN}🔐 MASTER PASSWORD VERIFICATION{RESET}")
    print("=" * 50)
    
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        password = getpass.getpass("Enter master password: ")
        
        try:
            with open(get_salt_file(), "rb") as f:
                salt = f.read()
            with open(get_master_password_file(), "rb") as f:
                stored_hash = f.read()
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            password_hash = kdf.derive(password.encode())
            
            if password_hash == stored_hash:
                print(f"{GREEN}✅ Master password verified!{RESET}")
                # Store in environment for Streamlit session
                os.environ['MASTER_PASSWORD'] = password
                return True
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"{RED}❌ Incorrect password. {remaining} attempts remaining.{RESET}")
                else:
                    print(f"{RED}❌ Too many failed attempts. Access denied.{RESET}")
                    
        except Exception as e:
            print(f"{RED}❌ Error verifying password: {e}{RESET}")
            return False
    
    return False

def change_master_password():
    """Change the existing master password"""
    print(f"\n{CYAN}🔄 CHANGE MASTER PASSWORD{RESET}")
    print("=" * 50)
    
    # First verify current password
    if not verify_master_password():
        print(f"{RED}❌ Cannot change password without verifying current one.{RESET}")
        return False
    
    print(f"\n{YELLOW}Now enter your new master password:{RESET}")
    return create_master_password()

def master_password_menu():
    """Handle master password management menu"""
    while True:
        clear_screen()
        print(f"\n{CYAN}🔑 MASTER PASSWORD MANAGEMENT{RESET}")
        print("=" * 50)
        
        if os.path.exists(get_master_password_file()):
            print(f"{GREEN}📋 Master password is configured{RESET}")
            print(f"\n{CYAN}[1]{RESET} 🔄 Change master password")
            print(f"{RED}[2]{RESET} 🗑️ Delete master password (WARNING: Will lose all history!)")
            print(f"{YELLOW}[3]{RESET} 🔙 Back to main menu")
        else:
            print(f"{YELLOW}📋 No master password configured{RESET}")
            print(f"\n{GREEN}[1]{RESET} 🔑 Create master password")
            print(f"{YELLOW}[2]{RESET} 🔙 Back to main menu")
        
        print(f"\n{YELLOW}💡 Press Ctrl+C to exit at any time.{RESET}")
        
        try:
            if os.path.exists(get_master_password_file()):
                choice = input(f"\n{BLUE}Enter your choice (1-3): {RESET}").strip()
                max_choice = 3
            else:
                choice = input(f"\n{BLUE}Enter your choice (1-2): {RESET}").strip()
                max_choice = 2
            
            if choice == '1':
                if os.path.exists(get_master_password_file()):
                    # Change existing password
                    if change_master_password():
                        input(f"{GREEN}Press Enter to continue...{RESET}")
                else:
                    # Create new password
                    if create_master_password():
                        input(f"{GREEN}Press Enter to continue...{RESET}")
            
            elif choice == '2':
                if os.path.exists(get_master_password_file()):
                    # Delete master password
                    print(f"\n{RED}⚠️  WARNING: This will delete your master password and ALL encrypted history!{RESET}")
                    confirm = input("Type 'DELETE' to confirm: ").strip()
                    if confirm == 'DELETE':
                        try:
                            if os.path.exists(get_master_password_file()):
                                os.remove(get_master_password_file())
                            if os.path.exists(get_salt_file()):
                                os.remove(get_salt_file())
                            # Also remove history files
                            user_data_dir = os.path.join(os.path.dirname(__file__), "user_data")
                            history_file = os.path.join(user_data_dir, "password_history.enc")
                            key_file = os.path.join(user_data_dir, "encryption.key")
                            if os.path.exists(history_file):
                                os.remove(history_file)
                            if os.path.exists(key_file):
                                os.remove(key_file)
                            print(f"\n{GREEN}✅ Master password and history deleted successfully.{RESET}")
                        except Exception as e:
                            print(f"{RED}❌ Error deleting files: {e}{RESET}")
                        input(f"{YELLOW}Press Enter to continue...{RESET}")
                    else:
                        print(f"{YELLOW}❌ Deletion cancelled.{RESET}")
                        input(f"{YELLOW}Press Enter to continue...{RESET}")
                else:
                    # Back to main menu
                    break
            
            elif choice == '3' and max_choice == 3:
                # Back to main menu
                break
            
            else:
                print(f"\n{RED}❌ Invalid choice. Please enter 1-{max_choice}.{RESET}")
                input(f"{MAGENTA}Press Enter to continue...{RESET}")
                
        except KeyboardInterrupt:
            print(f"\n{YELLOW}👋 Returning to main menu...{RESET}")
            break

def update_checklist_item(progress, item, status=True, message=""):
    """Update and display a checklist item"""
    progress[item] = status
    checkbox = "[OK]" if status else "[  ]"  # ASCII fallback for Windows compatibility
    if message:
        safe_print(f"{checkbox} {message}")
    return progress

def setup_environment():
    progress = show_progress_checklist()
    
    # Step 1: Check Python
    print(f"{YELLOW}⏳ Checking Python installation...{RESET}")
    try:
        python_cmd = get_python_command()
        progress = update_checklist_item(progress, 'python', True, f"Python detected: {python_cmd}")
    except RuntimeError as e:
        progress = update_checklist_item(progress, 'python', False, "❌ Python 3.7+ not found")
        raise e
    
    # Step 2: Setup Virtual Environment
    print(f"\n{YELLOW}⏳ Setting up virtual environment...{RESET}")
    venv_path = Path('venv')
    if not venv_path.exists():
        subprocess.run([python_cmd, '-m', 'venv', 'venv'], check=True)
        progress = update_checklist_item(progress, 'venv', True, "Virtual environment created")
    else:
        progress = update_checklist_item(progress, 'venv', True, "Virtual environment already exists")
    
    # Get Python executable paths
    system = platform.system().lower()
    if system == 'windows':
        python_exe = venv_path / 'Scripts' / 'python.exe'
        pip_exe = venv_path / 'Scripts' / 'pip.exe'
    else:
        python_exe = venv_path / 'bin' / 'python'
        pip_exe = venv_path / 'bin' / 'pip'
    
    # Step 3: Install Dependencies
    print(f"\n{YELLOW}⏳ Installing dependencies...{RESET}")
    if Path('requirements.txt').exists():
        try:
            # Upgrade pip silently
            subprocess.run([str(python_exe), '-m', 'pip', 'install', '--upgrade', 'pip'], 
                          capture_output=True, check=True)
            
            # Install requirements
            result = subprocess.run([str(pip_exe), 'install', '-r', 'requirements.txt'], 
                                  capture_output=True, text=True, check=True)
            progress = update_checklist_item(progress, 'dependencies', True, "All dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            progress = update_checklist_item(progress, 'dependencies', False, f"❌ Failed to install dependencies: {e}")
            raise e
    else:
        progress = update_checklist_item(progress, 'dependencies', False, "❌ requirements.txt not found")
    
    # Step 4: Ready to run
    progress = update_checklist_item(progress, 'ready', True, "Environment setup complete! 🎉")
    
    # Show final status
    print(f"\n{GREEN}{'='*40}")
    print(f"🎯 SETUP COMPLETE - ALL SYSTEMS READY!")
    print(f"{'='*40}{RESET}")
    
    return python_exe

def update_from_git():
    print(f"\n{BLUE}🔄 UPDATING FROM GITHUB{RESET}")
    print("=" * 30)
    
    print(f"{YELLOW}⏳ Checking for updates...{RESET}")
    try:
        # Check current branch
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True, check=True)
        branch = result.stdout.strip()
        print(f"   📂 Current branch: {CYAN}{branch}{RESET}")
        
        # Pull updates
        print(f"{YELLOW}⏳ Downloading latest changes...{RESET}")
        result = subprocess.run(['git', 'pull'], 
                              capture_output=True, text=True, check=True)
        
        if "Already up to date" in result.stdout:
            print(f"{GREEN}✅ Tool is already up to date!{RESET}")
        else:
            print(f"{GREEN}✅ Successfully updated the tool!{RESET}")
            print(f"   📥 Changes downloaded and applied")
            
    except subprocess.CalledProcessError as e:
        print(f"{RED}❌ Failed to update from GitHub{RESET}")
        print(f"   🔍 Please check your internet connection or repository setup")
        if e.stderr:
            print(f"   📝 Error details: {e.stderr.strip()}")
    
    print(f"\n{MAGENTA}Press Enter to return to menu...{RESET}", end="")
    input()

def run_app():
    python_exe = setup_environment()
    
    # Check if master password exists and verify it
    if not os.path.exists(get_master_password_file()):
        print(f"\n{YELLOW}📝 No master password found. Let's create one first!{RESET}")
        if not create_master_password():
            print(f"{RED}❌ Cannot start application without master password.{RESET}")
            input(f"{MAGENTA}Press Enter to return to menu...{RESET}")
            return
    else:
        if not verify_master_password():
            print(f"{RED}❌ Cannot start application without valid master password.{RESET}")
            input(f"{MAGENTA}Press Enter to return to menu...{RESET}")
            return
    
    # Clear status display
    print(f"\n{BLUE}🚀 LAUNCHING PASSWORD STRENGTH CHECKER{RESET}")
    print("=" * 50)
    
    # Server information
    print(f"{CYAN}📡 Server Details:{RESET}")
    print(f"   🖥️  Host: localhost")
    print(f"   🔢 Port: 8501")
    print(f"   🌐 URL: {GREEN}http://localhost:8501{RESET}")
    
    print(f"\n{YELLOW}⏳ Starting Streamlit server...{RESET}")
    print(f"{MAGENTA}💡 The app will automatically open in your default browser{RESET}")
    print(f"{RED}⏹️  Press Ctrl+C to stop the server{RESET}")
    
    print("\n" + "="*50)
    print(f"{GREEN}🎯 SERVER IS RUNNING - ACCESS YOUR APP AT:{RESET}")
    print(f"{CYAN}🔗 http://localhost:8501{RESET}")
    print("="*50 + "\n")
    
    try:
        # Create environment copy with master password
        env = os.environ.copy()
        subprocess.run([
            str(python_exe), '-m', 'streamlit', 'run', 'app.py',
            '--server.address', 'localhost',
            '--server.port', '8501'
        ], check=True, env=env)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}👋 Shutting down Password Strength Checker...{RESET}")
        print(f"{GREEN}✅ Server stopped successfully. Thank you for using our tool!{RESET}")
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}")
        sys.exit(1)

def print_ascii_title():
    ascii_art = f"""
{CYAN}
██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 

{YELLOW}███████╗████████╗██████╗ ███████╗███╗   ██╗ ██████╗ ████████╗██╗  ██╗
██╔════╝╚══██╔══╝██╔══██╗██╔════╝████╗  ██║██╔════╝ ╚══██╔══╝██║  ██║
███████╗   ██║   ██████╔╝█████╗  ██╔██╗ ██║██║  ███╗   ██║   ███████║
╚════██║   ██║   ██╔══██╗██╔══╝  ██║╚██╗██║██║   ██║   ██║   ██╔══██║
███████║   ██║   ██║  ██║███████╗██║ ╚████║╚██████╔╝   ██║   ██║  ██║
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝

{GREEN} ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
 ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{RESET}

{MAGENTA}    A cross platform password strength checker built by RL{RESET}
{"="*67}
"""
    print(ascii_art)

def main_menu():
    while True:
        clear_screen()
        print_ascii_title()
        
        print(f"{CYAN}🎯 MAIN MENU{RESET}")
        print("=" * 30)
        print(f"{CYAN}[1]{RESET} 🔄 Update tool from GitHub")
        print(f"{GREEN}[2]{RESET} 🚀 Use the tool")
        print(f"{YELLOW}[3]{RESET} 🔑 Master password settings")
        print(f"{RED}[4]{RESET} ❌ Exit")
        
        # Show master password status
        if os.path.exists(get_master_password_file()):
            print(f"\n{GREEN}🔐 Master password: Configured{RESET}")
        else:
            print(f"\n{YELLOW}🔐 Master password: Not configured{RESET}")
        
        print(f"\n{YELLOW}💡 Press Ctrl+C to exit at any time.{RESET}")
        choice = input(f"\n{BLUE}Enter your choice (1-4): {RESET}").strip()
        
        if choice == '1':
            update_from_git()
        elif choice == '2':
            run_app()
            break
        elif choice == '3':
            master_password_menu()
        elif choice == '4':
            print(f"\n{YELLOW}👋 Exiting Password Strength Checker. Goodbye!{RESET}")
            break
        else:
            print(f"\n{RED}❌ Invalid choice. Please enter 1-4.{RESET}")
            input(f"{MAGENTA}Press Enter to continue...{RESET}")

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}👋 Exiting Password Strength Checker. Goodbye!{RESET}")
    except Exception as e:
        print(f"{RED}❌ Unexpected error: {e}{RESET}")
        sys.exit(1)