import os
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import torch
from diffusers import AutoPipelineForText2Image
import uuid
from fastapi.staticfiles import StaticFiles
import pathlib

# Read Hugging Face token from environment variable
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN environment variable not set.")

# Load model and LoRA weights from RunPod volume
MODEL_DIR = '/workspace/flux_base'
LORA_PATH = '/workspace/flux_nsfw/flux_lustly-ai_v1.safetensors'

pipeline = AutoPipelineForText2Image.from_pretrained(
    MODEL_DIR,
    torch_dtype=torch.bfloat16,
)
pipeline.to("cuda")
pipeline.load_lora_weights(
    LORA_PATH,
    adapter_name="v1"
)
pipeline.set_adapters(["v1"], adapter_weights=[1])

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
frontend_path = pathlib.Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_index():
    index_file = frontend_path / "index.html"
    return FileResponse(index_file)

class GenerateRequest(BaseModel):
    gender: Optional[str] = None
    age: Optional[str] = None
    style: Optional[str] = None
    clothing: Optional[str] = None
    pose: Optional[str] = None
    background: Optional[str] = None
    art_style: Optional[str] = None
    free_prompt: Optional[str] = None

@app.post("/generate")
async def generate_image(req: GenerateRequest):
    # Compose prompt from fields
    prompt_parts = []
    if req.gender: prompt_parts.append(req.gender)
    if req.age: prompt_parts.append(req.age)
    if req.style: prompt_parts.append(req.style)
    if req.clothing: prompt_parts.append(req.clothing)
    if req.pose: prompt_parts.append(req.pose)
    if req.background: prompt_parts.append(req.background)
    if req.art_style: prompt_parts.append(req.art_style)
    if req.free_prompt: prompt_parts.append(req.free_prompt)
    prompt = ", ".join([p for p in prompt_parts if p])
    if not prompt:
        return JSONResponse({"error": "Prompt is empty."}, status_code=400)
    # Generate image
    out = pipeline(
        prompt=prompt,
        guidance_scale=4,
        height=768,
        width=768,
        num_inference_steps=20,
    ).images[0]
    # Save to temp file
    filename = f"output_{uuid.uuid4().hex}.png"
    out.save(filename)
    return FileResponse(filename, media_type="image/png", filename="output.png") 