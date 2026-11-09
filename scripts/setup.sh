#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
# Video-Use (official install.md)
test -d ~/Developer/video-use || git clone https://github.com/browser-use/video-use ~/Developer/video-use
(cd ~/Developer/video-use && uv sync)
mkdir -p ~/.claude/skills
ln -sfn ~/Developer/video-use ~/.claude/skills/video-use
# yt-dlp
command -v yt-dlp >/dev/null || uv tool install yt-dlp
# HyperFrames Claude Code plugin (official README)
claude plugin marketplace add heygen-com/hyperframes || true
claude plugin install hyperframes@hyperframes || true
