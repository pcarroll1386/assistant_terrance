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
        self.current_job = self.jobs[0] if self.jobs else None  # Set the first job as current if available
        self.current_job_task = self.jobs[0].tasks[0] if self.jobs and self.jobs[0].tasks else None  # Set the first task of the first job as current
        self.current_job_index = 0
        self.current_task_index = 0

    def set_current_job(self, job):
        """Set the current job."""
        self.current_job = job

    def set_current_job_task(self, task: Task):
        """Set the current job task."""
        self.current_job_task = task

    def scroll_job(self, direction: str):
        """Move to the next or previous job in the list."""
        if direction == 'next':
            self.current_job_index += 1
            if self.current_job_index >= len(self.jobs):
                self.current_job_index = 0
        elif direction == 'previous':
            self.current_job_index -= 1
            if self.current_job_index < 0:
                self.current_job_index = len(self.jobs) - 1
        else:
            raise ValueError("Direction must be 'next' or 'previous'.")
        self.current_job = self.jobs[self.current_job_index]
        if self.current_job_task not in self.current_job.tasks:
            self.current_job_task = self.current_job.tasks[0]

    def scroll_task(self, direction: str):
        """Move to the next or previous task in the current job."""
        if direction == 'next':
            self.current_task_index += 1
            if self.current_task_index >= len(self.current_job.tasks):
                self.current_task_index = 0
            return self.current_job.tasks[self.current_task_index]
        elif direction == 'previous':
            self.current_task_index -= 1
            if self.current_task_index < 0:
                self.current_task_index = len(self.current_job.tasks) - 1
            return self.current_job.tasks[self.current_task_index]
        else:
            raise ValueError("Direction must be 'next' or 'previous'.")
      