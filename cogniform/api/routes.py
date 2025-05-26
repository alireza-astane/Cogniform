from fastapi import APIRouter, HTTPException
from app.models.demographics import Demographics
from app.models.tasks import CRTTask, StroopTask, DelayDiscountingTask
from app.services.database import save_response, get_responses
from app.tasks.crt import CognitiveReflectionTest as CRT
from app.tasks.delay_discounting import DelayDiscountingTask as DelayDiscounting

router = APIRouter()


@router.post("/demographics")
async def submit_demographics(demographics: Demographics):
    # Save demographics data
    save_response("demographics", demographics.dict())
    return {"message": "Demographics submitted successfully."}


@router.get("/task/crt")
async def get_crt_task():
    crt_task = CRT()
    return crt_task.get_task()


@router.post("/task/crt/response")
async def submit_crt_response(response: CRTTask):
    save_response("crt", response.dict())
    return {"message": "CRT response submitted successfully."}


@router.get("/task/stroop")
async def get_stroop_task():
    stroop_task = Stroop()
    return stroop_task.get_task()


@router.post("/task/stroop/response")
async def submit_stroop_response(response: StroopTask):
    save_response("stroop", response.dict())
    return {"message": "Stroop response submitted successfully."}


@router.get("/task/delay_discounting")
async def get_delay_discounting_task():
    delay_discounting_task = DelayDiscounting()
    return delay_discounting_task.get_task()


@router.post("/task/delay_discounting/response")
async def submit_delay_discounting_response(response: DelayDiscountingTask):
    save_response("delay_discounting", response.dict())
    return {"message": "Delay Discounting response submitted successfully."}


# Example route to fetch all responses
@router.get("/responses", tags=["Responses"])
async def fetch_responses():
    responses = get_responses()
    return {"responses": [response.__dict__ for response in responses]}


# Route to serve a cognitive task
@router.get("/tasks/{task_name}", tags=["Tasks"])
async def get_task(task_name: str):
    if task_name == "crt":
        return {
            "task": "Cognitive Reflection Test",
            "questions": ["Question 1", "Question 2", "Question 3"],
        }
    elif task_name == "stroop":
        return {
            "task": "Stroop Task",
            "instructions": "Select the font color of the word.",
        }
    elif task_name == "delay_discounting":
        return {
            "task": "Delay Discounting Task",
            "instructions": "Choose between smaller-sooner and larger-later rewards.",
        }
    else:
        return {"error": "Task not found"}


@router.post("/tasks/{task_name}/submit", tags=["Tasks"])
async def submit_response(task_name: str, response: dict):
    try:
        demographic_data = response.get("demographic_data", {})
        response_data = response.get("response_data", {})
        saved_response = save_response(demographic_data, task_name, response_data)
        return {
            "message": "Response saved successfully!",
            "response_id": saved_response.id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
