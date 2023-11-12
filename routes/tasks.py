from bson import ObjectId
from fastapi import APIRouter, HTTPException
from models.request.task import Task
from models.mongo.task import MongoTask
from datetime import datetime
import json
from typing import Optional
from mongoengine.errors import DoesNotExist
from fastapi import Body

tasks_api = APIRouter(prefix='/tasks')


@tasks_api.post('', tags=["Task"])
async def create_task(task: Task):
    try:
        task_dict = task.model_dump()
        task_dict['created_at'] = datetime.utcnow()
        task_dict['updated_at'] = datetime.utcnow()
        mongo_task = MongoTask(**task_dict)
        mongo_task.save()

        log_entry = {
            "timestamp": datetime.utcnow(),
            "method": "POST",
            "url": tasks_api.url_path_for("create_task"),
        }
        print(log_entry)

        return json.loads(mongo_task.to_json())
    except Exception as e:
        print(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@tasks_api.get('', tags=["Task"])
async def get_tasks(task_id: Optional[str] = None, status: Optional[bool] = None):
    try:
        if task_id:
            task = MongoTask.objects.get(id=ObjectId(task_id))
            return json.loads(task.to_json())
        else:
            query = {}

            if status is not None:
                query["status"] = status

            tasks = MongoTask.objects(**query)
            log_entry = {
                "timestamp": datetime.utcnow(),
                "method": "GET",
                "url": tasks_api.url_path_for("get_tasks"),
            }
            print(log_entry)
            return json.loads(tasks.to_json())

    except DoesNotExist:
        if task_id:
            raise HTTPException(status_code=404, detail="Task not found")
        print({"error": "No tasks found"})
        return {"error": "No tasks found"}
    except Exception as e:
        print(f"Error retrieving tasks: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@tasks_api.put('', tags=["Task"])
async def update_task(task_id: str, task: Task):
    try:
        existing_task = MongoTask.objects.get(id=ObjectId(task_id))
        task_dict = {key: value for key,
                     value in task.model_dump().items() if key != 'created_at'}
        task_dict['updated_at'] = datetime.utcnow()
        existing_task.update(**task_dict)
        existing_task.reload()
        log_entry = {
            "timestamp": datetime.utcnow(),
            "method": "PUT",
            "url": tasks_api.url_path_for("update_task"),
        }
        print(log_entry)
        return json.loads(existing_task.to_json())
    except DoesNotExist:
        print({"error": "No tasks found"})
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        print(f"Error updating task by ID: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@tasks_api.delete('', tags=["Task"])
async def delete_task(task_id: str):
    try:
        task = MongoTask.objects.get(id=ObjectId(task_id))
        task.delete()
        log_entry = {
            "timestamp": datetime.utcnow(),
            "method": "DELETE",
            "url": tasks_api.url_path_for("delete_task"),
        }
        print(log_entry)
        return {"status": "success"}
    except DoesNotExist:
        print({"error": "No tasks found"})
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        print(f"Error deleting task by ID: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@tasks_api.put('/status', tags=["Task"])
async def mark_task_status(task_id: str, status: bool):

    try:
        task = MongoTask.objects.get(id=ObjectId(task_id))
        task.status = status
        task.updated_at = datetime.utcnow()
        task.save()
        log_entry = {
            "timestamp": datetime.utcnow(),
            "method": "PUT",
            "url": tasks_api.url_path_for("mark_task_status"),
        }
        print(log_entry)
        return json.loads(task.to_json())
    except DoesNotExist:
        print({"error": "No tasks found"})
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        print(f"Error updating task status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
