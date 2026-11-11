# Video Edit
### A Claude Code Skill by [@tenfoldmarc](https://www.instagram.com/tenfoldmarc)

Film your talking-head clips on your phone, drop them in a folder, type `/video-edit`, and Claude turns them into a finished Instagram reel. It picks your best take of every line, cuts the dead air, cuts you out of the background so words can sit behind your head, and applies a designed look with captions, motion graphics and sound. You never open an editor: you watch the result, say what you want changed, and it re-renders in about two minutes.

---

## What It Does

1. Finds your clips, makes contact sheets and transcribes every take with word-level timing.
2. Rebuilds your script from your takes (you can repeat lines as many times as you want) and keeps the cleanest one of each, with zero dead air between sections.
3. Cuts the reel straight from your original files, with sharp punch-ins from 4K for variety.
4. Cuts you out of the background, so big words can sit behind your head.
5. Applies one of three looks:
   - **Bold:** kinetic words around you, the big ones behind your head.
   - **Cool girl:** a warm grade with a yellow serif italic, and your own reels orbiting around you.
   - **Cool dude:** a dark editorial grade with tiny spaced capitals and big serif words.
6. Builds animated inserts in parallel with sub-agents: an app on screen behind you, your Instagram profile getting followed on your call to action, a file scrolling.
7. Keeps everything inside the Instagram safe zone, checks every cut frame by frame, and hands you a phone-ready copy.

---

## Requirements

- A Mac, a Windows 10/11 PC or a Linux computer. Apple Silicon Macs are fastest for the background cutout; on Windows and Linux that one step runs on the processor, so it takes longer.
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- [ffmpeg](https://ffmpeg.org)
- [Node.js 22 or newer](https://nodejs.org)
- Python 3.10 or newer ([python.org](https://www.python.org/downloads/))

Don't worry about connecting these manually. On first run the skill checks your computer, figures out whether it's a Mac, a PC or Linux, and gives you the exact line to paste for anything that's missing.

| | Mac | Windows (PowerShell) | Linux |
|---|---|---|---|
| ffmpeg | `brew install ffmpeg` | `winget install --id Gyan.FFmpeg -e` | `sudo apt install ffmpeg` |
| Node.js | `brew install node` | `winget install --id OpenJS.NodeJS.LTS -e` | [nodejs.org](https://nodejs.org) |
| Python | `brew install python` | `winget install --id Python.Python.3.12 -e` | `sudo apt install python3 python3-venv` |

**Windows support is new.** The skill was built and tested on a Mac, and Windows has not had that level of real-world testing yet. If something breaks on your PC, please [open an issue](https://github.com/tenfoldmarc/video-edit-skill/issues) with the error text and the `STATUS` lines the setup printed.

**On Windows:** each line is one paste into PowerShell. After installing, close Claude Code completely and open it again, or it won't see the new programs. Git for Windows is optional (the skill works with or without it). On a Windows ARM laptop (Snapdragon), add `--architecture x64` to the Python line.

---

## Install

No terminal needed.

### Step 1: Open Claude Code

Open Claude Code: the Code tab in the Claude desktop app, or type `claude` in your terminal. (This skill renders video on your computer, so it needs Claude Code; a regular chat can't run it.)

### Step 2: Paste this message

Copy-paste this into the chat and hit Enter:

```
Install this skill for me: https://github.com/tenfoldmarc/video-edit-skill
```

Claude downloads the skill into your skills folder and tells you when it's ready. Takes a few seconds.

### Step 3: Run the skill

Type:

```
/video-edit
```

Hit Enter. On your first run, the skill asks your name, your Instagram handle and your favorite look, checks your tools and sets up everything it needs (about 2 minutes, once). Just follow the prompts.

<details>
<summary>Prefer the terminal? Manual install</summary>

Open Terminal (Mac: `Command + Space`, type Terminal. Windows: Start menu, type PowerShell). Paste this one line and hit Enter (it needs [git](https://git-scm.com/downloads) installed):

```bash
git clone https://github.com/tenfoldmarc/video-edit-skill "$HOME/.claude/skills/video-edit"
```

Then type `claude` to open Claude Code and run `/video-edit`.
</details>

---

## Usage

**Edit today's clips:**
```
/video-edit I just dropped 5 clips in my downloads
```
Claude finds them, shows you which take it picked for each line, and sends you the finished reel.

**Name the look per section:**
```
/video-edit use the cool girl look when I say "the cool girl aesthetic", cool dude after that, bold everywhere else
```

**Give notes on a version:**
```
the captions feel too small, the grain is too much, and cut the pause before "or you can get"
```
It fixes exactly that and re-renders in about two minutes.

Tips for filming: shoot vertical in 4K if your phone allows (punch-ins stay sharp), keep the camera still for each setup, and repeat a line until it feels right. The skill picks the best take.

---

## Updating

Paste this into Claude:

```
Update the video-edit skill from https://github.com/tenfoldmarc/video-edit-skill
```

Or in Terminal / PowerShell: `git -C "$HOME/.claude/skills/video-edit" pull`

---

## Credits

Built on [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML-to-video rendering and background removal) and [faster-whisper](https://github.com/SYSTRAN/faster-whisper). Fonts from Google Fonts (SIL Open Font License). Sound effects from Pixabay, downloaded on setup.

---

## Built By

[@tenfoldmarc](https://www.instagram.com/tenfoldmarc). Follow for daily AI automation walkthroughs, real systems, not theory.
