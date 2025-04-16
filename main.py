from typing import Union
from pydantic import BaseModel, Field
from fastapi import FastAPI, status, Response
from fastapi.responses import HTMLResponse

app = FastAPI()
SYSTEMS_FAILURE = {
  "navigation": "NAV-01",
  "communications": "COM-02",
  "life_support": "LIFE-03",
  "engines": "ENG-04",
  "deflector_shield": "SHLD-05"
}
DEFECT = "deflector_shield"

class StatusResponse(BaseModel):
    damaged_system: str = Field(default="<pick one of the systems>", title="damaged system")
    

@app.get("/status", status_code=status.HTTP_200_OK)
def get_status() -> StatusResponse:
    return {"damaged_system": DEFECT}


@app.get("/repair-bay", status_code=status.HTTP_200_OK)
def repair_bay():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
    <div class="anchor-point">{SYSTEMS_FAILURE.get(DEFECT)}</div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/teapot", status_code=status.HTTP_418_IM_A_TEAPOT)
def iam_teapot():
    return Response(status_code=status.HTTP_418_IM_A_TEAPOT)
