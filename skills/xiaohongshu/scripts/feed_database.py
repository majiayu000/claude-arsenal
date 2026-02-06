#!/usr/bin/env python3
"""
小红书高赞笔记本地数据库
支持：添加、查询、分析、导出
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from collections import Counter

DB_DIR = Path.cwd() / "database"
DB_FILE = DB_DIR / "feeds.json"
SUMMARY_FILE = DB_DIR / "summary.md"


def _load_db() -> dict:
    if DB_FILE.exists():
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"feeds": [], "meta": {"created_at": datetime.now().isoformat(), "version": 1}}


def _save_db(db: dict):
    DB_DIR.mkdir(parents=True, exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def add(feed_json: str):
    """添加一条笔记到数据库，输入为 JSON 字符串"""
    feed = json.loads(feed_json)

    required = ["feed_id", "title"]
    for key in required:
        if key not in feed:
            print(json.dumps({"success": False, "error": f"缺少必填字段: {key}"}))
            sys.exit(1)

    db = _load_db()

    # 去重：同 feed_id 则更新
    existing_ids = {f["feed_id"]: i for i, f in enumerate(db["feeds"])}
    feed["updated_at"] = datetime.now().isoformat()

    if feed["feed_id"] in existing_ids:
        idx = existing_ids[feed["feed_id"]]
        feed["created_at"] = db["feeds"][idx].get("created_at", feed["updated_at"])
        db["feeds"][idx] = feed
        action = "updated"
    else:
        feed["created_at"] = feed["updated_at"]
        db["feeds"].append(feed)
        action = "added"

    _save_db(db)
    print(json.dumps({"success": True, "action": action, "feed_id": feed["feed_id"], "total": len(db["feeds"])}))


def list_feeds(domain: str = None, min_likes: int = 0, limit: int = 50):
    """列出数据库中的笔记"""
    db = _load_db()
    feeds = db["feeds"]

    if domain:
        feeds = [f for f in feeds if f.get("domain") == domain]
    if min_likes > 0:
        feeds = [f for f in feeds if f.get("likes", 0) >= min_likes]

    # 按赞数降序
    feeds.sort(key=lambda x: x.get("likes", 0), reverse=True)
    feeds = feeds[:limit]

    result = []
    for f in feeds:
        result.append({
            "feed_id": f["feed_id"],
            "title": f.get("title", ""),
            "author": f.get("author", ""),
            "likes": f.get("likes", 0),
            "favorites": f.get("favorites", 0),
            "comments": f.get("comments", 0),
            "domain": f.get("domain", ""),
            "created_at": f.get("created_at", ""),
        })

    print(json.dumps({"total": len(db["feeds"]), "filtered": len(result), "feeds": result}, ensure_ascii=False, indent=2))


def get(feed_id: str):
    """获取单条笔记完整数据"""
    db = _load_db()
    for f in db["feeds"]:
        if f["feed_id"] == feed_id:
            print(json.dumps(f, ensure_ascii=False, indent=2))
            return
    print(json.dumps({"error": f"未找到 feed_id={feed_id}"}))
    sys.exit(1)


def analyze():
    """分析数据库中所有笔记，生成洞察摘要"""
    db = _load_db()
    feeds = db["feeds"]

    if not feeds:
        print(json.dumps({"error": "数据库为空"}))
        return

    total = len(feeds)
    likes_list = [f.get("likes", 0) for f in feeds]
    favs_list = [f.get("favorites", 0) for f in feeds]
    comments_list = [f.get("comments", 0) for f in feeds]

    # 互动数据统计
    avg_likes = sum(likes_list) / total
    avg_favs = sum(favs_list) / total
    avg_comments = sum(comments_list) / total

    # 收藏/赞比
    fav_like_ratios = []
    for f in feeds:
        likes = f.get("likes", 0)
        if likes > 0:
            fav_like_ratios.append(f.get("favorites", 0) / likes)

    avg_fav_ratio = sum(fav_like_ratios) / len(fav_like_ratios) if fav_like_ratios else 0

    # 领域分布
    domain_counter = Counter(f.get("domain", "未分类") for f in feeds)

    # 标题类型分布
    title_type_counter = Counter()
    for f in feeds:
        analysis = f.get("analysis", {})
        if analysis.get("title_type"):
            title_type_counter[analysis["title_type"]] += 1

    # 配图风格分布
    image_style_counter = Counter()
    for f in feeds:
        analysis = f.get("analysis", {})
        if analysis.get("image_style"):
            image_style_counter[analysis["image_style"]] += 1

    # 内容类型分布
    content_type_counter = Counter()
    for f in feeds:
        analysis = f.get("analysis", {})
        if analysis.get("content_type"):
            content_type_counter[analysis["content_type"]] += 1

    # 提取高频关键要素
    all_elements = []
    for f in feeds:
        analysis = f.get("analysis", {})
        all_elements.extend(analysis.get("key_elements", []))
    element_counter = Counter(all_elements)

    # 提取高频标签
    all_tags = []
    for f in feeds:
        analysis = f.get("analysis", {})
        all_tags.extend(analysis.get("tags_used", []))
    tag_counter = Counter(all_tags)

    # TOP 5 高赞
    top5 = sorted(feeds, key=lambda x: x.get("likes", 0), reverse=True)[:5]

    insights = {
        "total_feeds": total,
        "engagement": {
            "avg_likes": round(avg_likes, 1),
            "avg_favorites": round(avg_favs, 1),
            "avg_comments": round(avg_comments, 1),
            "avg_fav_like_ratio": round(avg_fav_ratio, 2),
        },
        "domains": dict(domain_counter.most_common()),
        "title_types": dict(title_type_counter.most_common()),
        "image_styles": dict(image_style_counter.most_common()),
        "content_types": dict(content_type_counter.most_common()),
        "top_elements": dict(element_counter.most_common(10)),
        "top_tags": dict(tag_counter.most_common(15)),
        "top5_feeds": [{"title": f.get("title"), "likes": f.get("likes", 0), "author": f.get("author", "")} for f in top5],
        "analyzed_at": datetime.now().isoformat(),
    }

    print(json.dumps(insights, ensure_ascii=False, indent=2))

    # 同时生成 markdown 摘要
    _generate_summary(insights, feeds)


def _generate_summary(insights: dict, feeds: list):
    """生成 markdown 格式的分析摘要"""
    DB_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        "# 小红书高赞笔记分析摘要",
        "",
        f"> 数据库共 {insights['total_feeds']} 篇笔记 | 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
        "## 互动数据均值",
        "",
        f"| 指标 | 均值 |",
        f"|------|------|",
        f"| 赞 | {insights['engagement']['avg_likes']} |",
        f"| 收藏 | {insights['engagement']['avg_favorites']} |",
        f"| 评论 | {insights['engagement']['avg_comments']} |",
        f"| 收藏/赞比 | {insights['engagement']['avg_fav_like_ratio']} |",
        "",
    ]

    if insights["domains"]:
        lines.extend(["## 领域分布", ""])
        for domain, count in insights["domains"].items():
            lines.append(f"- {domain}: {count}篇")
        lines.append("")

    if insights["title_types"]:
        lines.extend(["## 标题类型分布", ""])
        for ttype, count in insights["title_types"].items():
            lines.append(f"- {ttype}: {count}篇")
        lines.append("")

    if insights["image_styles"]:
        lines.extend(["## 配图风格分布", ""])
        for style, count in insights["image_styles"].items():
            lines.append(f"- {style}: {count}篇")
        lines.append("")

    if insights["content_types"]:
        lines.extend(["## 内容类型分布", ""])
        for ctype, count in insights["content_types"].items():
            lines.append(f"- {ctype}: {count}篇")
        lines.append("")

    if insights["top_elements"]:
        lines.extend(["## 高频成功要素 TOP 10", ""])
        for elem, count in insights["top_elements"].items():
            lines.append(f"- {elem} ({count}次)")
        lines.append("")

    if insights["top_tags"]:
        lines.extend(["## 高频标签 TOP 15", ""])
        for tag, count in insights["top_tags"].items():
            lines.append(f"- {tag} ({count}次)")
        lines.append("")

    if insights["top5_feeds"]:
        lines.extend(["## TOP 5 高赞笔记", ""])
        lines.append("| 排名 | 标题 | 作者 | 赞数 |")
        lines.append("|------|------|------|------|")
        for i, f in enumerate(insights["top5_feeds"], 1):
            lines.append(f"| {i} | {f['title']} | {f['author']} | {f['likes']} |")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## 创作建议",
        "",
        "基于以上数据，创作时优先参考：",
    ])

    if insights["title_types"]:
        top_title = list(insights["title_types"].keys())[0]
        lines.append(f"- 标题采用 **{top_title}** 效果最佳")
    if insights["image_styles"]:
        top_style = list(insights["image_styles"].keys())[0]
        lines.append(f"- 配图优先用 **{top_style}** 风格")
    if insights["top_elements"]:
        top3_elems = list(insights["top_elements"].keys())[:3]
        lines.append(f"- 必备要素：{', '.join(top3_elems)}")

    lines.append("")

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n摘要已保存到: {SUMMARY_FILE}", file=sys.stderr)


def delete(feed_id: str):
    """删除一条笔记"""
    db = _load_db()
    before = len(db["feeds"])
    db["feeds"] = [f for f in db["feeds"] if f["feed_id"] != feed_id]
    after = len(db["feeds"])
    _save_db(db)
    print(json.dumps({"success": True, "deleted": before - after, "remaining": after}))


def stats():
    """输出数据库基本统计"""
    db = _load_db()
    feeds = db["feeds"]
    domains = Counter(f.get("domain", "未分类") for f in feeds)
    print(json.dumps({
        "total": len(feeds),
        "domains": dict(domains.most_common()),
        "db_path": str(DB_FILE),
        "db_size": DB_FILE.stat().st_size if DB_FILE.exists() else 0,
    }, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print("用法: feed_database.py <command> [args]")
        print("命令:")
        print("  add '<json>'      添加/更新笔记")
        print("  list [--domain X] [--min-likes N] [--limit N]")
        print("  get <feed_id>     获取单条详情")
        print("  delete <feed_id>  删除")
        print("  analyze           生成分析摘要")
        print("  stats             数据库统计")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "add":
        if len(sys.argv) < 3:
            # 从 stdin 读取
            feed_json = sys.stdin.read()
        else:
            feed_json = sys.argv[2]
        add(feed_json)

    elif cmd == "list":
        kwargs = {}
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i] == "--domain" and i + 1 < len(args):
                kwargs["domain"] = args[i + 1]
                i += 2
            elif args[i] == "--min-likes" and i + 1 < len(args):
                kwargs["min_likes"] = int(args[i + 1])
                i += 2
            elif args[i] == "--limit" and i + 1 < len(args):
                kwargs["limit"] = int(args[i + 1])
                i += 2
            else:
                i += 1
        list_feeds(**kwargs)

    elif cmd == "get":
        get(sys.argv[2])

    elif cmd == "delete":
        delete(sys.argv[2])

    elif cmd == "analyze":
        analyze()

    elif cmd == "stats":
        stats()

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
