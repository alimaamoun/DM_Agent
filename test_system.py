#!/usr/bin/env python3
"""
Test script for the Content Automation System
Tests GPU, Ollama connectivity, and image generation
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from core.settings import settings, get_device
from image_gen.generator import ImageGenerator


async def test_environment():
    """Test basic environment setup"""
    print("🔍 Testing Environment Setup...")
    
    # Test PyTorch and CUDA
    import torch
    print(f"✅ PyTorch version: {torch.__version__}")
    print(f"✅ CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"✅ CUDA device: {torch.cuda.get_device_name()}")
        print(f"✅ CUDA memory: {torch.cuda.get_device_properties(0).total_memory // 1024**3} GB")
    
    # Test device detection
    device = get_device()
    print(f"✅ Selected device: {device}")
    
    # Test directory creation
    print(f"✅ Output directory: {settings.output_path}")
    print(f"✅ Assets directory: {settings.local_asset_path}")
    print(f"✅ Temp directory: {settings.temp_path}")
    
    return True


async def test_ollama():
    """Test Ollama connectivity and model availability"""
    print("\n🔍 Testing Ollama Connection...")
    
    try:
        import ollama
        client = ollama.Client(host=settings.ollama_host)
        
        # Test connection
        models = client.list()
        print(f"✅ Connected to Ollama at {settings.ollama_host}")
        print(f"✅ Available models: {len(models['models'])}")
        
        # Check for required models
        model_names = [model.model for model in models.models]
        required_models = [settings.caption_model, settings.text_model]
        
        for model in required_models:
            if model in model_names:
                print(f"✅ Model available: {model}")
            else:
                print(f"⚠️  Model missing: {model}")
                print(f"   Run: ollama pull {model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("   Make sure Ollama is running: ollama serve")
        return False


async def test_image_generation():
    """Test basic image generation"""
    print("\n🔍 Testing Image Generation...")
    
    try:
        generator = ImageGenerator()
        
        # Test without model loading first (dry run)
        print("📋 Generator initialized")
        print(f"📋 Device: {generator.device}")
        
        # Generate a simple test image
        test_prompt = "a cute robot painting on a canvas, digital art"
        print(f"🎨 Test prompt: {test_prompt}")
        
        result = await generator.generate(
            prompt=test_prompt,
            size="512x512",  # Smaller size for faster testing
            steps=20,        # Fewer steps for faster testing
            enhance_prompt=False  # Skip enhancement for basic test
        )
        
        print(f"✅ Image generated successfully!")
        print(f"✅ File: {result['image_path']}")
        print(f"✅ Generation time: {result['generation_time']:.2f}s")
        print(f"✅ Size: {result['size']}")
        
        # Verify file exists
        if Path(result['image_path']).exists():
            print(f"✅ File saved successfully")
        else:
            print(f"❌ File not found at {result['image_path']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Image generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_prompt_enhancement():
    """Test prompt enhancement with Ollama"""
    print("\n🔍 Testing Prompt Enhancement...")
    
    try:
        generator = ImageGenerator()
        
        basic_prompt = "a coffee shop"
        enhanced = await generator.enhance_prompt(basic_prompt, "cozy and warm")
        
        print(f"📝 Original: {basic_prompt}")
        print(f"📝 Enhanced: {enhanced}")
        
        if len(enhanced) > len(basic_prompt):
            print("✅ Prompt enhancement working")
            return True
        else:
            print("⚠️ Prompt enhancement may not be working properly")
            return False
            
    except Exception as e:
        print(f"❌ Prompt enhancement failed: {e}")
        return False


async def run_full_test():
    """Run a complete end-to-end test"""
    print("\n🚀 Running Full End-to-End Test...")
    
    try:
        generator = ImageGenerator()
        
        # Test complete workflow
        result = await generator.generate(
            prompt="modern office workspace",
            style="professional photography",
            size="1024x1024",
            steps=30,
            enhance_prompt=True
        )
        
        print(f"🎉 Full test completed!")
        print(f"🖼️  Final image: {result['image_path']}")
        print(f"⏱️  Total time: {result['generation_time']:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Full test failed: {e}")
        return False


async def main():
    """Main test runner"""
    print("🧪 Content Automation System - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Ollama", test_ollama),
        ("Basic Image Generation", test_image_generation),
        ("Prompt Enhancement", test_prompt_enhancement),
        ("Full End-to-End", run_full_test),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = await test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*20} TEST SUMMARY {'='*20}")
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready!")
    else:
        print("⚠️ Some tests failed. Check the output above.")
    
    return passed == total


if __name__ == "__main__":
    asyncio.run(main()) 