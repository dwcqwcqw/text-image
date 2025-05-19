import uvicorn
from main import app

def handler(event=None, context=None):
    # This function can be used by RunPod to start the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000) 