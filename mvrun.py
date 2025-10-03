import argparse
import threading
import subprocess
import logging
import os
import signal
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s:%(lineno)d [pid:%(process)d] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Global list to track running processes
running_processes = []
pid_files = []

def cleanup_pid_file(pid_file):
    """Remove a PID file if it exists"""
    if os.path.exists(pid_file):
        try:
            os.remove(pid_file)
            logger.info(f"Removed PID file {pid_file}")
        except Exception as e:
            logger.error(f"Error removing PID file {pid_file}: {e}")

def signal_handler(sig, frame):
    """Handle Ctrl-C gracefully"""
    logger.info("Received interrupt signal (Ctrl-C), shutting down gracefully...")
    
    # Terminate all running processes
    for process in running_processes:
        if process and process.poll() is None:  # Process is still running
            try:
                logger.info(f"Terminating process PID {process.pid}")
                process.terminate()
                # Give it a moment to terminate gracefully
                try:
                    process.wait(timeout=5)
                    logger.info(f"Process PID {process.pid} terminated successfully")
                except subprocess.TimeoutExpired:
                    logger.warning(f"Process PID {process.pid} did not terminate, forcing kill")
                    process.kill()
                    process.wait()
            except Exception as e:
                logger.error(f"Error terminating process PID {process.pid}: {e}")
    
    # Clean up PID files
    for pid_file in pid_files:
        cleanup_pid_file(pid_file)
    
    logger.info("Shutdown complete")
    sys.exit(0)

# Run python in subprocess
def run_script(script_name, pid_file, *args):
    process = None
    try:
        # Path to the Python interpreter inside the virtual environment
        python_executable = './env/bin/python'

        # Combine the script name and arguments
        command = [python_executable, script_name] + list(args)

        # Run the subprocess (output goes directly to console for real-time viewing)
        process = subprocess.Popen(command)
        
        # Track the process globally
        running_processes.append(process)
        
        # Write PID to file
        with open(pid_file, 'w') as f:
            f.write(str(process.pid))
        logger.info(f"Started {script_name} with PID {process.pid}, written to {pid_file}")
        
        # Wait for the process to complete
        process.wait()
        
    except Exception as e:
        logger.error(f"Error running {script_name}: {e}")
    finally:
        # Clean up PID file when process exits
        cleanup_pid_file(pid_file)

# Parse runtime argument (--config) and start subprocess threads
def main():
    # Register signal handler for Ctrl-C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    parser = argparse.ArgumentParser(description="Helper script to run the database and web frontend in separate threads.")

    # Add --config runtime argument
    parser.add_argument('--config', help="Path to the configuration file.", default='config.ini')
    args = parser.parse_args()

    # PID file paths
    db_pid_file = 'meshview-db.pid'
    web_pid_file = 'meshview-web.pid'
    
    # Track PID files globally for cleanup
    pid_files.append(db_pid_file)
    pid_files.append(web_pid_file)

    # Database Thread
    dbthrd = threading.Thread(target=run_script, args=('startdb.py', db_pid_file, '--config', args.config))

    # Web server thread
    webthrd = threading.Thread(target=run_script, args=('main.py', web_pid_file, '--config', args.config))

    # Start Meshview subprocess threads
    logger.info(f"Starting Meshview with config: {args.config}")
    logger.info("Starting database thread...")
    dbthrd.start()
    logger.info("Starting web server thread...")
    webthrd.start()

    try:
        dbthrd.join()
        webthrd.join()
    except KeyboardInterrupt:
        # This shouldn't be reached due to signal handler, but just in case
        signal_handler(signal.SIGINT, None)

if __name__ == '__main__':
    main()
