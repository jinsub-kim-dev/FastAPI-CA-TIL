import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from containers import Container
from user.interface.controllers.user_controller import router as user_routers


app = FastAPI()

container = Container()
app.container = container

app.include_router(user_routers)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )

@app.get("/")
def hello():
    return {"Hello": "FastAPI"}

@app.on_event("startup")
async def startup_event():
    container.init_resources()
    container.wire(modules=["user.interface.controllers.user_controller"])

@app.on_event("shutdown")
async def shutdown_event():
    container.shutdown_resources()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)