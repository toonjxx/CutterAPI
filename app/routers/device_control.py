from fastapi import APIRouter
from internal.serial_communication import write_device

router = APIRouter()

@router.post("/device/send-command/")
async def send_command(command: str):
    result = write_device(command)
    return {"result": result}