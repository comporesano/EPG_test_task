from fastapi import FastAPI

from api import all_routers

app = FastAPI(title="EPG Test Task", summary="Clients operation API")

for router in all_routers:
    app.include_router(router=router, prefix="/api")
