#!/usr/bin/env python3
"""
Smart Info Manager - 完整示例
演示如何使用系统自动管理信息
"""

import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from keyword_extractor import KeywordExtractor
from github_manager import GitHubManager


def demo_basic_usage():
    """基础使用示例"""
    print("=" * 60)
    print("示例 1: 基础使用 - 保存一个紧急任务")
    print("=" * 60)
    
    # 创建提取器和管理器
    extractor = KeywordExtractor()
    manager = GitHubManager()
    
    # 用户输入
    text = "记住明天要完成网站的 React 首页设计,这个很紧急!要用 Next.js 框架。"
    
    print(f"\n用户输入: {text}")
    print("\n处理中...")
    
    # 提取信息
    info = extractor.extract(text)
    
    print("\n提取的信息:")
    print(f"  - 分类: {info['category']}")
    print(f"  - 优先级: {info['priority']}")
    print(f"  - 关键词: {', '.join(info['keywords'][:5])}")
    print(f"  - 技术栈: {', '.join([kw['keyword'] for kw in info['tech_keywords']])}")
    print(f"  - 任务: {info['tasks']}")
    print(f"  - 时间: {info['dates']}")
    
    # 保存到 GitHub
    print("\n保存到 GitHub...")
    # result = manager.process_and_save(text, info)
    # print(f"✓ 保存成功!")
    # print(f"  - 文件路径: {result['filepath']}")
    # print(f"  - GitHub 链接: {result['github_url']}")
    print("  (演示模式,未实际保存)")


def demo_batch_processing():
    """批量处理示例"""
    print("\n\n" + "=" * 60)
    print("示例 2: 批量处理多条信息")
    print("=" * 60)
    
    extractor = KeywordExtractor()
    manager = GitHubManager()
    
    texts = [
        "学习了 Python Django 框架,做了一个博客项目。",
        "明天和张三开会讨论新功能,要准备演示。",
        "记住我喜欢用 VS Code,主题是 One Dark Pro。",
        "项目使用 Go + MongoDB + RabbitMQ,部署在 AWS。",
    ]
    
    print(f"\n处理 {len(texts)} 条信息...\n")
    
    for i, text in enumerate(texts, 1):
        print(f"{i}. {text}")
        info = extractor.extract(text)
        print(f"   → 分类: {info['category']}, 优先级: {info['priority']}")
        # result = manager.process_and_save(text, info)
        # print(f"   ✓ 已保存: {result['filepath']}\n")
    
    print("(演示模式,未实际保存)")


def demo_search_index():
    """搜索索引示例"""
    print("\n\n" + "=" * 60)
    print("示例 3: 使用索引搜索信息")
    print("=" * 60)
    
    import json
    
    # 模拟索引数据
    keywords_index = {
        "React": {
            "count": 15,
            "files": [
                "tasks/urgent/20240115-143022-task.md",
                "notes/tech/20240115-react-notes.md",
                "projects/website/20240114-frontend.md"
            ],
            "last_updated": "2024-01-15T14:30:22"
        },
        "Python": {
            "count": 23,
            "files": [
                "notes/learning/20240110-python-django.md",
                "projects/blog/20240112-backend.md"
            ],
            "last_updated": "2024-01-15T10:15:30"
        }
    }
    
    print("\n搜索关键词: 'React'")
    if "React" in keywords_index:
        data = keywords_index["React"]
        print(f"  找到 {data['count']} 个相关记录")
        print(f"  最后更新: {data['last_updated']}")
        print(f"  相关文件:")
        for file in data['files']:
            print(f"    - {file}")
    
    print("\n搜索关键词: 'Python'")
    if "Python" in keywords_index:
        data = keywords_index["Python"]
        print(f"  找到 {data['count']} 个相关记录")
        print(f"  相关文件:")
        for file in data['files'][:3]:
            print(f"    - {file}")


def demo_timeline_view():
    """时间线视图示例"""
    print("\n\n" + "=" * 60)
    print("示例 4: 时间线视图")
    print("=" * 60)
    
    # 模拟时间线数据
    timeline = {
        "2024-01-15": {
            "tasks": 3,
            "notes": 5,
            "memories": 2,
            "files": [
                {
                    "path": "tasks/urgent/20240115-143022-task.md",
                    "category": "work",
                    "priority": "urgent"
                },
                {
                    "path": "notes/tech/20240115-react.md",
                    "category": "learning",
                    "priority": "normal"
                }
            ]
        },
        "2024-01-14": {
            "tasks": 2,
            "notes": 3,
            "memories": 1,
            "files": []
        }
    }
    
    print("\n2024-01-15 的活动:")
    date_data = timeline["2024-01-15"]
    print(f"  任务: {date_data['tasks']} 个")
    print(f"  笔记: {date_data['notes']} 个")
    print(f"  记忆: {date_data['memories']} 个")
    print(f"\n  文件列表:")
    for file in date_data['files']:
        print(f"    [{file['priority']}] {file['path']}")


def demo_tech_stats():
    """技术栈统计示例"""
    print("\n\n" + "=" * 60)
    print("示例 5: 技术栈使用统计")
    print("=" * 60)
    
    # 模拟技术关键词数据
    tech_keywords = {
        "React": {"count": 15, "category": "frameworks"},
        "Python": {"count": 23, "category": "languages"},
        "Docker": {"count": 8, "category": "tools"},
        "PostgreSQL": {"count": 12, "category": "databases"},
        "Next.js": {"count": 7, "category": "frameworks"},
        "Go": {"count": 5, "category": "languages"},
        "MongoDB": {"count": 6, "category": "databases"},
        "VS Code": {"count": 10, "category": "tools"}
    }
    
    # 按类别分组
    by_category = {}
    for keyword, data in tech_keywords.items():
        category = data["category"]
        if category not in by_category:
            by_category[category] = []
        by_category[category].append((keyword, data["count"]))
    
    # 排序并显示
    for category, keywords in by_category.items():
        keywords.sort(key=lambda x: x[1], reverse=True)
        print(f"\n{category.upper()}:")
        for keyword, count in keywords:
            bar = "█" * min(count, 20)
            print(f"  {keyword:15s} {bar} ({count})")


def demo_priority_distribution():
    """优先级分布示例"""
    print("\n\n" + "=" * 60)
    print("示例 6: 任务优先级分布")
    print("=" * 60)
    
    # 模拟任务数据
    tasks = {
        "urgent": 5,
        "important": 12,
        "normal": 28
    }
    
    total = sum(tasks.values())
    
    print(f"\n总任务数: {total}")
    print(f"\n优先级分布:")
    
    for priority, count in tasks.items():
        percentage = (count / total) * 100
        bar = "█" * int(percentage / 2)
        print(f"  {priority:10s} {bar} {count:2d} ({percentage:5.1f}%)")


def interactive_demo():
    """交互式演示"""
    print("\n\n" + "=" * 60)
    print("示例 7: 交互式使用")
    print("=" * 60)
    
    extractor = KeywordExtractor()
    
    print("\n输入一些信息,系统会自动分析和分类。")
    print("输入 'quit' 退出。\n")
    
    while True:
        try:
            text = input("📝 输入信息: ").strip()
            
            if text.lower() == 'quit':
                break
            
            if not text:
                continue
            
            info = extractor.extract(text)
            
            print(f"\n📊 分析结果:")
            print(f"  🏷️  分类: {info['category']}")
            print(f"  ⚡ 优先级: {info['priority']}")
            
            if info['keywords']:
                print(f"  🔑 关键词: {', '.join(info['keywords'][:5])}")
            
            if info['tech_keywords']:
                techs = [kw['keyword'] for kw in info['tech_keywords']]
                print(f"  💻 技术栈: {', '.join(techs)}")
            
            if info['tasks']:
                print(f"  ✅ 任务:")
                for task in info['tasks']:
                    print(f"      - {task}")
            
            if info['dates']:
                print(f"  📅 时间: {info['dates'][0]['text']}")
            
            print(f"  😊 情感: {info['sentiment']}")
            print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"错误: {e}")
    
    print("\n再见! 👋")


def main():
    """主函数"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "Smart Info Manager - 完整演示" + " " * 17 + "║")
    print("╚" + "═" * 58 + "╝")
    
    # 运行各种示例
    demo_basic_usage()
    demo_batch_processing()
    demo_search_index()
    demo_timeline_view()
    demo_tech_stats()
    demo_priority_distribution()
    
    # 交互式演示(可选)
    print("\n\n是否要进入交互式模式? (y/n): ", end='')
    try:
        choice = input().strip().lower()
        if choice == 'y':
            interactive_demo()
    except:
        pass
    
    print("\n\n" + "=" * 60)
    print("演示结束!")
    print("=" * 60)
    print("\n要开始实际使用:")
    print("1. 设置 GitHub token: export GITHUB_TOKEN='your_token'")
    print("2. 运行脚本或在对话中使用触发词")
    print("3. 查看 README.md 了解更多详情")
    print("\n")


if __name__ == "__main__":
    main()
