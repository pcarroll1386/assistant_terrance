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
        self.tasks = []  # Initialize an empty list for tasks

    def add_task(self, task):
        """Add a new task to the job controller."""
        self.tasks.append(task)
        print(f"Task added: {task}")

    def get_tasks(self):
        """Return the list of tasks."""
        return self.tasks