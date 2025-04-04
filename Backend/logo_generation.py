from diffusers import DiffusionPipeline
import torch

torch.cuda.empty_cache()

pipe = DiffusionPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16,
    use_safetensors=True,
    device_map="balanced"  # Use "balanced" instead of "auto"
)

pipe.load_lora_weights("Shakker-Labs/FLUX.1-dev-LoRA-Logo-Design")

pipe.enable_attention_slicing()
pipe.enable_vae_tiling()

prompt = 'logo,Minimalist,A man stands in front of a door,his shadow forming the word "A"'

# Reduce inference steps to save VRAM
image = pipe(prompt, num_inference_steps=25).images[0]
image.save("logo_output.png")
image.show()
