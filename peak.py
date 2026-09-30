"""Find the most-replayed moments in a YouTube video using yt-dlp's heatmap data."""

import sys
import re
import yt_dlp


def extract_video_id(url: str) -> str | None:
    patterns = [
        r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:embed|shorts)/([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_heatmap(url: str) -> list[dict] | None:
    opts = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info.get("heatmap")


def merge_peaks(segments: list[dict], top_n: int = 3) -> list[dict]:
    """Group neighbouring high-heat segments into single moments, return top N."""
    if not segments:
        return []

    threshold = max(s["value"] for s in segments) * 0.3

    groups: list[list[dict]] = []
    current_group: list[dict] = []

    for seg in segments:
        if seg["value"] >= threshold:
            current_group.append(seg)
        else:
            if current_group:
                groups.append(current_group)
                current_group = []
    if current_group:
        groups.append(current_group)

    moments = []
    for group in groups:
        peak_seg = max(group, key=lambda s: s["value"])
        midpoint = (peak_seg["start_time"] + peak_seg["end_time"]) / 2
        moments.append({"time": midpoint, "value": peak_seg["value"]})

    moments.sort(key=lambda m: m["value"], reverse=True)
    return moments[:top_n]


def format_timestamp(seconds: float) -> str:
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python peak.py <youtube-url>")
        sys.exit(1)

    url = sys.argv[1]
    video_id = extract_video_id(url)
    if not video_id:
        print("Error: could not parse a video ID from that URL.")
        sys.exit(1)

    heatmap = fetch_heatmap(url)
    if not heatmap:
        print("This video has no most-replayed heatmap.")
        sys.exit(0)

    moments = merge_peaks(heatmap)

    for i, moment in enumerate(moments, 1):
        ts = format_timestamp(moment["time"])
        t_param = int(moment["time"])
        link = f"https://www.youtube.com/watch?v={video_id}&t={t_param}s"
        print(f"#{i}  {ts:<8} heat {moment['value']:.2f}   {link}")


if __name__ == "__main__":
    main()
