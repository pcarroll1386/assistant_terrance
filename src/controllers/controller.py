## Standard Library Imports
import sys
import time

## Local Imports
from src.physical_interface.mockLCD import CharLCD1602 as LCD  # Adjusted import
from src.services.jobs_service import JobsService
from src.services.job_task_service import JobTaskService
from src.controllers.timer_controller import TimerController
from src.controllers.input_controller import InputController
from src.controllers.job_controller import JobController
from src.schemas.job_schemas import JobsContainer, Job, Task


class Controller(object):
    """Controller class to manage the appication logic."""
    def __init__(self):
        """Initialize the controller."""
        self.job_service = JobsService()
        self.job_tasks = JobTaskService()
        self.job_controller= JobController()
        self.lcd = LCD()
        self.timer = TimerController()
        self.input_controller = InputController()


    def shutdown(self):
        """Shutdown the controller."""
        self.lcd.write(0, 0, "Exiting...")
        self.lcd.write(0, 1, "Goodbye!")
        self.lcd.destroy()
        # Restore terminal settings
        self.input_controller._restore_terminal()
        sys.exit()


    def check_input(self):
        """Check for keyboard input without blocking."""
        return self.input_controller.check_input()
  
    def loop(self):
        self.lcd.write(0, 0, "Good morning")
        time.sleep(.3)
        self.lcd.write(0, 1, "Ma'am:")
        time.sleep(1)
        
        self.job_list = self.job_service.get_active_jobs()
        if not self.job_list:
            self.lcd.write(0, 0, "No active jobs")
            self.lcd.write(0, 1, "Please check later")
            self.shutdown()

        self._initialize_current_selections()
        self._display_controls()
        
        # Setup navigation callbacks
        navigation_callbacks = {
            'next_job': self.next_job,
            'previous_job': self.previous_job,
            'next_task': self.next_task,
            'previous_task': self.previous_task,
            'quit': self.shutdown
        }
        
        try:
            while True:
                # Check for key input and process
                key = self.input_controller.check_input()
                if key:
                    print(f"\n[DEBUG] Key pressed: '{key}' (ord: {ord(key)})")
                    result = self.input_controller.process_navigation_input(key, navigation_callbacks)
                    if result:
                        print(f"[DEBUG] Navigation action processed for key '{key}'")
                
                # Display current status
                self._display_current_status()
                
                self.count += 1
                time.sleep(0.1)  # Reduced sleep for more responsive input
                
        except KeyboardInterrupt:
            self.shutdown()

    def _initialize_current_selections(self):
        """Initialize current job and task selections."""
        if self.current_job == None:
            self.set_current_job(self.job_list[0])

        if self.current_job_task not in self.current_job.tasks:
            tasks = self.current_job.tasks[0]
            if tasks:
                self.set_current_job_task(tasks[0])

    def _display_controls(self):
        """Display control instructions."""
        help_text = self.input_controller.get_control_help_text()
        self.lcd.write(0, 0, help_text['line1'])
        self.lcd.write(0, 1, help_text['line2'])
        time.sleep(2)

    def _display_current_status(self):
        """Display current job and task status."""
        if self.current_job and self.current_job_task:
            self.lcd.write(0, 0, f"{self.current_job['short_name']} {self.current_job_task['short_name']}")
            self.lcd.write(0, 1, f"{self.timer.get_daily_elapsed_time()} {self.timer.get_task_elapsed_time()}")