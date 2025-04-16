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
    critical_pressure = 10.0  # MPa
    critical_temperature = 500.0  # °C at 10 MPa
    specific_volume_liquid_critical = 0.0035  # m³/kg
    specific_volume_vapor_critical = 0.0035  # m³/kg

    normal_pressure = 0.05  # MPa
    normal_temperature = 30.0  # °C
    specific_volume_liquid_normal = 0.00105  # m³/kg
    specific_volume_vapor_normal = 30.0  # m³/kg

    def linear_interpolate(x, x1, y1, x2, y2):
        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

    if pressure < normal_pressure:
        temperature = normal_temperature
    elif pressure > critical_pressure:
        temperature = critical_temperature
    else:
        temperature = linear_interpolate(
            pressure,
            normal_pressure,
            normal_temperature,
            critical_pressure,
            critical_temperature,
        )

    if pressure < normal_pressure:
        specific_volume_liquid = specific_volume_liquid_normal
    elif pressure > critical_pressure:
        specific_volume_liquid = specific_volume_liquid_critical
    else:
        specific_volume_liquid = linear_interpolate(
            pressure,
            normal_pressure,
            specific_volume_liquid_normal,
            critical_pressure,
            specific_volume_liquid_critical,
        )

    if pressure < normal_pressure:
        specific_volume_vapor = specific_volume_vapor_normal
    elif pressure > critical_pressure:
        specific_volume_vapor = specific_volume_vapor_critical
    else:
        specific_volume_vapor = linear_interpolate(
            pressure,
            normal_pressure,
            specific_volume_vapor_normal,
            critical_pressure,
            specific_volume_vapor_critical,
        )

    alert_wall_e = temperature > 30.0
    wall_e_message = (
        "Alert Wall-E! Temperature is above 30°C. Hurry!"
        if alert_wall_e
        else "Temperature is safe, don't worry Wall-E."
    )

    return {
        "specific_volume_liquid": specific_volume_liquid,
        "specific_volume_vapor": specific_volume_vapor,
        "temperature": temperature,
        "wall_e_alert": alert_wall_e,
        "message": wall_e_message,
    }