## Standard Library Imports
from typing import List, Dict, Optional

## Local Imports
from src.schemas.job_schemas import Job, Task
from src.services.jobs_service import JobsService


class JobController():
    """Controller for managing jobs and tasks."""
    
    def __init__(self):
        self.job_service = JobsService()
        self.jobs = self.job_service.get_all_jobs()  # Load all jobs from the service
        self.current_job = None
        self.current_job_task = None
        self.current_job_index = 0
        self.current_task_index = 0

    def add_task(self, task):
        """Add a new task to the job controller."""
        self.tasks.append(task)
        print(f"Task added: {task}")

    def get_tasks(self):
        """Return the list of tasks."""
        return self.tasks

    def set_current_job(self, job):
        """Set the current job."""
        self.current_job = job

    def set_current_job_task(self, task: Task):
        """Set the current job task."""
        self.current_job_task = task

    def next_job(self):
        """Move to the next job in the list."""
        pass

    def previous_job(self):
        """Move to the previous job in the list."""
        pass

    def next_task(self):
        """Move to the next task in the current job."""
        pass

    def previous_task(self):
        """Move to the previous task in the current job."""
        pass