import argparse, datetime, random, time
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

def iso_date_time():
    return datetime.datetime.now().isoformat()


def skip_safety_checker(images, *args, **kwargs):
    return images, False


class ModelRun(BaseModel):
    prompt: str

@app.post("/")
async def root(model_run: ModelRun):
    prompt = model_run.prompt
    samples = 1
    iters = 1 
    height = 500
    width = 500 
    steps = 50
    scale = 7.5 
    seed = 0

    prefix = prompt.replace(" ", "_")[:170]

    model_name = "CompVis/stable-diffusion-v1-4"
    half = False 
    dtype, rev = (torch.float16, "fp16") if half else (torch.float32, "main")
    device = "cuda"

    with open("token.txt") as f:
            token = f.read().replace("\n", "")

    pipe = StableDiffusionPipeline.from_pretrained(
            model_name, torch_dtype=dtype, revision=rev, use_auth_token=token
        ).to(device)
    print("load pipeline start:", iso_date_time())

    skip = False
        
    if skip:
        pipe.safety_checker = skip_safety_checker

    print("loaded models after:", iso_date_time())

    generator = torch.Generator(device=device).manual_seed(seed)
    img_name = None
    for j in range(iters):
        with autocast(device):
            images = pipe(
                [prompt] * samples,
                height=height,
                width=width,
                num_inference_steps=steps,
                guidance_scale=scale,
                generator=generator,
            )

        for i, image in enumerate(images["sample"]):
            img_name = "output/%s__steps_%d__scale_%0.2f__seed_%d__n_%d.png" % (prefix, steps, scale, seed, j * samples + i + 1)
            image.save(img_name)

    print("completed pipeline:", iso_date_time(), flush=True)

    return {"image": img_name}
