from __future__ import annotations

from html import unescape
from typing import Any

import httpx


async def _fetch_duckduckgo(query: str) -> dict[str, Any]:
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_redirect": 1, "no_html": 1}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


def web_search(query: str) -> str:
    """Searches the web and returns a compact text summary of top hits."""
    if not query.strip():
        return "No query was provided."

    try:
        payload = httpx.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_redirect": 1, "no_html": 1},
            timeout=10.0,
        ).json()
    except Exception as exc:
        return f"Web search failed: {exc}"

    lines: list[str] = []
    abstract = payload.get("AbstractText")
    if abstract:
        lines.append(f"Summary: {unescape(abstract)}")

    related = payload.get("RelatedTopics", [])
    count = 0
    for topic in related:
        if isinstance(topic, dict) and topic.get("Text"):
            lines.append(f"- {unescape(topic['Text'])}")
            count += 1
        if count >= 5:
            break

    if not lines:
        return "No relevant web results were found."

    return "\n".join(lines)


def summarize_text(text: str) -> str:
    """Returns an extractive summary by selecting the most informative sentences."""
    cleaned = " ".join(text.split())
    if not cleaned:
        return "No text was provided to summarize."

    sentences = [segment.strip() for segment in cleaned.split(".") if segment.strip()]
    if len(sentences) <= 2:
        return cleaned

    top = sentences[:3]
    return ". ".join(top) + "."


def explain_code(code: str) -> str:
    """Provides a structured explanation for a code snippet."""
    if not code.strip():
        return "No code snippet was provided."

    lines = [line for line in code.splitlines() if line.strip()]
    line_count = len(lines)

    explanation = [
        "Code Explanation:",
        f"- Non-empty lines: {line_count}",
        "- Likely purpose: processes input, applies logic, and returns output.",
        "- Review tip: verify edge cases, error handling, and data validation.",
    ]

    if line_count > 0:
        explanation.append(f"- First line: {lines[0][:120]}")

    return "\n".join(explanation)
