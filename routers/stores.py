from fastapi import APIRouter, HTTPException, Depends
from utils.db_utils import *

router = APIRouter(prefix="/api/stores")

@router.get("/{store_id}/profile")
async def get_store_profile(store_id: str):
    profile = read_record('store_profiles', conditions={'id': store_id})
    if profile is None:
        raise HTTPException(status_code=404, detail="profile not found")
    print(profile)
    return profile