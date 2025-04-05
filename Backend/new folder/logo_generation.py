# from diffusers import DiffusionPipeline
# import torch

# torch.cuda.empty_cache()

# pipe = DiffusionPipeline.from_pretrained(
#     "black-forest-labs/FLUX.1-dev",
#     torch_dtype=torch.float16,
#     use_safetensors=True
# ).to("cuda")

# pipe.load_lora_weights("Shakker-Labs/FLUX.1-dev-LoRA-Logo-Design")

# pipe.enable_attention_slicing()
# pipe.enable_vae_tiling()

# prompt = 'logo,Minimalist,A man stands in front of a door,his shadow forming the word "A"'

# image = pipe(prompt, num_inference_steps=25).images[0]
# image.save("logo_output.png")
# image.show()
from diffusers import StableDiffusionPipeline
import torch

model = "runwayml/stable-diffusion-v1-5"
lora = "nerijs/pokemon-lora"  # Example LoRA that works with v1.5

pipe = StableDiffusionPipeline.from_pretrained(
    model,
    torch_dtype=torch.float16,
    safety_checker=None
).to("cuda")

# Enable low memory mode
pipe.enable_attention_slicing()
pipe.enable_vae_tiling()

# Load LoRA adapter
pipe.load_lora_weights(lora)

prompt = "A logo of a futuristic fox, minimal, vector style"
image = pipe(prompt, num_inference_steps=25).images[0]
image.save("light_logo.png")

