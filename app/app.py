import os

from fastapi import FastAPI

from app.router import v1

app = FastAPI(debug=True,
              title=os.getenv("NAME"),
              version=os.getenv("VERSION"),
              description=os.getenv("DESCRIPTION")
              )

app.include_router(v1.router)
