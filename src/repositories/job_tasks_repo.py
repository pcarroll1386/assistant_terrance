import json
import os
from typing import List, Dict, Optional

class JobTasksRepository:
    def __init__(self, json_file_path: str = None):
        if json_file_path is None:
            # Default to the mock data file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.json_file_path = os.path.join(current_dir, "..", "mock_data", "job_tasks.json")
        else:
            self.json_file_path = json_file_path

    def _load_tasks(self) -> List[Dict]:
        """Load job tasks from the JSON file."""
        try:
            with open(self.json_file_path, 'r') as file:
                data = json.load(file)
                return data.get('job_tasks', [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def _save_tasks(self, tasks: List[Dict]) -> None:
        """Save job tasks to the JSON file."""
        data = {"job_tasks": tasks}
        with open(self.json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def get_all_tasks(self) -> List[Dict]:
        """Get all job tasks from the JSON file."""
        return self._load_tasks()

    def get_task_by_id(self, task_id: int) -> Optional[Dict]:
        """Retrieve a task by its ID from the JSON file."""
        tasks = self._load_tasks()
        for task in tasks:
            if task.get('id') == task_id:
                return task
        return None

    def get_task_by_short_name(self, short_name: str) -> Optional[Dict]:
        """Get a task by its short name."""
        tasks = self._load_tasks()
        for task in tasks:
            if task.get('short_name') == short_name:
                return task
        return None

    def get_tasks_by_name_pattern(self, pattern: str) -> List[Dict]:
        """Get tasks where the name contains the given pattern (case-insensitive)."""
        tasks = self._load_tasks()
        pattern_lower = pattern.lower()
        return [task for task in tasks if pattern_lower in task.get('name', '').lower()]

    def get_tasks_by_short_name_pattern(self, pattern: str) -> List[Dict]:
        """Get tasks where the short_name contains the given pattern."""
        tasks = self._load_tasks()
        return [task for task in tasks if pattern in task.get('short_name', '')]

    def create_task(self, task_data: Dict) -> Dict:
        """Create a new task in the JSON file."""
        tasks = self._load_tasks()
        
        # Generate new ID if not provided
        if 'id' not in task_data or task_data['id'] is None:
            existing_ids = [task.get('id', 0) for task in tasks]
            task_data['id'] = max(existing_ids, default=0) + 1
        
        tasks.append(task_data)
        self._save_tasks(tasks)
        return task_data

    def update_task(self, task_id: int, task_data: Dict) -> Optional[Dict]:
        """Update an existing task in the JSON file."""
        tasks = self._load_tasks()
        
        for i, task in enumerate(tasks):
            if task.get('id') == task_id:
                # Update the task data while preserving the ID
                task_data['id'] = task_id
                tasks[i] = task_data
                self._save_tasks(tasks)
                return task_data
        
        return None

    def delete_task(self, task_id: int) -> bool:
        """Delete a task from the JSON file."""
        tasks = self._load_tasks()
        
        for i, task in enumerate(tasks):
            if task.get('id') == task_id:
                tasks.pop(i)
                self._save_tasks(tasks)
                return True
        
        return False

    def task_exists(self, task_id: int) -> bool:
        """Check if a task with the given ID exists."""
        return self.get_task_by_id(task_id) is not None

    def get_task_ids(self) -> List[int]:
        """Get a list of all task IDs."""
        tasks = self._load_tasks()
        return [task.get('id') for task in tasks if task.get('id') is not None]

    def get_tasks_by_ids(self, task_ids: List[int]) -> List[Dict]:
        """Get multiple tasks by their IDs."""
        tasks = self._load_tasks()
        result = []
        
        for task_id in task_ids:
            for task in tasks:
                if task.get('id') == task_id:
                    result.append(task)
                    break
        
        return result

    def validate_task_structure(self, task_data: Dict) -> bool:
        """Validate that task data has required fields."""
        required_fields = ['name', 'short_name']
        return all(field in task_data for field in required_fields)

    def get_tasks_count(self) -> int:
        """Get the total number of tasks."""
        return len(self._load_tasks())
