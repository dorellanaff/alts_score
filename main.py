from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Datos aproximados de saturación (basados en el diagrama)
phase_data = {
    0.05: {"specific_volume_liquid": 0.00105, "specific_volume_vapor": 30.0},
    1:    {"specific_volume_liquid": 0.0012,  "specific_volume_vapor": 0.1},
    5:    {"specific_volume_liquid": 0.0015,  "specific_volume_vapor": 0.01},
    10:   {"specific_volume_liquid": 0.0035,  "specific_volume_vapor": 0.0035},  # Punto crítico
}

class PhaseChangeResponse(BaseModel):
    specific_volume_liquid: float
    specific_volume_vapor: float

@app.get("/phase-change-diagram", response_model=PhaseChangeResponse)
def get_phase_data(pressure: float = Query(..., gt=0)):
    if pressure < 0.05:
        raise HTTPException(status_code=400, detail="Pressure too low. Data only available for T > 30°C.")

    if pressure in phase_data:
        return phase_data[pressure]

    raise HTTPException(status_code=404, detail="No data available for this pressure.")
