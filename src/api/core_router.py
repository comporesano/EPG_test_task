from typing import Annotated, List

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from copy import copy

from schemas.user import UserCreateScheme, UserUnitListResponseScheme
from services import UserOperatingService, user_operating_service
from utils import haversine
from schemas import UserListRequestScheme


router = APIRouter(tags=["Core API router for core operations"])


@router.get("/", include_in_schema=False)
async def main_redirect():
    return RedirectResponse(url='/docs', status_code=307)


@router.get("/api/list")
async def get_clients_list(
    uos: Annotated[UserOperatingService, Depends(user_operating_service)],
    request: UserListRequestScheme = Depends()
) -> list[list, UserUnitListResponseScheme] | list[UserUnitListResponseScheme]:
    print(request)
    result = await uos.get()
    result = result.scalars().all()
    u_lat = request.distance_filter_lat
    u_long = request.distance_filter_long
    if request.sortion_field:
        result = sorted(result, 
                            key=lambda user: getattr(user, request.sortion_field), 
                            reverse=not request.sortion_filter)
    if request.distance_filter:
        dist_res = []
        distances = {}
        for user in result:
            dist = haversine(point1=(u_lat, u_long), point2=(user.latitude, user.longitude))
            if dist < request.distance_filter:
                dist_res.append(user)
                distances[user.id] = dist
        result = copy(dist_res)
        result.append(distances )
    return [UserUnitListResponseScheme(**user.__dict__) for user in result]