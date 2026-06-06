"""
Video Tools - AI视频工具集
支持视频脚本、分镜、字幕生成
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class VideoTools:
    """
    AI视频工具集
    支持：脚本、分镜、字幕、描述
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def generate_script(self, topic: str, duration: str = "5分钟", style: str = "教育") -> Dict:
        """生成视频脚本"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请为以下主题生成视频脚本：

主题：{topic}
时长：{duration}
风格：{style}

请返回JSON格式：
{{
    "title": "视频标题",
    "description": "视频描述",
    "scenes": [
        {{
            "timestamp": "00:00",
            "duration": "30秒",
            "visual": "画面描述",
            "narration": "旁白",
            "text_on_screen": "屏幕文字",
            "music": "音乐建议"
        }}
    ],
    "tags": ["标签1", "标签2"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"script": content}

    def generate_storyboard(self, script: str) -> List[Dict]:
        """生成分镜脚本"""
        if not self.client:
            return [{"error": "LLM客户端未配置"}]

        prompt = f"""请根据以下脚本生成分镜脚本：

{script}

请返回JSON格式：
[
    {{
        "scene": 1,
        "shot_type": "镜头类型",
        "camera_movement": "镜头运动",
        "description": "画面描述",
        "duration": "时长",
        "dialogue": "对话",
        "notes": "备注"
    }}
]"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return [{"storyboard": content}]

    def generate_subtitles(self, transcript: str, style: str = "简洁") -> str:
        """生成字幕"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请根据以下转录生成SRT字幕：

{transcript}

要求：
1. 使用SRT格式
2. {style}风格
3. 每行不超过20字
4. 时间轴准确"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def generate_video_description(self, video_content: str, platform: str = "youtube") -> Dict:
        """生成视频描述"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请为以下视频生成{platform}描述：

内容：{video_content}

请返回JSON格式：
{{
    "title": "标题",
    "description": "描述",
    "tags": ["标签1", "标签2"],
    "category": "分类",
    "thumbnail_text": "缩略图文字"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"description": content}

    def generate_chapters(self, video_content: str) -> List[Dict]:
        """生成视频章节"""
        if not self.client:
            return [{"error": "LLM客户端未配置"}]

        prompt = f"""请根据以下视频内容生成章节：

{video_content}

请返回JSON格式：
[
    {{"timestamp": "00:00", "title": "章节标题", "description": "简短描述"}}
]"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return [{"chapters": content}]

    def suggest_hooks(self, topic: str, count: int = 5) -> List[str]:
        """建议视频开头钩子"""
        if not self.client:
            return ["LLM客户端未配置"]

        prompt = f"""请为"{topic}"视频建议{count}个开头钩子：

要求：
1. 吸引观众注意力
2. 引发好奇心
3. 10秒内

请返回JSON数组格式：["钩子1", "钩子2", ...]"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return [response.choices[0].message.content]


def create_tools(**kwargs) -> VideoTools:
    """创建视频工具"""
    return VideoTools(**kwargs)


if __name__ == "__main__":
    tools = create_tools()

    print("Video Tools")
    print()

    # 测试
    hooks = tools.suggest_hooks("Python编程入门", 3)
    print("Hooks:")
    for h in hooks:
        print(f"  - {h}")
