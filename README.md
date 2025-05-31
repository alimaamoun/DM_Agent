# Content Automation System (Open Source)

An open-source alternative to expensive SaaS content creation tools, leveraging local AI models for automated social media content generation, image creation, and publishing.

## 🎯 Project Overview

This system replaces expensive subscriptions to Leonardo.AI, Canva, and Later.com with:
- **Local Image Generation**: Stable Diffusion 3 Medium via Hugging Face
- **Design Automation**: Python-based templating with Pillow/HTML
- **Content Generation**: Ollama models (Llama 3, Mistral)
- **Publishing**: Self-hosted n8n workflows + platform APIs

## 🛠 Hardware Requirements

**Minimum** (Developer 2 setup):
- GPU: RTX 2070 SUPER (8GB VRAM) or equivalent
- CPU: Ryzen 9 3900X or similar
- RAM: 32GB
- Storage: 50GB free (for models)

## 🏗 Architecture

```
content-automation/
├── core/                    # Shared utilities
│   ├── settings.py         # Configuration management
│   ├── models.py           # Model interfaces
│   └── storage.py          # Asset management
├── image_gen/              # Developer 2: Image generation
│   ├── generator.py        # SD3 pipeline
│   ├── prompt_enhancer.py  # Prompt engineering
│   └── templates/          # Design templates
├── design/                 # Developer 2: Design automation
│   ├── compositor.py       # Layout engine
│   ├── brand.py           # Brand consistency
│   └── assets/            # Logos, fonts, etc.
├── publishing/             # Developer 2: Publishing system
│   ├── scheduler.py        # Content scheduling
│   ├── platforms/         # Platform integrations
│   └── workflows/         # n8n configurations
├── content/                # Developer 1: Content pipeline
│   ├── planner.py         # Content calendar
│   ├── generator.py       # Text generation
│   └── reviewer.py        # Approval system
└── integration/            # Sunday: System integration
    ├── api.py             # Internal APIs
    ├── orchestrator.py    # Main workflow
    └── testing/           # End-to-end tests
```

## 📅 Development Timeline (Thursday-Sunday)

### Developer 2 (Visual & Publishing) - You
- **Thursday**: Environment setup, model downloads, API testing
- **Friday**: Image generation system, prompt engineering
- **Saturday**: Design automation, caption generation
- **Sunday**: Integration with content pipeline

## 🚀 Quick Start

### Prerequisites
```bash
# WSL Ubuntu environment
sudo apt update
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11 python3.11-venv build-essential git
```

### Setup
```bash
# Clone and setup environment
git clone <repo-url>
cd content-automation
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download models
python scripts/download_models.py
```

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:
```env
OLLAMA_HOST=http://localhost:11434
HUGGINGFACE_TOKEN=your_token_here
GOOGLE_DRIVE_CREDENTIALS=path/to/creds.json
PLATFORM_APIS=configured_separately
```

## 📋 Daily Tasks

### Thursday (Environment Bootstrap)
- [ ] Python environment setup
- [ ] Hugging Face model download (SD3 Medium)
- [ ] Ollama model installation
- [ ] Basic image generation test

### Friday (Core Image Pipeline)
- [ ] Image generation system
- [ ] Prompt enhancement logic
- [ ] Google Drive integration
- [ ] Asset management

### Saturday (Design & Content)
- [ ] Design templating system
- [ ] Caption/hashtag generator
- [ ] Brand consistency tools
- [ ] Publishing pipeline

### Sunday (Integration)
- [ ] API integration with content system
- [ ] End-to-end workflow testing
- [ ] Performance optimization
- [ ] Documentation completion

## 🤝 Contributing

This is a two-developer sprint project. See individual task assignments in the project board.

## 📄 License

MIT License - see LICENSE file for details.

## 🎨 Models Used

- **Image Generation**: Stable Diffusion 3 Medium (Stability AI Community License)
- **Prompt Enhancement**: stable-diffusion-prompt-generator
- **Text Generation**: Llama 3 8B, Mistral 7B
- **Embeddings**: nomic-embed-text

## 🔗 Links

- [Hugging Face Models](https://huggingface.co/stabilityai/stable-diffusion-3-medium)
- [Ollama](https://ollama.ai/)
- [n8n Self-hosted](https://n8n.io/) 