"""
Job schema classes for deserializing JSON data into Python objects.

This module contains dataclasses and schemas for jobs and tasks used in the 
LCD Product Display System for tracking sewing/craft jobs and tasks.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union, Dict, Any
import json


@dataclass
class Task:
    """Represents a single task within a job."""
    id: int
    name: str
    short_name: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a Task instance from a dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            short_name=data['short_name']
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Task instance to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name
        }


@dataclass
class Job:
    """Represents a complete job with embedded tasks."""
    id: int
    name: str
    short_name: str
    ingress_date: str  # ISO format datetime string
    start_date: str    # ISO format datetime string
    tasks: List[Task]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Job':
        """Create a Job instance from a dictionary."""
        tasks = [Task.from_dict(task_data) for task_data in data.get('tasks', [])]
        return cls(
            id=data['id'],
            name=data['name'],
            short_name=data['short_name'],
            ingress_date=data['ingress_date'],
            start_date=data['start_date'],
            tasks=tasks
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Job instance to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name,
            'ingress_date': self.ingress_date,
            'start_date': self.start_date,
            'tasks': [task.to_dict() for task in self.tasks]
        }
    
    @property
    def ingress_datetime(self) -> datetime:
        """Get ingress_date as a datetime object."""
        return datetime.fromisoformat(self.ingress_date.replace('Z', '+00:00'))
    
    @property
    def start_datetime(self) -> datetime:
        """Get start_date as a datetime object."""
        return datetime.fromisoformat(self.start_date.replace('Z', '+00:00'))
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a specific task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_task_by_short_name(self, short_name: str) -> Optional[Task]:
        """Get a specific task by its short name."""
        for task in self.tasks:
            if task.short_name == short_name:
                return task
        return None
    
    @property
    def is_custom_job(self) -> bool:
        """Check if this is a custom job (starts with 'c-ms')."""
        return self.short_name.startswith('c-ms')
    
    @property
    def is_prefab_job(self) -> bool:
        """Check if this is a prefab job (starts with 'pf-')."""
        return self.short_name.startswith('pf-')


@dataclass
class JobsContainer:
    """Container for multiple jobs, matching the JSON structure."""
    jobs: List[Job]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JobsContainer':
        """Create a JobsContainer instance from a dictionary."""
        jobs = [Job.from_dict(job_data) for job_data in data.get('jobs', [])]
        return cls(jobs=jobs)
    
    @classmethod
    def from_json_file(cls, file_path: str) -> 'JobsContainer':
        """Load JobsContainer from a JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert JobsContainer instance to dictionary."""
        return {
            'jobs': [job.to_dict() for job in self.jobs]
        }
    
    def to_json_file(self, file_path: str, indent: int = 4) -> None:
        """Save JobsContainer to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=indent)
    
    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        """Get a specific job by its ID."""
        for job in self.jobs:
            if job.id == job_id:
                return job
        return None
    
    def get_job_by_short_name(self, short_name: str) -> Optional[Job]:
        """Get a specific job by its short name."""
        for job in self.jobs:
            if job.short_name == short_name:
                return job
        return None
    
    def get_custom_jobs(self) -> List[Job]:
        """Get all custom jobs (c-ms* pattern)."""
        return [job for job in self.jobs if job.is_custom_job]
    
    def get_prefab_jobs(self) -> List[Job]:
        """Get all prefab jobs (pf-* pattern)."""
        return [job for job in self.jobs if job.is_prefab_job]
    
    def get_jobs_by_type(self, job_type: str) -> List[Job]:
        """Get jobs by type ('custom', 'prefab', or 'all')."""
        if job_type.lower() == 'custom':
            return self.get_custom_jobs()
        elif job_type.lower() == 'prefab':
            return self.get_prefab_jobs()
        else:
            return self.jobs
    
    def add_job(self, job: Job) -> None:
        """Add a new job to the container."""
        self.jobs.append(job)
    
    def remove_job(self, job_id: int) -> bool:
        """Remove a job by its ID. Returns True if removed, False if not found."""
        for i, job in enumerate(self.jobs):
            if job.id == job_id:
                del self.jobs[i]
                return True
        return False
    
    @property
    def job_count(self) -> int:
        """Get the total number of jobs."""
        return len(self.jobs)
    
    @property
    def custom_job_count(self) -> int:
        """Get the number of custom jobs."""
        return len(self.get_custom_jobs())
    
    @property
    def prefab_job_count(self) -> int:
        """Get the number of prefab jobs."""
        return len(self.get_prefab_jobs())


# Utility functions for common operations
def load_jobs_from_json(file_path: str) -> JobsContainer:
    """Load jobs from a JSON file."""
    return JobsContainer.from_json_file(file_path)


def save_jobs_to_json(jobs_container: JobsContainer, file_path: str, indent: int = 4) -> None:
    """Save jobs to a JSON file."""
    jobs_container.to_json_file(file_path, indent)


def create_job_from_data(job_data: Dict[str, Any]) -> Job:
    """Create a Job instance from raw data."""
    return Job.from_dict(job_data)


def create_task_from_data(task_data: Dict[str, Any]) -> Task:
    """Create a Task instance from raw data."""
    return Task.from_dict(task_data)


# Example usage and validation
if __name__ == "__main__":
    # Example of how to use the schemas
    sample_job_data = {
        "id": 1001,
        "name": "Custom Baseball Cap",
        "short_name": "c-ms01",
        "ingress_date": "2025-07-15T08:30:00Z",
        "start_date": "2025-07-16T09:00:00Z",
        "tasks": [
            {"id": 1, "name": "Pattern Cutting", "short_name": "cut"},
            {"id": 2, "name": "Fabric Preparation", "short_name": "prep"},
            {"id": 3, "name": "Steam Pressing", "short_name": "press"}
        ]
    }
    
    # Create job object
    job = Job.from_dict(sample_job_data)
    print(f"Created job: {job.name} ({job.short_name})")
    print(f"Tasks: {len(job.tasks)}")
    print(f"Is custom job: {job.is_custom_job}")
    print(f"Ingress datetime: {job.ingress_datetime}")
    
    # Convert back to dict
    job_dict = job.to_dict()
    print("Converted back to dict successfully")
    
    # Create jobs container
    jobs_data = {"jobs": [sample_job_data]}
    jobs_container = JobsContainer.from_dict(jobs_data)
    print(f"Jobs container created with {jobs_container.job_count} jobs")
