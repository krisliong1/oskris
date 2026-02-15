#!/usr/bin/env python3
"""
关键词提取和实体识别脚本
从对话文本中提取关键信息
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Set
from collections import Counter

class KeywordExtractor:
    """关键词和实体提取器"""
    
    def __init__(self):
        # 技术关键词库
        self.tech_keywords = {
            # 编程语言
            "languages": [
                "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", 
                "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Dart"
            ],
            # 框架
            "frameworks": [
                "React", "Vue", "Angular", "Next.js", "Nuxt", "Django", 
                "Flask", "FastAPI", "Express", "NestJS", "Spring", "Laravel"
            ],
            # 工具
            "tools": [
                "Git", "Docker", "Kubernetes", "VS Code", "GitHub", "GitLab",
                "Jenkins", "Webpack", "Vite", "npm", "yarn", "pnpm"
            ],
            # 数据库
            "databases": [
                "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite",
                "MariaDB", "Cassandra", "DynamoDB", "Elasticsearch"
            ],
            # 云服务
            "cloud": [
                "AWS", "Azure", "GCP", "Vercel", "Netlify", "Heroku",
                "DigitalOcean", "Cloudflare", "Firebase"
            ]
        }
        
        # 优先级关键词
        self.priority_keywords = {
            "urgent": [
                "紧急", "urgent", "asap", "立即", "马上", "今天", "today",
                "现在", "now", "immediately", "急"
            ],
            "important": [
                "重要", "important", "关键", "核心", "必须", "must",
                "critical", "crucial", "essential", "vital"
            ]
        }
        
        # 时间关键词
        self.time_keywords = {
            "今天": 0, "明天": 1, "后天": 2,
            "下周": 7, "下个月": 30,
            "today": 0, "tomorrow": 1
        }
        
        # 分类关键词
        self.category_keywords = {
            "work": ["工作", "项目", "会议", "任务", "deadline", "客户", "同事"],
            "life": ["生活", "家庭", "朋友", "健康", "购物", "旅游"],
            "learning": ["学习", "笔记", "教程", "课程", "书籍", "技能"]
        }
    
    def extract(self, text: str) -> Dict:
        """主提取函数"""
        return {
            "entities": self.extract_entities(text),
            "keywords": self.extract_keywords(text),
            "tech_keywords": self.extract_tech_keywords(text),
            "dates": self.extract_dates(text),
            "tasks": self.extract_tasks(text),
            "priority": self.determine_priority(text),
            "category": self.determine_category(text),
            "sentiment": self.analyze_sentiment(text)
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """提取实体(简化版,实际应使用 NLP 库)"""
        entities = {
            "PERSON": [],
            "ORG": [],
            "PRODUCT": [],
            "LOCATION": []
        }
        
        # 简单的模式匹配(实际应使用 spaCy 或其他 NLP 库)
        # 这里只是示例
        
        # 检测人名(中文姓名模式)
        person_pattern = r'[\u4e00-\u9fa5]{2,4}(?:先生|女士|老师|经理|总监)?'
        # 检测组织名
        org_pattern = r'[\u4e00-\u9fa5]+(?:公司|科技|集团|有限公司|股份)'
        
        return entities
    
    def extract_keywords(self, text: str) -> List[str]:
        """提取一般关键词"""
        # 简单的词频统计(实际应使用 jieba 分词)
        words = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+', text)
        
        # 过滤停用词
        stop_words = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人'}
        keywords = [w for w in words if w not in stop_words and len(w) > 1]
        
        # 统计词频
        counter = Counter(keywords)
        return [word for word, count in counter.most_common(10)]
    
    def extract_tech_keywords(self, text: str) -> List[Dict[str, str]]:
        """提取技术关键词"""
        found = []
        
        for category, keywords in self.tech_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    found.append({
                        "keyword": keyword,
                        "category": category
                    })
        
        return found
    
    def extract_dates(self, text: str) -> List[Dict]:
        """提取日期和时间信息"""
        dates = []
        
        # 检测相对时间
        for keyword, offset in self.time_keywords.items():
            if keyword in text:
                target_date = datetime.now().date()
                from datetime import timedelta
                target_date += timedelta(days=offset)
                dates.append({
                    "text": keyword,
                    "date": target_date.isoformat(),
                    "type": "relative"
                })
        
        # 检测绝对日期(简单模式)
        date_patterns = [
            r'(\d{4})[年-](\d{1,2})[月-](\d{1,2})',  # 2024-01-15
            r'(\d{1,2})[月/](\d{1,2})[日/]',         # 1/15
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                dates.append({
                    "text": match.group(0),
                    "type": "absolute"
                })
        
        return dates
    
    def extract_tasks(self, text: str) -> List[str]:
        """提取任务"""
        tasks = []
        
        # 任务标识词
        task_indicators = ['要', '需要', '完成', '做', 'TODO', 'todo', '任务']
        
        # 简单的句子分割
        sentences = re.split(r'[。！？\n;]', text)
        
        for sentence in sentences:
            for indicator in task_indicators:
                if indicator in sentence:
                    tasks.append(sentence.strip())
                    break
        
        return tasks
    
    def determine_priority(self, text: str) -> str:
        """判断优先级"""
        text_lower = text.lower()
        
        # 检查紧急关键词
        for keyword in self.priority_keywords["urgent"]:
            if keyword in text_lower:
                return "urgent"
        
        # 检查重要关键词
        for keyword in self.priority_keywords["important"]:
            if keyword in text_lower:
                return "important"
        
        return "normal"
    
    def determine_category(self, text: str) -> str:
        """判断分类"""
        scores = {category: 0 for category in self.category_keywords}
        
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    scores[category] += 1
        
        # 返回得分最高的分类
        max_category = max(scores, key=scores.get)
        return max_category if scores[max_category] > 0 else "general"
    
    def analyze_sentiment(self, text: str) -> str:
        """简单的情感分析"""
        positive_words = ['好', '棒', '优秀', '成功', '完成', '高兴', 'good', 'great', 'excellent']
        negative_words = ['差', '糟', '失败', '问题', '错误', 'bad', 'poor', 'fail', 'error']
        
        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"


def main():
    """测试函数"""
    extractor = KeywordExtractor()
    
    test_texts = [
        "明天要完成网站的 React 首页设计,这个很紧急!要用 Next.js 框架。",
        "学习了 Python Django 框架,做了一个博客项目,感觉很好。",
        "记住我喜欢用 VS Code 编辑器,主题是 One Dark Pro。"
    ]
    
    for text in test_texts:
        print(f"\n测试文本: {text}")
        print("-" * 50)
        result = extractor.extract(text)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
