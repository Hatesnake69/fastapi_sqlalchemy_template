from fastapi.routing import APIRouter

import api.endpoints as endpoints

api_router = APIRouter()


for name, entity in endpoints.__dict__.items():
    if not name.startswith("__"):
        api_router.include_router(router=getattr(entity, "router"))
