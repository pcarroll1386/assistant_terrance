from typing import List, Dict, Optional
from src.repositories.job_tasks_repo import JobTasksRepository

class JobTaskService:
    def __init__(self):
        self.task_repo = JobTasksRepository()

    def get_all_tasks(self) -> List[Dict]:
        """Get all available job tasks."""
        return self.task_repo.get_all_tasks()

    def get_task_by_id(self, task_id: int) -> Optional[Dict]:
        """Get a specific task by ID."""
        return self.task_repo.get_task_by_id(task_id)

    def get_task_by_short_name(self, short_name: str) -> Optional[Dict]:
        """Get a task by its short name."""
        return self.task_repo.get_task_by_short_name(short_name)

    def get_tasks_by_ids(self, task_ids: List[int]) -> List[Dict]:
        """Get multiple tasks by their IDs."""
        return self.task_repo.get_tasks_by_ids(task_ids)

    def search_tasks_by_name(self, search_term: str) -> List[Dict]:
        """Search tasks by name pattern."""
        return self.task_repo.get_tasks_by_name_pattern(search_term)

    def search_tasks_by_short_name(self, search_term: str) -> List[Dict]:
        """Search tasks by short name pattern."""
        return self.task_repo.get_tasks_by_short_name_pattern(search_term)

    def get_tasks_for_display(self, limit: int = None) -> List[Dict]:
        """Get tasks formatted for LCD display with essential info only."""
        tasks = self.task_repo.get_all_tasks()
        
        display_tasks = []
        for task in tasks:
            display_task = {
                'id': task.get('id'),
                'short_name': task.get('short_name'),
                'name': task.get('name')[:15] + '...' if len(task.get('name', '')) > 15 else task.get('name')
            }
            display_tasks.append(display_task)
        
        if limit:
            return display_tasks[:limit]
        
        return display_tasks

    def get_task_names_by_ids(self, task_ids: List[int]) -> List[str]:
        """Get just the task names for given IDs."""
        tasks = self.task_repo.get_tasks_by_ids(task_ids)
        return [task.get('name', '') for task in tasks]

    def get_task_short_names_by_ids(self, task_ids: List[int]) -> List[str]:
        """Get just the task short names for given IDs."""
        tasks = self.task_repo.get_tasks_by_ids(task_ids)
        return [task.get('short_name', '') for task in tasks]

    def get_common_tasks(self) -> List[Dict]:
        """Get commonly used tasks (basic workflow tasks)."""
        common_task_short_names = ['prep', 'cut', 'sew', 'press', 'qc', 'pack']
        
        all_tasks = self.task_repo.get_all_tasks()
        common_tasks = []
        
        for task in all_tasks:
            if task.get('short_name') in common_task_short_names:
                common_tasks.append(task)
        
        return common_tasks

    def get_specialized_tasks(self) -> List[Dict]:
        """Get specialized tasks (not in basic workflow)."""
        basic_task_short_names = ['prep', 'cut', 'sew', 'press', 'qc', 'pack']
        
        all_tasks = self.task_repo.get_all_tasks()
        specialized_tasks = []
        
        for task in all_tasks:
            if task.get('short_name') not in basic_task_short_names:
                specialized_tasks.append(task)
        
        return specialized_tasks

    def validate_task_ids(self, task_ids: List[int]) -> Dict[str, any]:
        """Validate that all provided task IDs exist."""
        all_task_ids = self.task_repo.get_task_ids()
        
        valid_ids = []
        invalid_ids = []
        
        for task_id in task_ids:
            if task_id in all_task_ids:
                valid_ids.append(task_id)
            else:
                invalid_ids.append(task_id)
        
        return {
            'all_valid': len(invalid_ids) == 0,
            'valid_ids': valid_ids,
            'invalid_ids': invalid_ids,
            'total_requested': len(task_ids),
            'valid_count': len(valid_ids)
        }

    def get_task_summary(self) -> Dict[str, any]:
        """Get a summary of all tasks."""
        all_tasks = self.task_repo.get_all_tasks()
        
        # Categorize tasks by type
        cutting_tasks = [t for t in all_tasks if 'cut' in t.get('short_name', '').lower() or 'cut' in t.get('name', '').lower()]
        sewing_tasks = [t for t in all_tasks if 'sew' in t.get('short_name', '').lower() or 'sew' in t.get('name', '').lower()]
        finishing_tasks = [t for t in all_tasks if any(word in t.get('name', '').lower() for word in ['press', 'finish', 'hem', 'pack'])]
        
        return {
            'total_tasks': len(all_tasks),
            'cutting_related': len(cutting_tasks),
            'sewing_related': len(sewing_tasks),
            'finishing_related': len(finishing_tasks),
            'task_ids': [t.get('id') for t in all_tasks],
            'short_names': [t.get('short_name') for t in all_tasks]
        }

    def create_task(self, task_data: Dict) -> Dict:
        """Create a new task."""
        return self.task_repo.create_task(task_data)

    def update_task(self, task_id: int, task_data: Dict) -> Optional[Dict]:
        """Update an existing task."""
        return self.task_repo.update_task(task_id, task_data)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        return self.task_repo.delete_task(task_id)

    def validate_task_data(self, task_data: Dict) -> Dict[str, any]:
        """Validate task data and return validation result."""
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ['name', 'short_name']
        for field in required_fields:
            if field not in task_data or not task_data[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate short_name length
        short_name = task_data.get('short_name', '')
        if short_name and len(short_name) > 7:
            errors.append("short_name must be 7 characters or less")
        
        # Check if short_name already exists
        if short_name:
            existing_task = self.task_repo.get_task_by_short_name(short_name)
            if existing_task:
                errors.append(f"Task with short_name '{short_name}' already exists")
        
        # Check name length for display purposes
        name = task_data.get('name', '')
        if name and len(name) > 50:
            warnings.append("Task name is quite long and may be truncated in displays")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def get_tasks_count(self) -> int:
        """Get total number of tasks."""
        return self.task_repo.get_tasks_count()

    def task_exists(self, task_id: int) -> bool:
        """Check if a task exists."""
        return self.task_repo.task_exists(task_id)
