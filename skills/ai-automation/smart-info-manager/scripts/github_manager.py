#!/usr/bin/env python3
"""
GitHub 仓库管理脚本
处理文件的存储、提交和索引更新
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class GitHubManager:
    """GitHub 仓库管理器"""
    
    def __init__(self, repo_path: str = "krisliong1/oskris"):
        self.repo_path = repo_path
        self.local_path = "/tmp/oskris"
        self.repo_url = f"https://github.com/{repo_path}.git"
        
        # 目录结构
        self.directories = {
            "memories": {
                "personal": "memories/personal",
                "preferences": "memories/preferences",
                "conversations": "memories/conversations"
            },
            "tasks": {
                "urgent": "tasks/urgent",
                "important": "tasks/important",
                "normal": "tasks/normal"
            },
            "projects": "projects",
            "notes": {
                "tech": "notes/tech",
                "work": "notes/work",
                "learning": "notes/learning"
            },
            "archive": "archive",
            "index": "index"
        }
    
    def init_repo(self):
        """初始化或克隆仓库"""
        if os.path.exists(self.local_path):
            # 拉取最新更改
            os.system(f"cd {self.local_path} && git pull")
        else:
            # 克隆仓库
            os.system(f"git clone {self.repo_url} {self.local_path}")
        
        # 创建目录结构
        self.create_directory_structure()
    
    def create_directory_structure(self):
        """创建完整的目录结构"""
        def create_dirs(base_path: str, structure: dict):
            if isinstance(structure, dict):
                for key, value in structure.items():
                    if isinstance(value, str):
                        Path(os.path.join(base_path, value)).mkdir(parents=True, exist_ok=True)
                    elif isinstance(value, dict):
                        create_dirs(base_path, value)
        
        create_dirs(self.local_path, self.directories)
    
    def determine_filepath(self, info: Dict) -> str:
        """根据提取的信息确定文件路径"""
        category = info.get("category", "general")
        priority = info.get("priority", "normal")
        
        # 生成时间戳
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        timestamp = now.strftime("%Y%m%d-%H%M%S")
        
        # 根据内容类型确定路径
        if info.get("tasks"):
            # 任务文件
            base_dir = self.directories["tasks"][priority]
            filename = f"{timestamp}-task.md"
        elif category == "learning":
            # 学习笔记
            base_dir = self.directories["notes"]["learning"]
            filename = f"{date_str}-note.md"
        elif "tech_keywords" in info and info["tech_keywords"]:
            # 技术笔记
            base_dir = self.directories["notes"]["tech"]
            filename = f"{date_str}-tech.md"
        else:
            # 默认归档
            base_dir = f"{self.directories['archive']}/{now.year}/{now.month:02d}/{now.day:02d}"
            Path(os.path.join(self.local_path, base_dir)).mkdir(parents=True, exist_ok=True)
            filename = f"{timestamp}.md"
        
        return os.path.join(base_dir, filename)
    
    def generate_markdown(self, text: str, info: Dict) -> str:
        """生成 Markdown 格式的文件内容"""
        now = datetime.now()
        
        # 构建 frontmatter
        frontmatter = {
            "date": now.isoformat(),
            "category": info.get("category", "general"),
            "priority": info.get("priority", "normal"),
            "tags": info.get("keywords", [])[:10],  # 取前10个关键词
            "entities": [e for e in info.get("entities", {}).values() if e],
            "tech_keywords": [kw["keyword"] for kw in info.get("tech_keywords", [])],
            "sentiment": info.get("sentiment", "neutral")
        }
        
        # 构建内容
        content_parts = [
            "---",
            json.dumps(frontmatter, indent=2, ensure_ascii=False),
            "---",
            "",
            f"# {info.get('category', 'Note').title()} - {now.strftime('%Y-%m-%d')}",
            "",
            "## 内容",
            text,
            ""
        ]
        
        # 添加提取的任务
        if info.get("tasks"):
            content_parts.extend([
                "## 任务清单",
                ""
            ])
            for task in info["tasks"]:
                content_parts.append(f"- [ ] {task}")
            content_parts.append("")
        
        # 添加关键词
        if info.get("keywords"):
            content_parts.extend([
                "## 关键词",
                ""
            ])
            for keyword in info["keywords"][:10]:
                content_parts.append(f"- {keyword}")
            content_parts.append("")
        
        # 添加技术关键词
        if info.get("tech_keywords"):
            content_parts.extend([
                "## 技术栈",
                ""
            ])
            tech_by_category = {}
            for kw in info["tech_keywords"]:
                category = kw["category"]
                if category not in tech_by_category:
                    tech_by_category[category] = []
                tech_by_category[category].append(kw["keyword"])
            
            for category, keywords in tech_by_category.items():
                content_parts.append(f"**{category.title()}**: {', '.join(keywords)}")
            content_parts.append("")
        
        # 添加时间信息
        if info.get("dates"):
            content_parts.extend([
                "## 时间信息",
                ""
            ])
            for date in info["dates"]:
                content_parts.append(f"- {date.get('text', '')} ({date.get('type', '')})")
            content_parts.append("")
        
        return "\n".join(content_parts)
    
    def save_file(self, text: str, info: Dict) -> str:
        """保存文件到本地仓库"""
        # 确定文件路径
        filepath = self.determine_filepath(info)
        full_path = os.path.join(self.local_path, filepath)
        
        # 创建目录
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # 生成内容
        content = self.generate_markdown(text, info)
        
        # 写入文件
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def update_index(self, filepath: str, info: Dict):
        """更新索引文件"""
        index_dir = os.path.join(self.local_path, "index")
        
        # 更新关键词索引
        keywords_index = os.path.join(index_dir, "keywords.json")
        self._update_json_index(keywords_index, info.get("keywords", []), filepath)
        
        # 更新技术关键词索引
        tech_index = os.path.join(index_dir, "tech-keywords.json")
        tech_keywords = [kw["keyword"] for kw in info.get("tech_keywords", [])]
        self._update_json_index(tech_index, tech_keywords, filepath)
        
        # 更新时间线索引
        timeline_index = os.path.join(index_dir, "timeline.json")
        date_key = datetime.now().strftime("%Y-%m-%d")
        self._update_timeline_index(timeline_index, date_key, filepath, info)
    
    def _update_json_index(self, index_file: str, keywords: List[str], filepath: str):
        """更新 JSON 索引"""
        # 读取现有索引
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
        else:
            index = {}
        
        # 更新索引
        for keyword in keywords:
            if keyword not in index:
                index[keyword] = {
                    "count": 0,
                    "files": [],
                    "last_updated": None
                }
            
            index[keyword]["count"] += 1
            if filepath not in index[keyword]["files"]:
                index[keyword]["files"].append(filepath)
            index[keyword]["last_updated"] = datetime.now().isoformat()
        
        # 写回文件
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    
    def _update_timeline_index(self, index_file: str, date_key: str, filepath: str, info: Dict):
        """更新时间线索引"""
        # 读取现有索引
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                timeline = json.load(f)
        else:
            timeline = {}
        
        # 更新索引
        if date_key not in timeline:
            timeline[date_key] = {
                "tasks": 0,
                "notes": 0,
                "memories": 0,
                "files": []
            }
        
        # 统计类型
        category = info.get("category", "general")
        if "tasks" in info and info["tasks"]:
            timeline[date_key]["tasks"] += 1
        elif category == "learning":
            timeline[date_key]["notes"] += 1
        else:
            timeline[date_key]["memories"] += 1
        
        timeline[date_key]["files"].append({
            "path": filepath,
            "category": category,
            "priority": info.get("priority", "normal")
        })
        
        # 写回文件
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(timeline, f, indent=2, ensure_ascii=False)
    
    def commit_and_push(self, filepath: str, message: str = None):
        """提交并推送到 GitHub"""
        if not message:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"Auto-save: {filepath} ({now})"
        
        # Git 操作
        commands = [
            f"cd {self.local_path}",
            f"git add {filepath} index/",
            f'git commit -m "{message}"',
            "git push origin main"
        ]
        
        command = " && ".join(commands)
        result = os.system(command)
        
        return result == 0
    
    def process_and_save(self, text: str, info: Dict) -> Dict:
        """完整的处理流程"""
        # 初始化仓库
        self.init_repo()
        
        # 保存文件
        filepath = self.save_file(text, info)
        
        # 更新索引
        self.update_index(filepath, info)
        
        # 提交推送
        success = self.commit_and_push(filepath)
        
        return {
            "success": success,
            "filepath": filepath,
            "repo_url": self.repo_url,
            "github_url": f"https://github.com/{self.repo_path}/blob/main/{filepath}"
        }


def main():
    """测试函数"""
    manager = GitHubManager()
    
    # 测试数据
    test_text = "明天要完成网站的 React 首页设计,这个很紧急!"
    test_info = {
        "category": "work",
        "priority": "urgent",
        "keywords": ["网站", "React", "首页设计"],
        "tech_keywords": [{"keyword": "React", "category": "frameworks"}],
        "tasks": ["完成网站的 React 首页设计"],
        "dates": [{"text": "明天", "type": "relative"}],
        "sentiment": "neutral"
    }
    
    result = manager.process_and_save(test_text, test_info)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
