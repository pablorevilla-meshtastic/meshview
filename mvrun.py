import argparse
import threading
import subprocess

# Run python in subprocess
def run_script(script_name, *args):
    try:
        # Path to the Python interpreter inside the virtual environment
        python_executable = '.venv/bin/python'

        # Combine the script name and arguments
        command = [python_executable, script_name] + list(args)

        # Run the subprocess and report errors
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"Error running {script_name}: {e}")

# Parse runtime argument (--config) and start subprocess threads
def main():
    parser = argparse.ArgumentParser(description="Helper script to run the datbase and web frontend in separate threads.")

    # Add --config runtime argument
    parser.add_argument('--config', help="Path to the configuration file.", default='config.ini')
    args = parser.parse_args()

    # Database Thread
    dbthrd = threading.Thread(target=run_script, args=('startdb.py', '--config', args.config))

    # Web server thread
    webthrd = threading.Thread(target=run_script, args=('main.py', '--config', args.config))

    # Start Meshview subprocess threads
    dbthrd.start()
    webthrd.start()

    dbthrd.join()
    webthrd.join()

if __name__ == '__main__':
    main()
