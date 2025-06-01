"""
Image Generation Module using Stable Diffusion 3 Medium
Optimized for RTX 2070 SUPER (8GB VRAM)
"""

import asyncio
import time
import torch
from pathlib import Path
from typing import Optional, Dict, Any
from PIL import Image
import ollama

from diffusers import StableDiffusion3Pipeline
from core.settings import settings, get_device, get_image_size_tuple


class ImageGenerator:
    """Handles image generation using Stable Diffusion 3 Medium"""
    
    def __init__(self):
        self.pipeline = None
        self.device = get_device()
        self.ollama_client = ollama.Client(host=settings.ollama_host)
        
    def load_model(self):
        """Load SD3 Medium pipeline with memory optimizations"""
        if self.pipeline is not None:
            return
            
        print(f"Loading Stable Diffusion 3 Medium on {self.device}...")
        
        # Load with memory optimizations for 8GB VRAM
        self.pipeline = StableDiffusion3Pipeline.from_pretrained(
            settings.sd3_model_path,
            torch_dtype=torch.float16,  # Half precision for memory efficiency
            use_safetensors=True,
            variant="fp16"
        )
        
        # Memory optimizations
        self.pipeline.enable_model_cpu_offload()  # Offload to CPU when not in use
        self.pipeline.enable_vae_slicing()        # Process VAE in slices
        self.pipeline.enable_attention_slicing()  # Reduce memory for attention
        
        # Move to GPU
        self.pipeline = self.pipeline.to(self.device)
        
        print(f"✅ Model loaded on {self.device}")
    
    async def enhance_prompt(self, basic_prompt: str, style_preference: str = None) -> str:
        """Enhance a basic prompt using Ollama's prompt generator"""
        try:
            # Build enhancement prompt
            enhancement_request = f"""Transform this basic description into a detailed, artistic prompt for Stable Diffusion:
            
Basic idea: {basic_prompt}
Style preference: {style_preference or 'creative and professional'}

Make it detailed with artistic elements, lighting, composition, and quality modifiers."""

            response = self.ollama_client.generate(
                model=settings.prompt_enhancer_model,
                prompt=enhancement_request,
                stream=False
            )
            
            enhanced = response['response'].strip()
            print(f"📝 Enhanced prompt: {enhanced}")
            return enhanced
            
        except Exception as e:
            print(f"⚠️ Prompt enhancement failed: {e}")
            # Fallback to basic prompt with some enhancements
            return f"{basic_prompt}, high quality, detailed, professional photography"
    
    async def generate(
        self, 
        prompt: str,
        style: Optional[str] = None,
        size: str = "1024x1024",
        steps: int = 30,
        guidance_scale: float = 7.0,
        enhance_prompt: bool = True
    ) -> Dict[str, Any]:
        """Generate an image from a text prompt"""
        
        # Load model if not already loaded
        self.load_model()
        
        # Enhance the prompt if requested
        if enhance_prompt:
            prompt = await self.enhance_prompt(prompt, style)
        elif style:
            prompt = f"{prompt}, {style} style"
        
        # Parse size
        width, height = get_image_size_tuple(size)
        
        # Generate image
        print(f"🎨 Generating {width}x{height} image...")
        print(f"📋 Prompt: {prompt}")
        
        start_time = time.time()
        
        # Generate with error handling
        try:
            with torch.autocast(self.device):
                image = self.pipeline(
                    prompt=prompt,
                    width=width,
                    height=height,
                    num_inference_steps=steps,
                    guidance_scale=guidance_scale,
                    num_images_per_prompt=1,
                ).images[0]
            
            generation_time = time.time() - start_time
            
            # Save image
            timestamp = int(time.time())
            filename = f"generated_{timestamp}_{width}x{height}.png"
            image_path = settings.output_path / filename
            image.save(image_path)
            
            print(f"✅ Generated in {generation_time:.2f}s: {image_path}")
            
            # Convert to bytes for MCP
            import io
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            return {
                "image_path": str(image_path),
                "image_data": img_bytes.getvalue(),
                "prompt": prompt,
                "size": f"{width}x{height}",
                "generation_time": generation_time,
                "steps": steps,
                "guidance_scale": guidance_scale
            }
            
        except torch.cuda.OutOfMemoryError:
            # Handle VRAM overflow
            torch.cuda.empty_cache()
            print("⚠️ CUDA out of memory. Try reducing image size or steps.")
            raise
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            raise
    
    async def generate_batch(self, prompts: list[str], **kwargs) -> list[Dict[str, Any]]:
        """Generate multiple images in sequence"""
        results = []
        for i, prompt in enumerate(prompts):
            print(f"\n🔄 Generating image {i+1}/{len(prompts)}")
            result = await self.generate(prompt, **kwargs)
            results.append(result)
            
            # Clear cache between generations
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        
        return results
    
    def unload_model(self):
        """Free up VRAM by unloading the model"""
        if self.pipeline is not None:
            del self.pipeline
            self.pipeline = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            print("🗑️ Model unloaded from memory") 