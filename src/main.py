from fastapi import FastAPI

from api import all_routers

app = FastAPI(title="EPG Test Task", 
              summary="Clients operation API",
              redoc_url=None)

for router in all_routers:
    app.include_router(router=router, prefix="")
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8081)