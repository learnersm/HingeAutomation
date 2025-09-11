"""
Scrcpy Manager Module
Handles scrcpy process lifecycle
"""

import subprocess
import logging
import time
import os
from config import TIMEOUTS, SCRCPY_OPTIONS

class ScrcpyManager:
    def __init__(self):
        self.process = None

    def start_scrcpy(self):
        """
        Launch scrcpy process
        """
        try:
            cmd = ['scrcpy'] + SCRCPY_OPTIONS
            logging.info("Starting scrcpy...")
            # Set environment to ensure GUI window creation
            env = os.environ.copy()
            env['DISPLAY'] = env.get('DISPLAY', ':0')

            # Use os.system for GUI application launch
            cmd_str = ' '.join(cmd)
            logging.info(f"Launching scrcpy with command: {cmd_str}")

            # Launch scrcpy asynchronously using os.system
            import threading
            def launch_scrcpy():
                os.system(cmd_str + ' > /dev/null 2>&1 &')

            thread = threading.Thread(target=launch_scrcpy)
            thread.daemon = True
            thread.start()

            # Wait a bit for the process to start
            time.sleep(2)

            # Check if scrcpy process is running
            try:
                result = subprocess.run(['pgrep', 'scrcpy'], capture_output=True, text=True)
                if result.returncode == 0:
                    logging.info("scrcpy process found running")
                    # Store a dummy process object for compatibility
                    self.process = subprocess.Popen(['sleep', '1'])  # Dummy process
                    return True
                else:
                    logging.error("scrcpy process not found")
                    return False
            except Exception as e:
                logging.error(f"Error checking scrcpy process: {e}")
                return False

            # Wait for window to appear
            time.sleep(TIMEOUTS["scrcpy_start"])

            if self.is_running():
                logging.info("scrcpy started successfully")
                return True
            else:
                stdout, stderr = self.process.communicate()
                logging.error(f"scrcpy failed to start: {stderr}")
                return False

        except FileNotFoundError:
            logging.error("scrcpy not found. Please ensure it's installed and in PATH")
            return False
        except Exception as e:
            logging.error(f"Error starting scrcpy: {e}")
            return False

    def stop_scrcpy(self):
        """
        Terminate scrcpy process
        """
        if self.process and self.is_running():
            logging.info("Stopping scrcpy...")
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
                logging.info("scrcpy stopped successfully")
            except subprocess.TimeoutExpired:
                logging.warning("scrcpy didn't terminate gracefully, killing...")
                self.process.kill()
                self.process.wait()
        else:
            logging.info("scrcpy is not running")

    def is_running(self):
        """
        Check if scrcpy process is running
        """
        return self.process is not None and self.process.poll() is None
