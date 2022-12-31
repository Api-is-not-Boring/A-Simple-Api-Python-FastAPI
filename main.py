from os import getenv
import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app",
        host=getenv("ADDRESS"),
        port=int(getenv("PORT")),
        headers=[("server", "FastAPI")],
        reload=True
    )
