from fastapi import APIRouter, HTTPException
from models.request.task import Task 
from models.mongo.task import MongoTask 
from datetime import datetime
import json
from typing import Optional
from mongoengine.errors import DoesNotExist
import logging

# Create a logger instance
logger = logging.getLogger(__name__)

tasks_api = APIRouter(prefix='/tasks')

@tasks_api.post('', tags=["Task"])
async def create_task(task: Task):
    try:
        task_dict = task.model_dump()
        task_dict['created_at'] = datetime.utcnow()
        task_dict['updated_at'] = datetime.utcnow()
        mongo_task = MongoTask(**task_dict)
        mongo_task.save()

        return json.loads(mongo_task.to_json())
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@tasks_api.get('', tags=["Task"])
async def get_tasks(task_id: Optional[str] = None, completed: Optional[bool] = None):
    try:
        if task_id:
            task = MongoTask.objects.get(task_id=task_id)
            return json.loads(task.to_json())
        else:
            query = {}

            if completed is not None:
                query["status"] = "completed" if completed else "not completed"

            tasks = MongoTask.objects(**query)
            return json.loads(tasks.to_json())
    except DoesNotExist:
        if task_id:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"error": "No tasks found"}
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@tasks_api.put('/{task_id}', tags=["Task"])
async def update_task(task_id: str, task: Task):
    try:
        existing_task = MongoTask.objects.get(task_id=task_id)
        task_dict = task.model_dump()
        task_dict['updated_at'] = datetime.utcnow()
        existing_task.update(**task_dict)
        existing_task.reload()
        return json.loads(existing_task.to_json())
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        logger.error(f"Error updating task by ID: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@tasks_api.delete('/{task_id}', tags=["Task"])
async def delete_task(task_id: str):
    try:
        task = MongoTask.objects.get(task_id=task_id)
        task.delete()
        return {"status": "success"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        logger.error(f"Error deleting task by ID: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@tasks_api.put('/{task_id}/status', tags=["Task"])
async def mark_task_status(task_id: int, status: dict):
    if "status" not in status:
        raise HTTPException(status_code=400, detail="Missing 'status' field in the request body")

    status_value = status["status"]
    if not isinstance(status_value, bool):
        raise HTTPException(status_code=400, detail="Invalid 'status' value, it should be a boolean (true or false)")

    try:
        task = MongoTask.objects.get(task_id=task_id)
        task.status = status_value
        task.updated_at = datetime.utcnow()
        task.save()
        return json.loads(task.to_json())
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        logger.error(f"Error updating task status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
