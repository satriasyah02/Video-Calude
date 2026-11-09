import json, subprocess, sys, os
edit = sys.argv[1]
e = json.load(open(f"{edit}/edl.json"))
src = e["sources"]["S"]
W, H, FPS = 1080, 1920, 30
GRADE = "hqdn3d=1.5:1.5:4:4,eq=contrast=1.08:brightness=0.015:saturation=1.12:gamma=0.97,colorbalance=rm=-0.03:bm=0.04:rh=-0.02:bh=0.03,unsharp=5:5:0.9:5:5:0.0"
os.makedirs(f"{edit}/clips", exist_ok=True)
segmap, t = [], 0.0
files = []
for i, r in enumerate(e["ranges"]):
    s, en = r["start"], r["end"]
    spd = r.get("speed", 1.0)
    z = r.get("zoom", 1.0)
    dur = (en - s) / spd
    zw, zh = int(round(W*z/2)*2), int(round(H*z/2)*2)
    vf = f"setpts=(PTS-STARTPTS)/{spd},fps={FPS},scale={zw}:{zh}:flags=lanczos,crop={W}:{H}:(iw-{W})/2:(ih-{H})*0.35,setsar=1,{GRADE},format=yuv420p"
    out = f"{edit}/clips/seg_{i:02d}.mp4"
    cmd = ["ffmpeg","-v","error","-y","-ss",f"{s:.3f}","-to",f"{en:.3f}","-i",src]
    if r.get("mute"):
        cmd += ["-f","lavfi","-t",f"{dur:.3f}","-i","anullsrc=r=48000:cl=stereo",
                "-map","0:v:0","-map","1:a:0","-vf",vf]
    else:
        af = f"aresample=48000,afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03:.3f}:d=0.03"
        cmd += ["-map","0:v:0","-map","0:a:0","-vf",vf,"-af",af]
    cmd += ["-t",f"{dur:.3f}","-c:v","libx264","-preset","slow","-crf","14","-g",str(FPS),
            "-c:a","aac","-b:a","192k","-ac","2","-ar","48000","-movflags","+faststart",out]
    subprocess.run(cmd, check=True)
    d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out]))
    segmap.append({"i":i,"beat":r["beat"],"quote":r["quote"],"src_start":s,"src_end":en,"speed":spd,"out_start":round(t,3),"out_dur":round(d,3)})
    t += d
    files.append(out)
with open(f"{edit}/clips/list.txt","w") as f:
    for p in files: f.write(f"file '{p}'\n")
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{edit}/clips/list.txt","-c","copy","-movflags","+faststart",f"{edit}/base.mp4"],check=True)
json.dump(segmap, open(f"{edit}/segmap.json","w"), indent=1)
print("total", round(t,2))
