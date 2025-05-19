# NSFW Text-to-Image Generator (RunPod Ready)

This project is a full-stack (FastAPI + React) web app for generating NSFW images of characters in various scenes, using a Hugging Face diffusion model and LoRA weights. It is optimized for deployment on RunPod with large models stored in persistent Volumes.

## Features
- User-friendly web UI for prompt selection and free text input
- Backend image generation using `diffusers` and custom LoRA
- Downloadable image output
- All-in-one Docker deployment (code + dependencies only)
- **Model and LoRA weights are loaded from RunPod Volumes, not included in the image**

## Model Storage (RunPod Volumes)
- **Base model:** `/workspace/flux_base` (e.g. FLUX.1-dev)
- **LoRA weights:** `/workspace/flux_nsfw` (e.g. Flux_Lustly.ai_Uncensored_nsfw_v1)

> Upload your model files to RunPod Volumes and mount them to `/workspace` in your Pod.

## Setup & Deployment

### 1. Build Docker Image (locally or on RunPod)
```bash
docker build -t text-image .
```

### 2. Push to Docker Hub (optional, for cloud deployment)
```bash
docker tag text-image yourdockerhub/text-image:latest
docker push yourdockerhub/text-image:latest
```

### 3. Prepare RunPod Volumes
- Create Volumes in RunPod and upload your model files:
  - `/workspace/flux_base` (base model directory)
  - `/workspace/flux_nsfw` (LoRA weights directory)
- Mount these Volumes to `/workspace` in your Pod.

### 4. Deploy on RunPod
- Use the built Docker image.
- Mount Volumes as described above.
- Expose port 8000.

### 5. Usage
- Access the web UI at `http://<your-pod-ip>:8000`
- Fill in the prompt fields and generate images.

## Security Note
- **Do NOT include large model files in your repository or Docker image.**
- Always use Volumes or cloud storage for large models.

## License
This project is for research and educational purposes only. Please comply with all applicable laws and platform policies.
