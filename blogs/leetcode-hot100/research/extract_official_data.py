#!/usr/bin/env python3
"""Build and audit a local research snapshot for LeetCode Hot 100.

The script itself performs no network requests.  It parses HTML/JSON fetched
from the official LeetCode China pages and prepares one batched GraphQL query.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


class NextDataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.capture = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "script" and values.get("id") == "__NEXT_DATA__":
            self.capture = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.capture:
            self.capture = False

    def handle_data(self, data: str) -> None:
        if self.capture:
            self.parts.append(data)


class PlainTextParser(HTMLParser):
    BLOCK_TAGS = {
        "p", "pre", "li", "ul", "ol", "div", "br", "table", "tr", "h1",
        "h2", "h3", "h4", "blockquote",
    }

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        value = html.unescape("".join(self.parts)).replace("\xa0", " ")
        value = re.sub(r"[ \t]+", " ", value)
        value = re.sub(r"\n\s*\n+", "\n", value)
        return value.strip()


def parse_next_data(path: Path) -> dict:
    parser = NextDataParser()
    parser.feed(path.read_text(encoding="utf-8"))
    if not parser.parts:
        raise RuntimeError(f"No __NEXT_DATA__ found in {path}")
    return json.loads("".join(parser.parts))


def find_study_plan(next_data: dict) -> dict:
    queries = next_data["props"]["pageProps"]["dehydratedState"]["queries"]
    for query in queries:
        detail = query.get("state", {}).get("data", {}).get("studyPlanV2Detail")
        if detail:
            return detail
    raise RuntimeError("studyPlanV2Detail not found")


QUESTION_FIELDS = """
questionId
questionFrontendId
title
titleSlug
translatedTitle
translatedContent
difficulty
topicTags { name translatedName slug }
hints
codeSnippets { lang langSlug code }
metaData
""".strip()


def prepare(plan_html: Path, out_dir: Path) -> None:
    detail = find_study_plan(parse_next_data(plan_html))
    rows: list[dict] = []
    for group in detail["planSubGroups"]:
        for order_in_group, question in enumerate(group["questions"], 1):
            rows.append(
                {
                    "order": len(rows) + 1,
                    "module": group["name"],
                    "module_slug": group["slug"],
                    "order_in_module": order_in_group,
                    "id": question["questionFrontendId"],
                    "title": question["translatedTitle"],
                    "title_en": question["title"],
                    "slug": question["titleSlug"],
                    "difficulty": question["difficulty"],
                    "tags": [
                        tag["nameTranslated"]
                        for tag in question.get("topicTags", [])
                        if tag.get("nameTranslated")
                    ],
                    "url": f"https://leetcode.cn/problems/{question['titleSlug']}/",
                }
            )

    aliases = [
        f'q{i}: question(titleSlug: "{row["slug"]}") {{ {QUESTION_FIELDS} }}'
        for i, row in enumerate(rows)
    ]
    payload = {"query": "query Hot100Questions {\n" + "\n".join(aliases) + "\n}"}

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "official_plan.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "questions_query.json").write_text(
        json.dumps(payload, ensure_ascii=False), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "name": detail["name"],
                "modules": len(detail["planSubGroups"]),
                "questions": len(rows),
                "difficulty": Counter(row["difficulty"] for row in rows),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def normalize_content(source: str | None) -> str:
    if not source:
        return ""
    parser = PlainTextParser()
    parser.feed(source)
    return parser.text()


def finish(plan_json: Path, questions_json: Path, out_dir: Path) -> None:
    plan = json.loads(plan_json.read_text(encoding="utf-8"))
    response = json.loads(questions_json.read_text(encoding="utf-8"))
    if response.get("errors"):
        raise RuntimeError(json.dumps(response["errors"], ensure_ascii=False))

    details: list[dict] = []
    missing: list[str] = []
    mismatches: list[dict] = []
    for i, row in enumerate(plan):
        question = response.get("data", {}).get(f"q{i}")
        if not question:
            missing.append(row["slug"])
            continue
        py = next(
            (x["code"] for x in question.get("codeSnippets", []) if x["langSlug"] == "python3"),
            "",
        )
        content_text = normalize_content(question.get("translatedContent"))
        detail = {
            **row,
            "content_text": content_text,
            "hints": question.get("hints", []),
            "python_signature": py,
            "metadata": json.loads(question["metaData"]) if question.get("metaData") else None,
            "official_tags": [
                tag.get("translatedName") or tag["name"]
                for tag in question.get("topicTags", [])
            ],
        }
        details.append(detail)
        if str(question["questionFrontendId"]) != str(row["id"]):
            mismatches.append(
                {"slug": row["slug"], "plan_id": row["id"], "detail_id": question["questionFrontendId"]}
            )
        if row["title"] != question["translatedTitle"]:
            mismatches.append(
                {"slug": row["slug"], "plan_title": row["title"], "detail_title": question["translatedTitle"]}
            )

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "official_questions.json").write_text(
        json.dumps(details, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    audit = {
        "plan_count": len(plan),
        "detail_count": len(details),
        "missing": missing,
        "mismatches": mismatches,
        "difficulty": Counter(row["difficulty"] for row in details),
        "module_counts": Counter(row["module"] for row in details),
        "empty_content": [row["slug"] for row in details if not row["content_text"]],
        "empty_python_signature": [row["slug"] for row in details if not row["python_signature"]],
    }
    (out_dir / "audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(audit, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    prepare_parser = sub.add_parser("prepare")
    prepare_parser.add_argument("plan_html", type=Path)
    prepare_parser.add_argument("out_dir", type=Path)

    finish_parser = sub.add_parser("finish")
    finish_parser.add_argument("plan_json", type=Path)
    finish_parser.add_argument("questions_json", type=Path)
    finish_parser.add_argument("out_dir", type=Path)

    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.plan_html, args.out_dir)
    else:
        finish(args.plan_json, args.questions_json, args.out_dir)


if __name__ == "__main__":
    main()
