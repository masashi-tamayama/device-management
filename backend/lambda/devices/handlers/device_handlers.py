import json
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Device
from ..schemas import DeviceCreate, Device as DeviceSchema
from fastapi.responses import JSONResponse
import uuid

class UnicodeJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":")
        ).encode("utf-8")

router = APIRouter()

@router.post("/devices/", response_model=DeviceSchema, status_code=201)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    """新しいデバイスを作成"""
    db_device = Device(
        id=str(uuid.uuid4()),
        name=device.name,
        manufacturer=device.manufacturer
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return UnicodeJSONResponse(
        content={
            "name": db_device.name,
            "manufacturer": db_device.manufacturer,
            "id": db_device.id,
            "created_at": db_device.created_at.isoformat(),
            "updated_at": db_device.updated_at.isoformat()
        },
        status_code=201
    )

@router.get("/devices/", response_model=List[DeviceSchema])
def list_devices(db: Session = Depends(get_db)):
    """全デバイスを取得"""
    devices = db.query(Device).all()
    return UnicodeJSONResponse(
        content=[{
            "name": device.name,
            "manufacturer": device.manufacturer,
            "id": device.id,
            "created_at": device.created_at.isoformat(),
            "updated_at": device.updated_at.isoformat()
        } for device in devices]
    )

@router.get("/devices/{device_id}", response_model=DeviceSchema)
def get_device(device_id: str, db: Session = Depends(get_db)):
    """指定されたIDのデバイスを取得"""
    device = db.query(Device).filter(Device.id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="指定されたデバイスが見つかりません")
    return UnicodeJSONResponse(
        content={
            "name": device.name,
            "manufacturer": device.manufacturer,
            "id": device.id,
            "created_at": device.created_at.isoformat(),
            "updated_at": device.updated_at.isoformat()
        }
    )

@router.put("/devices/{device_id}", response_model=DeviceSchema)
def update_device(device_id: str, device: DeviceCreate, db: Session = Depends(get_db)):
    """デバイスを更新"""
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="指定されたデバイスが見つかりません")
    
    for key, value in device.dict().items():
        setattr(db_device, key, value)
    
    db.commit()
    db.refresh(db_device)
    return UnicodeJSONResponse(
        content={
            "name": db_device.name,
            "manufacturer": db_device.manufacturer,
            "id": db_device.id,
            "created_at": db_device.created_at.isoformat(),
            "updated_at": db_device.updated_at.isoformat()
        }
    )

@router.delete("/devices/{device_id}")
def delete_device(device_id: str, db: Session = Depends(get_db)):
    """デバイスを削除"""
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="指定されたデバイスが見つかりません")
    
    db.delete(db_device)
    db.commit()
    return UnicodeJSONResponse(
        content={"message": "デバイスを削除しました", "device_id": device_id}
    ) 