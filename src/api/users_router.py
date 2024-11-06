from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from sqlalchemy.exc import IntegrityError

from schemas import UserCreateResponseScheme, UserCreateScheme, MatchCreateScheme
from services import UserOperatingService, user_operating_service, MatchOperatingService, match_service
from utils import watermark_put


router = APIRouter(prefix="/clients", tags=["Enpoints for clients operating"])

@router.post("/create")
async def create_user(
    uos: Annotated[UserOperatingService, Depends(user_operating_service)],
    avatar: UploadFile = File(...),
    request: UserCreateScheme = Depends()
) -> UserCreateResponseScheme:

    try:
        avatar_data = await avatar.read()
        wmarked_image = await watermark_put(avatar_data,
                                            "EPG API",
                                            (3, 8, 12),
                                            'Pillow/Tests/fonts/FreeMono.ttf',
                                            128,
                                            (0, 0))
        result = await uos.add_one({
            **request.__dict__, 
            "avatar": wmarked_image}
        )
        
        return UserCreateResponseScheme(id=result.scalar_one())
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f"User with e-mail {request.e_mail} already exist!")

    
@router.post("/{matcher_id}/match")
async def match_user(
    ms: Annotated[MatchOperatingService, Depends(match_service)],
    request: MatchCreateScheme = Depends()
):
    try:
        await ms.add_one(request.__dict__)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: <{str(e)}> during matching other user")
