from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from uuid import uuid4


from app.services.database import init_db


import asyncio
from app.services.database import get_db
from app.services.analysis import analyze_data

analysis_results = {}  # Store the latest analysis results in memory


async def periodic_analysis():
    while True:
        db = next(get_db())  # Use the generator to get the database session
        try:
            global analysis_results
            analysis_results = analyze_data(db)
        finally:
            db.close()  # Ensure the database session is closed
        await asyncio.sleep(60)  # Run every 60 seconds


# Initialize the database
init_db()

# Initialize the FastAPI app
app = FastAPI(
    title="CogniForm",
    description="An interactive cognitive science survey platform.",
    version="0.1.0",
)

# Serve static files (e.g., CSS)
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# In-memory session store
active_sessions = {}


# Middleware to check authentication
def get_session(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in active_sessions:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return session_id


from app.models.user import User


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_analysis())


@app.get("/")
async def home(request: Request):
    # Create a new session if not already present
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in active_sessions:
        session_id = str(uuid4())
        active_sessions[session_id] = User(session_id)
        response = templates.TemplateResponse("static/home.html", {"request": request})
        response.set_cookie(key="session_id", value=session_id)
        print(f"Set-Cookie: session_id={session_id}")  # Debug
        return response
    return templates.TemplateResponse("static/home.html", {"request": request})


@app.post("/delay_discounting")
async def submit_delay_discounting(
    request: Request, session_id: str = Depends(get_session)
):
    form_data = await request.form()
    choice = form_data.get("choice")
    response_time = float(form_data.get("response_time"))
    user = active_sessions[session_id]

    # Store the response
    user.add_delay_discounting_response(choice=choice, response_time=response_time)

    # Redirect to the results page
    return RedirectResponse("/my_result", status_code=303)


from app.services.database import save_user_responses


@app.get("/my_result")
async def my_result(request: Request, session_id: str = Depends(get_session)):
    user = active_sessions[session_id]
    results = user.get_results()
    print(user)
    print(user.get_results())
    print(results)

    # Save all responses in the database
    db = next(get_db())
    try:
        save_user_responses(db, session_id, results)
    finally:
        db.close()

    return templates.TemplateResponse(
        "static/my_result.html", {"request": request, "results": results}
    )


# @app.get("/results")
# async def results(request: Request, session_id: str = Depends(get_session)):
#     # Retrieve results for the current session
#     user_data = active_sessions.get(session_id, {})
#     results = user_data.get("results", {})
#     return templates.TemplateResponse(
#         "static/results.html", {"request": request, "results": results}
#     )


@app.get("/results")
async def results(request: Request):
    global analysis_results
    if "demographics" not in analysis_results:
        analysis_results["demographics"] = {
            "average_age": None,
            "education_distribution": {},
            "familiarity_distribution": {},
        }
    if "crt" not in analysis_results:
        analysis_results["crt"] = {
            "average_response_time": None,
            "accuracy": None,
        }
    if "delay_discounting" not in analysis_results:
        analysis_results["delay_discounting"] = {
            "average_response_time": None,
            "choice_distribution": {},
        }
    return templates.TemplateResponse(
        "static/results.html", {"request": request, "results": analysis_results}
    )


@app.get("/demographics")
async def demographics(request: Request, session_id: str = Depends(get_session)):
    return templates.TemplateResponse("static/demographics.html", {"request": request})


# @app.get("/crt")
# async def crt(request: Request, session_id: str = Depends(get_session)):
#     return templates.TemplateResponse("static/crt.html", {"request": request})


@app.get("/delay_discounting")
async def delay_discounting(request: Request, session_id: str = Depends(get_session)):
    return templates.TemplateResponse(
        "static/delay_discounting.html", {"request": request}
    )


@app.get("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id in active_sessions:
        del active_sessions[session_id]
    response = RedirectResponse("/")
    response.delete_cookie("session_id")
    return response


@app.post("/demographics")
async def submit_demographics(request: Request, session_id: str = Depends(get_session)):
    form_data = await request.form()
    user = active_sessions[session_id]

    # Add demographics data
    user.add_demographics(
        age=int(form_data.get("age")),
        education=form_data.get("education"),
        familiarity=form_data.get("familiarity"),
    )
    return RedirectResponse("/crt", status_code=303)


from app.tasks.crt import CognitiveReflectionTest

crt_task = CognitiveReflectionTest()


@app.get("/crt")
async def crt(request: Request, session_id: str = Depends(get_session)):
    # Get the first unanswered question
    current_index = len(active_sessions[session_id].get_results().get("crt", []))
    question = crt_task.get_question(current_index)
    if not question:
        # Redirect to results if all questions are answered
        return RedirectResponse("/results", status_code=303)
    return templates.TemplateResponse(
        "static/crt.html",
        {"request": request, "question": question, "index": current_index},
    )


@app.post("/crt")
async def submit_crt(request: Request, session_id: str = Depends(get_session)):
    form_data = await request.form()
    user_answer = float(form_data.get("answer"))
    response_time = float(form_data.get("response_time"))
    question_index = int(form_data.get("index"))
    user = active_sessions[session_id]

    # Validate and store the response
    question = crt_task.questions[question_index]
    is_correct = user_answer == question["answer"]
    user.add_crt_response(
        question=question["question"],
        user_answer=user_answer,
        is_correct=is_correct,
        response_time=response_time,
    )

    # Redirect to the next question or results
    next_question = crt_task.get_question(question_index + 1)
    if next_question:
        return RedirectResponse("/crt", status_code=303)
    return RedirectResponse("/delay_discounting", status_code=303)

    # # Redirect to the next question or results
    # next_question = crt_task.get_question(question_index + 1)
    # if next_question:
    #     return RedirectResponse("/crt", status_code=303)
    # return RedirectResponse("/delay_discounting", status_code=303)
