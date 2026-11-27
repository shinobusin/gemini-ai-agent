import json
import urllib.parse
import urllib.request


def search_wikipedia(topic: str) -> str:
    """Searches Wikipedia for a topic and returns a concise factual summary and source URL."""
    headers = {"User-Agent": "PulseAIAgent/1.0 (https://github.com/shinobusin/my-ai-agent)"}
    try:
        encoded_query = urllib.parse.quote(topic)
        search_url = (
            f"https://en.wikipedia.org/w/api.php?"
            f"action=opensearch&search={encoded_query}&limit=1&namespace=0&format=json"
        )
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            search_data = json.loads(res.read().decode())

        titles = search_data[1]
        if not titles:
            return f"No Wikipedia article found for: {topic}"

        best_title = titles[0]
        encoded_title = urllib.parse.quote(best_title.replace(" ", "_"))

        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"
        summary_req = urllib.request.Request(summary_url, headers=headers)
        with urllib.request.urlopen(summary_req, timeout=10) as res:
            summary_data = json.loads(res.read().decode())

        extract = summary_data.get("extract", "No summary available.")
        page_url = summary_data.get("content_urls", {}).get("desktop", {}).get("page", "")
        return f"Wikipedia — {summary_data.get('title', best_title)}:\n{extract}\nSource: {page_url}"
    except Exception as e:
        return f"Wikipedia lookup failed: {e}"