# Content Automation System Architecture

## Hybrid MCP + n8n Design

This system combines the reliability of workflow automation (n8n) with the flexibility of LLM-driven interaction (MCP).

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interfaces                              │
├─────────────────────┬───────────────────────┬───────────────────┤
│   Claude Chat       │   n8n Web UI          │   Manual Scripts  │
│   (via MCP)         │   (workflows)         │   (CLI tools)     │
└─────────────────────┴───────────────────────┴───────────────────┘
           │                      │                      │
           ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     API Layer                                   │
├─────────────────────┬───────────────────────┬───────────────────┤
│   MCP Server        │   REST API            │   Direct Imports  │
│   (mcp/server.py)   │   (FastAPI)           │   (Python)        │
└─────────────────────┴───────────────────────┴───────────────────┘
           │                      │                      │
           └──────────────────────┼──────────────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Core Modules                                │
├─────────────────────┬───────────────────┬───────────────────────┤
│   Image Generation  │   Design System   │   Publishing          │
│   🔥 PyTorch HERE   │   • Branding      │   • Scheduling        │
│   • SD3 Pipeline    │   • Templates     │   • Platform APIs     │
│   • Prompt Enhance  │   • Composition   │   • Content Calendar  │
│   • Style Transfer  │   • Composition   │   • Content Calendar  │
└─────────────────────┴───────────────────┴───────────────────────┘
```

## Use Case Examples

### 1. Scheduled Automation (n8n)
```yaml
# Daily workflow: content-generation.json
trigger: cron("0 9 * * *")  # 9 AM daily
steps:
  1. Read Google Sheets calendar
  2. Generate images for today's themes
  3. Create captions with Llama
  4. Apply brand templates
  5. Schedule posts for peak times
  6. Send summary email
```

### 2. Interactive Creation (MCP)
```
You: "Create a LinkedIn post about our new AI feature"

Claude: I'll create that for you. Let me:
1. Generate a professional image about AI features
2. Write a LinkedIn-appropriate caption
3. Apply your brand template

[calls: generate_image, create_social_post, brand_assets]

Here's your post: [shows image + caption]
Would you like me to schedule it or make any adjustments?
```

### 3. Intelligent Workflow Modification (MCP + n8n)
```
You: "Our engagement is low this week, adjust the posting strategy"

Claude: I'll analyze the performance and update workflows:
1. Check this week's analytics
2. Identify best-performing content types  
3. Modify n8n workflows to prioritize those formats
4. Reschedule upcoming posts for optimal times

[calls: analyze_content_performance, update_workflow_config]
```

## Component Responsibilities

### MCP Server (`mcp/server.py`)
- **Purpose**: Intelligent, conversational interface
- **Handles**: 
  - Ad-hoc content requests
  - Creative variations
  - Performance analysis
  - System configuration
- **Benefits**: Flexible, context-aware, can handle edge cases

### n8n Workflows (`publishing/workflows/`)
- **Purpose**: Reliable, scheduled automation  
- **Handles**:
  - Daily content generation
  - Batch operations
  - Error recovery
  - Monitoring & alerts
- **Benefits**: Deterministic, visual debugging, proven reliability

### Core Modules (Shared by both)
- **Image Generation**: `image_gen/`
- **Design System**: `design/`
- **Publishing**: `publishing/`
- **Content Management**: `content/`

## Data Flow Examples

### Morning Automation (n8n)
```
9:00 AM: n8n triggers daily workflow
  ├─ Reads content calendar (Google Sheets)
  ├─ Calls image_gen.generate() for each theme
  ├─ Applies brand templates via design.compositor
  ├─ Generates captions via content.generator
  ├─ Schedules posts via publishing.scheduler
  └─ Sends summary email
```

### Interactive Session (MCP)
```
User → Claude: "Make the Tuesday post more vibrant"
  ├─ MCP calls get_content_calendar("tuesday")
  ├─ MCP calls generate_image(prompt="vibrant version of...")
  ├─ MCP calls brand_assets(template="bold")
  └─ Returns: Updated post preview
```

## Advantages of Hybrid Approach

| Aspect | Pure n8n | Pure MCP | Hybrid |
|--------|----------|----------|--------|
| **Reliability** | ✅ High | ⚠️ Variable | ✅ High (n8n backbone) |
| **Flexibility** | ❌ Low | ✅ High | ✅ High (MCP interface) |
| **Debugging** | ✅ Visual | ⚠️ Logs only | ✅ Both |
| **Cost** | 💰 Free | 💰 API calls | 💰 Minimal API calls |
| **Speed** | ✅ Fast | ⚠️ LLM latency | ✅ Fast (n8n), Smart (MCP) |

## Implementation Priority

### Week 1: Core System
1. Build core modules (image_gen, design, publishing)
2. Create basic n8n workflows
3. Test end-to-end automation

### Week 2: MCP Integration  
1. Implement MCP server
2. Expose key tools to Claude
3. Test interactive workflows

### Week 3: Advanced Features
1. Performance analytics
2. Intelligent workflow updates
3. Multi-platform optimization

## Future Roadmap

- **Smart Content Optimization**: MCP analyzes performance and suggests n8n workflow improvements
- **A/B Testing**: MCP creates variants, n8n deploys them systematically
- **Audience Segmentation**: MCP personalizes content, n8n handles delivery logic
- **Trend Integration**: MCP identifies trends, updates n8n templates automatically 