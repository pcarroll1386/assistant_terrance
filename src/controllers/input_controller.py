## Standard Library Imports
import sys
import select
import termios
import tty

class InputController:
    """Controller for handling keyboard input and navigation."""
    
    def __init__(self):
        """Initialize the input controller."""
        self.old_settings = None
        self._setup_terminal()
    
    def _setup_terminal(self):
        """Setup terminal for raw input (non-blocking, no echo)."""
        try:
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
        except (termios.error, AttributeError):
            # Fallback if terminal setup fails
            self.old_settings = None
    
    def _restore_terminal(self):
        """Restore terminal to original settings."""
        if self.old_settings:
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            except (termios.error, AttributeError):
                pass
    
    def check_input(self):
        """Check for keyboard input without blocking."""
        try:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.read(1)
                return key
        except (OSError, ValueError):
            # Fallback method
            pass
        return None
    
    def process_navigation_input(self, key, navigation_callbacks):
        """
        Process navigation input and call appropriate callbacks.
        
        Args:
            key: The pressed key
            navigation_callbacks: Dict with callback functions for each action
                Expected keys: 'next_job', 'previous_job', 'next_task', 'previous_task', 'quit'
        """
        if not key:
            return False
            
        key_lower = key.lower()
        print(f"DEBUG: Processing key '{key_lower}'")
        
        if key_lower == 'j' and 'next_job' in navigation_callbacks:
            print("DEBUG: Calling next_job")
            navigation_callbacks['next_job']()
            return True
        elif key_lower == 'k' and 'previous_job' in navigation_callbacks:
            print("DEBUG: Calling previous_job")
            navigation_callbacks['previous_job']()
            return True
        elif key_lower == 'n' and 'next_task' in navigation_callbacks:
            print("DEBUG: Calling next_task")
            navigation_callbacks['next_task']()
            return True
        elif key_lower == 'p' and 'previous_task' in navigation_callbacks:
            print("DEBUG: Calling previous_task")
            navigation_callbacks['previous_task']()
            return True
        elif key_lower == 'q' and 'quit' in navigation_callbacks:
            print("DEBUG: Calling quit")
            navigation_callbacks['quit']()
            return True
        else:
            print(f"DEBUG: No action for key '{key_lower}'")
        
        return False
    
    def get_control_help_text(self):
        """Get help text for available controls."""
        return {
            'line1': "Controls:",
            'line2': "j/k=job n/p=task"
        }
    
    def get_extended_help_text(self):
        """Get extended help text for all controls."""
        return [
            "Navigation Controls:",
            "j = Next Job",
            "k = Previous Job", 
            "n = Next Task",
            "p = Previous Task",
            "q = Quit"
        ]
