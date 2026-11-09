# Video-Calude — edit video pendek (TikTok / Reels / Shorts)

## Format output (wajib)
- Nisbah 9:16, **1080x1920**, H.264 + AAC, `yuv420p`, 30fps (kecuali diminta lain).
- Pastikan teks/kapsyen berada dalam zon selamat (elak ~250px atas & ~350px bawah untuk UI platform).

## Tools
- **Video-Use** (skill `video-use`, di `~/Developer/video-use`): potong, grade, kapsyen, transkripsi ElevenLabs Scribe. Output ke `<folder_video>/edit/`.
- **HyperFrames** (plugin `hyperframes@hyperframes`, CLI `npx hyperframes`): animasi/overlay HTML -> video. Guna `--resolution portrait`.
- **yt-dlp**: muat turun video rujukan.
- **FFmpeg / FFprobe**: encode & semak.
- Remotion: BELUM dipasang — tanya pengguna dahulu.

## Peraturan
- Jangan edit atau transcribe video tanpa arahan pengguna (transkripsi kos kredit ElevenLabs).
- Jangan commit `.env`, API key, atau fail video mentah/output.
- Semak tools: `bash scripts/verify.sh`. Pasang semula: `bash scripts/setup.sh`.
