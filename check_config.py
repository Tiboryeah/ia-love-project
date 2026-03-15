import requests

# First check model info
r = requests.get("http://127.0.0.1:7860/sdapi/v1/memory")
if r.ok:
    print("Memory:", r.json())

r2 = requests.get("http://127.0.0.1:7860/sdapi/v1/options")
if r2.ok:
    opts = r2.json()
    print("Offload mode:", opts.get("diffusers_offload_mode"))
    print("Generator device:", opts.get("diffusers_generator_device"))
    print("No half:", opts.get("no_half"))
    print("No half vae:", opts.get("no_half_vae"))
