## Standard Library Imports
import json
import os
from typing import List, Dict, Optional

## Local Imports
from src.schemas.job_schemas import Job, Task

class JobRepository:
    def __init__(self, json_file_path: str = None):
        if json_file_path is None:
            # Default to the mock data file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.json_file_path = os.path.join(current_dir, "..", "mock_data", "jobs.json")
        else:
            self.json_file_path = json_file_path

    def _load_jobs(self) -> List[Job]:
        """Load jobs from the JSON file. and convert them to Job instances."""
        try:
            with open(self.json_file_path, 'r') as file:
                data = json.load(file)
                jobs = []
                if 'jobs' in data:
                    for job in data['jobs']:
                        # Convert each job dictionary to a Job instance
                        job = Job.from_dict(job)
                        jobs.append(job)
                return jobs
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def _save_jobs(self, jobs: List[Job]) -> None:
        """Save jobs to the JSON file."""
        # Convert Job objects to dictionaries for JSON serialization
        jobs_data = [job.to_dict() for job in jobs]
        data = {"jobs": jobs_data}
        with open(self.json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def get_all_jobs(self) -> List[Job]:
        """Get all jobs from the JSON file."""
        return self._load_jobs()

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        """Retrieve a job by its ID from the JSON file."""
        jobs = self._load_jobs()
        for job in jobs:
            if job.id == job_id:
                return job
        return None

    def get_jobs_by_short_name(self, short_name: str) -> List[Job]:
        """Get jobs that match the given short name."""
        jobs = self._load_jobs()
        return [job for job in jobs if job.short_name == short_name]

    def get_jobs_by_type(self, job_type: str) -> List[Job]:
        """Get jobs by type (custom or prefab based on short_name prefix)."""
        jobs = self._load_jobs()
        if job_type.lower() == 'custom':
            return [job for job in jobs if job.short_name.startswith('c-ms')]
        elif job_type.lower() == 'prefab':
            return [job for job in jobs if job.short_name.startswith('pf-')]
        return []

    def create_job(self, job_data: Dict) -> Job:
        """Create a new job in the JSON file."""
        jobs = self._load_jobs()
        
        # Generate new ID if not provided
        if 'id' not in job_data or job_data['id'] is None:
            existing_ids = [job.id for job in jobs]
            job_data['id'] = max(existing_ids, default=0) + 1
        
        # Create Job object from dictionary
        new_job = Job.from_dict(job_data)
        jobs.append(new_job)
        self._save_jobs(jobs)
        return new_job

    def update_job(self, job_id: int, job_data: Dict) -> Optional[Job]:
        """Update an existing job in the JSON file."""
        jobs = self._load_jobs()
        
        for i, job in enumerate(jobs):
            if job.id == job_id:
                # Update the job data while preserving the ID
                job_data['id'] = job_id
                updated_job = Job.from_dict(job_data)
                jobs[i] = updated_job
                self._save_jobs(jobs)
                return updated_job
        
        return None

    def delete_job(self, job_id: int) -> bool:
        """Delete a job from the JSON file."""
        jobs = self._load_jobs()
        
        for i, job in enumerate(jobs):
            if job.id == job_id:
                jobs.pop(i)
                self._save_jobs(jobs)
                return True
        
        return False

    def get_jobs_with_task(self, task_id: int) -> List[Job]:
        """Get all jobs that contain a specific task ID."""
        jobs = self._load_jobs()
        result = []
        
        for job in jobs:
            for task in job.tasks:
                if task.id == task_id:
                    result.append(job)
                    break
        
        return result
