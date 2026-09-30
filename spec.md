# Spec: Most-Replayed Timestamp Finder (Phase 1)

**Type:** Small standalone Python script (`peak.py`)

## Goal

Give it a YouTube URL, get back the timestamp(s) of the most replayed moment(s) in the video.

## Requirement (from the user)

| ID | Requirement |
|----|-------------|
| R1 | Get the timestamp of the viral / most replayed moment of a video using only its URL. |

## Phase 1 functional requirements

| ID | Requirement |
|----|-------------|
| FR-1 | Take a YouTube URL as the command-line argument. |
| FR-2 | Read the video's "Most replayed" heatmap with yt-dlp, without downloading the video. |
| FR-3 | Pick the top 3 most replayed moments, ranked by heat, highest first. Neighbouring segments of the same bump count as one moment. |
| FR-4 | For each moment, print: rank, timestamp (`mm:ss`, or `h:mm:ss` for videos over an hour), heat value (0-1), and a link that opens the video at that time. |
| FR-5 | If the video has no heatmap, print a one-line message saying so and exit. |

## How it works

- Dependency: Python 3.10+ and `yt-dlp`. No ffmpeg, no API keys.
- yt-dlp returns the heatmap as a list of `{start_time, end_time, value}` segments, where `value` is 0-1 and 1.0 is the video's own peak.
- The jump-to time for a moment is the midpoint of its segment.

## Usage and output

```bash
python peak.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

```
#1  8:24   heat 1.00   https://www.youtube.com/watch?v=VIDEO_ID&t=504s
#2  21:07  heat 0.81   https://www.youtube.com/watch?v=VIDEO_ID&t=1267s
#3  3:40   heat 0.66   https://www.youtube.com/watch?v=VIDEO_ID&t=220s
```

## Done when

1. Running the script on a public video with a heatmap prints up to 3 ranked moments with working links.
2. Nothing is downloaded and no API key is needed.

## Later (to brainstorm)

- Skip peaks in the first seconds of the video
- Minimum heat threshold
- `--top N` flag
- JSON output
- Suggested start/end clip window around each peak
- Cutting the actual clip (see `spec.md`)
