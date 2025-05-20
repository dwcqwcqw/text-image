import os
import torch
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from diffusers import AutoPipelineForText2Image
import uuid
from fastapi.staticfiles import StaticFiles
import pathlib

# Set GPU memory optimization flags
torch.cuda.empty_cache()
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"

# Make HF_TOKEN optional when using local models
HF_TOKEN = os.getenv("HF_TOKEN", "dummy_token")

# Load model and LoRA weights from RunPod volume
MODEL_DIR = '/workspace/flux_base'
LORA_PATH = '/workspace/flux_nsfw/flux_lustly-ai_v1.safetensors'

# Use more memory-efficient settings
pipeline = AutoPipelineForText2Image.from_pretrained(
    MODEL_DIR,
    torch_dtype=torch.float16,  # Use float16 instead of bfloat16 for better compatibility
    device_map="balanced",      # Changed from "auto" to "balanced" as per error message
    local_files_only=True,      # Don't try to download from HF
)

# Load LoRA weights with PEFT backend
try:
    pipeline.load_lora_weights(
        LORA_PATH,
        adapter_name="v1"
    )
    pipeline.set_adapters(["v1"], adapter_weights=[1])
except ValueError as e:
    if "PEFT backend is required" in str(e):
        print("Error: Please install PEFT with 'pip install peft>=0.6.0'")
        raise
    else:
        raise

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 简化静态文件服务配置
frontend_path = pathlib.Path(__file__).parent / "static"
if frontend_path.exists() and frontend_path.is_dir():
    print(f"Frontend path exists: {frontend_path}")
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")
else:
    print(f"Frontend path does not exist: {frontend_path}")
    @app.get("/")
    def read_root():
        return {"message": "API is running"}

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
    
    # Generate image with memory-optimized settings
    try:
        # Clear CUDA cache before generation
        torch.cuda.empty_cache()
        
        out = pipeline(
            prompt=prompt,
            guidance_scale=4,
            height=512,  # Reduced from 768 to save memory
            width=512,   # Reduced from 768 to save memory
            num_inference_steps=15,  # Reduced from 20 to save memory
        ).images[0]
        
        # Save to temp file
        filename = f"output_{uuid.uuid4().hex}.png"
        out.save(filename)
        return FileResponse(filename, media_type="image/png", filename="output.png")
    except RuntimeError as e:
        if "out of memory" in str(e):
            return JSONResponse({"error": "GPU out of memory. Try with a smaller image size or simpler prompt."}, status_code=500)
        else:
            raise
