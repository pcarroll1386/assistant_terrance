## Standard Library Imports
from typing import List, Dict, Optional
from datetime import datetime

## Local Imports
from src.repositories.job_repo import JobRepository
from src.schemas.job_schemas import Job, Task


class JobsService:
    def __init__(self):
        self.job_repo = JobRepository()

    def get_all_jobs(self) -> List[Job]:
        """Get all jobs."""
        return self.job_repo.get_all_jobs()

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        """Get a specific job by ID."""
        return self.job_repo.get_job_by_id(job_id)

    def get_jobs_by_type(self, job_type: str) -> List[Job]:
        """Get jobs by type (custom or prefab)."""
        return self.job_repo.get_jobs_by_type(job_type)

    def get_custom_jobs(self) -> List[Job]:
        """Get all custom jobs (c-ms prefix)."""
        return self.job_repo.get_jobs_by_type('custom')

    def get_prefab_jobs(self) -> List[Job]:
        """Get all prefab jobs (pf- prefix)."""
        return self.job_repo.get_jobs_by_type('prefab')

    def get_job_by_short_name(self, short_name: str) -> Optional[Job]:
        """Get a job by its short name."""
        jobs = self.job_repo.get_jobs_by_short_name(short_name)
        return jobs[0] if jobs else None

    def get_active_jobs(self) -> List[Job]:
        """Get jobs that have started (start_date has passed)."""
        from datetime import timezone
        current_time = datetime.now(timezone.utc)
        
        active_jobs = []
        for job in self.job_repo.get_all_jobs():
            if job.start_datetime <= current_time:
                active_jobs.append(job)
        
        return active_jobs

    def get_pending_jobs(self) -> List[Job]:
        """Get jobs that haven't started yet (start_date is in the future)."""
        from datetime import timezone
        current_time = datetime.now(timezone.utc)
        
        pending_jobs = []
        for job in self.job_repo.get_all_jobs():
            if job.start_datetime > current_time:
                pending_jobs.append(job)
        
        return pending_jobs

    def get_jobs_with_task_count(self) -> List[Dict]:
        """Get all jobs with task count added as dictionary for compatibility."""
        jobs_with_count = []
        
        for job in self.job_repo.get_all_jobs():
            job_dict = job.to_dict()
            job_dict['task_count'] = len(job.tasks)
            jobs_with_count.append(job_dict)
        
        return jobs_with_count

    def get_job_summary(self, job_id: int) -> Optional[Dict]:
        """Get a summary of a job with basic info and task count."""
        job = self.get_job_by_id(job_id)
        
        if job:
            summary = {
                'id': job.id,
                'name': job.name,
                'short_name': job.short_name,
                'ingress_date': job.ingress_date,
                'start_date': job.start_date,
                'task_count': len(job.tasks),
                'type': 'custom' if job.is_custom_job else 'prefab'
            }
            return summary
        
        return None

    def get_jobs_for_display(self, limit: int = None) -> List[Job]:
        """Get jobs formatted for LCD display with essential info only."""
        jobs = self.job_repo.get_all_jobs()
        
        if limit:
            return jobs[:limit]
        
        return jobs

    def create_job(self, job_data: Dict) -> Job:
        """Create a new job from dictionary data."""
        return self.job_repo.create_job(job_data)

    def update_job(self, job_id: int, job_data: Dict) -> Optional[Job]:
        """Update an existing job."""
        return self.job_repo.update_job(job_id, job_data)

    def delete_job(self, job_id: int) -> bool:
        """Delete a job."""
        return self.job_repo.delete_job(job_id)

    def get_jobs_count(self) -> Dict[str, int]:
        """Get count of different job types."""
        all_jobs = self.job_repo.get_all_jobs()
        custom_jobs = self.get_custom_jobs()
        prefab_jobs = self.get_prefab_jobs()
        
        return {
            'total': len(all_jobs),
            'custom': len(custom_jobs),
            'prefab': len(prefab_jobs)
        }

    def validate_job_data(self, job_data: Dict) -> Dict[str, any]:
        """Validate job data and return validation result."""
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ['name', 'short_name', 'ingress_date', 'start_date']
        for field in required_fields:
            if field not in job_data or not job_data[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate short_name format
        short_name = job_data.get('short_name', '')
        if short_name and not (short_name.startswith('c-ms') or short_name.startswith('pf-')):
            errors.append("short_name must start with 'c-ms' (custom) or 'pf-' (prefab)")
        
        # Check if short_name already exists
        if short_name:
            existing_job = self.get_job_by_short_name(short_name)
            if existing_job:
                errors.append(f"Job with short_name '{short_name}' already exists")
        
        # Validate tasks
        tasks = job_data.get('tasks', [])
        if not tasks:
            warnings.append("Job has no tasks assigned")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def save_jobs_to_file(self) -> bool:
        """Save operations are handled automatically by the JobRepository."""
        # The JobRepository saves to file automatically on create/update/delete operations
        return True

    def reload_jobs_from_file(self) -> bool:
        """Jobs are loaded fresh from file on each repository operation."""
        # The JobRepository loads from file on each operation, so no explicit reload needed
        return True
