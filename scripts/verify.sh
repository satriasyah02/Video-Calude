#!/bin/bash
# Semak semua tools untuk edit video pendek 9:16 (1080x1920).
export PATH="$HOME/.local/bin:$PATH"
ok(){ printf "  [OK]   %s\n" "$1"; }; bad(){ printf "  [FAIL] %s\n" "$1"; }
chk(){ if eval "$2" >/dev/null 2>&1; then ok "$1"; else bad "$1"; fi; }
chk "Node.js 22+"   'node -e "process.exit(+process.versions.node.split(\".\")[0]>=22?0:1)"'
chk "npm"           'npm --version'
chk "Python 3"      'python3 --version'
chk "pip / uv"      'pip --version || uv --version'
chk "Git"           'git --version'
chk "FFmpeg"        'ffmpeg -version'
chk "FFprobe"       'ffprobe -version'
chk "Claude Code"   'claude --version'
chk "yt-dlp"        'yt-dlp --version'
chk "Video-Use skill"   'test -f ~/.claude/skills/video-use/SKILL.md && cd ~/Developer/video-use && uv run python helpers/timeline_view.py --help'
chk "HyperFrames plugin" 'claude plugin list | grep -q hyperframes@hyperframes'
chk "HyperFrames CLI"    'npx --yes hyperframes --version'
if [ -n "$ELEVENLABS_API_KEY" ] || grep -q '^ELEVENLABS_API_KEY=..' ~/Developer/video-use/.env 2>/dev/null; then ok "ElevenLabs API key"; else bad "ElevenLabs API key (belum ditetapkan)"; fi
