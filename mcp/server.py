"""
MCP Server for Content Automation System
Exposes tools for Claude to interact with the content generation pipeline
"""

import asyncio
from typing import Any, Sequence
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource, Tool, TextContent, ImageContent, EmbeddedResource
)

# Import our core modules
from core.settings import settings
from image_gen.generator import ImageGenerator
from design.compositor import DesignCompositor
from publishing.scheduler import ContentScheduler
from content.generator import CaptionGenerator

# Initialize our components
image_gen = ImageGenerator()
design_comp = DesignCompositor()
scheduler = ContentScheduler()
caption_gen = CaptionGenerator()

server = Server("content-automation")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List all available content automation tools"""
    return [
        Tool(
            name="generate_image",
            description="Generate an image using Stable Diffusion based on a text prompt",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Text description of image to generate"},
                    "style": {"type": "string", "description": "Art style (optional): realistic, cartoon, abstract, etc."},
                    "size": {"type": "string", "description": "Image size: 1024x1024, 1024x576, etc."},
                    "steps": {"type": "integer", "description": "Inference steps (default: 30)"}
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="enhance_prompt",
            description="Enhance a basic prompt into a detailed SD prompt using local LLM",
            inputSchema={
                "type": "object",
                "properties": {
                    "basic_prompt": {"type": "string", "description": "Simple description to enhance"},
                    "style_preference": {"type": "string", "description": "Preferred artistic style"}
                },
                "required": ["basic_prompt"]
            }
        ),
        Tool(
            name="create_social_post",
            description="Generate a complete social media post with image and caption",
            inputSchema={
                "type": "object",
                "properties": {
                    "theme": {"type": "string", "description": "Content theme/topic"},
                    "platform": {"type": "string", "description": "Target platform: instagram, twitter, linkedin"},
                    "tone": {"type": "string", "description": "Content tone: professional, casual, inspirational"},
                    "include_hashtags": {"type": "boolean", "description": "Whether to include hashtags"}
                },
                "required": ["theme", "platform"]
            }
        ),
        Tool(
            name="schedule_content",
            description="Schedule content for future posting",
            inputSchema={
                "type": "object",
                "properties": {
                    "content_id": {"type": "string", "description": "ID of generated content"},
                    "schedule_time": {"type": "string", "description": "ISO datetime string"},
                    "platforms": {"type": "array", "items": {"type": "string"}, "description": "Target platforms"}
                },
                "required": ["content_id", "schedule_time", "platforms"]
            }
        ),
        Tool(
            name="get_content_calendar",
            description="View scheduled content and pipeline status",
            inputSchema={
                "type": "object",
                "properties": {
                    "date_range": {"type": "string", "description": "Date range: this_week, next_week, this_month"}
                }
            }
        ),
        Tool(
            name="brand_assets",
            description="Apply brand assets (logo, colors, fonts) to generated content",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "Path to image to brand"},
                    "template": {"type": "string", "description": "Brand template: minimal, bold, elegant"},
                    "add_logo": {"type": "boolean", "description": "Whether to add company logo"}
                },
                "required": ["image_path"]
            }
        ),
        Tool(
            name="analyze_content_performance",
            description="Get insights on content performance and suggestions",
            inputSchema={
                "type": "object",
                "properties": {
                    "time_period": {"type": "string", "description": "Analysis period: week, month, quarter"},
                    "metric": {"type": "string", "description": "Metric to analyze: engagement, reach, clicks"}
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls from Claude"""
    
    if name == "generate_image":
        result = await image_gen.generate(
            prompt=arguments["prompt"],
            style=arguments.get("style"),
            size=arguments.get("size", "1024x1024"),
            steps=arguments.get("steps", 30)
        )
        return [
            TextContent(type="text", text=f"Generated image: {result['image_path']}"),
            ImageContent(
                type="image",
                data=result["image_data"],
                mimeType="image/png"
            )
        ]
    
    elif name == "enhance_prompt":
        enhanced = await image_gen.enhance_prompt(
            arguments["basic_prompt"],
            arguments.get("style_preference")
        )
        return [TextContent(type="text", text=f"Enhanced prompt: {enhanced}")]
    
    elif name == "create_social_post":
        post = await create_complete_post(
            theme=arguments["theme"],
            platform=arguments["platform"],
            tone=arguments.get("tone", "professional"),
            include_hashtags=arguments.get("include_hashtags", True)
        )
        return [
            TextContent(type="text", text=f"Created post: {post['caption']}"),
            ImageContent(
                type="image", 
                data=post["image_data"],
                mimeType="image/png"
            )
        ]
    
    elif name == "schedule_content":
        result = await scheduler.schedule(
            arguments["content_id"],
            arguments["schedule_time"],
            arguments["platforms"]
        )
        return [TextContent(type="text", text=f"Scheduled: {result}")]
    
    elif name == "get_content_calendar":
        calendar = await scheduler.get_calendar(arguments.get("date_range", "this_week"))
        return [TextContent(type="text", text=f"Calendar: {calendar}")]
    
    elif name == "brand_assets":
        branded = await design_comp.apply_branding(
            arguments["image_path"],
            template=arguments.get("template", "minimal"),
            add_logo=arguments.get("add_logo", True)
        )
        return [TextContent(type="text", text=f"Branded image: {branded}")]
    
    elif name == "analyze_content_performance":
        analysis = await analyze_performance(
            arguments.get("time_period", "week"),
            arguments.get("metric", "engagement")
        )
        return [TextContent(type="text", text=f"Performance: {analysis}")]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def create_complete_post(theme: str, platform: str, tone: str, include_hashtags: bool):
    """Create a complete social media post with image and caption"""
    # Generate image based on theme
    image_result = await image_gen.generate(
        prompt=f"{theme} content for {platform}",
        style="professional" if tone == "professional" else "creative"
    )
    
    # Generate caption
    caption = await caption_gen.generate(
        theme=theme,
        platform=platform,
        tone=tone,
        include_hashtags=include_hashtags
    )
    
    return {
        "image_path": image_result["image_path"],
        "image_data": image_result["image_data"],
        "caption": caption,
        "platform": platform
    }

async def analyze_performance(time_period: str, metric: str):
    """Analyze content performance"""
    # This would integrate with platform APIs to get real metrics
    return f"Analysis for {time_period}: {metric} trending upward"

async def main():
    # Run the server using stdin/stdout streams
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="content-automation",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main()) 