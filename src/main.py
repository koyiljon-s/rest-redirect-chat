# -*- coding: utf-8 -*-
import os
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI

from api.router import router


app = FastAPI(title="Rest Redirect Chat API")

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)