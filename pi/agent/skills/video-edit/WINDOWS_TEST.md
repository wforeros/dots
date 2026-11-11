# Windows test checklist

The skill was built and run on a Mac. Windows support is new: the Windows code paths were reviewed and unit-tested by simulation, and this checklist is the real-machine run, from a clean Windows PC to a rendered test reel. It takes 30 to 45 minutes, most of it waiting.

You do not need to be technical. Do the steps in order, tick the boxes, and when something fails, stop and report what the "If it fails" line asks for in a [GitHub issue](https://github.com/tenfoldmarc/video-edit-skill/issues).

## What you need

- A Windows 10 or Windows 11 PC with about 10 GB of free disk space
- A Claude plan that includes Claude Code (Pro or Max)
- One vertical phone video of a person talking to the camera, 20 to 40 seconds, saved in your Downloads folder

## Write these down first

- [ ] Windows version: press `Windows + R`, type `winver`, Enter. Note the version and build.
- [ ] Processor and RAM: Settings > System > About. Note "Processor" and "Installed RAM". (If the processor says Snapdragon or ARM, use the x64 Python line from the README in Step 2 and say so in your report.)

## Step 1: Install Claude Code

- [ ] Install the Claude desktop app from https://claude.com/download, sign in, and open the **Code** tab.

## Step 2: Install the three tools

Open PowerShell (Start menu, type `PowerShell`, Enter). Paste these one at a time. If it asks you to agree to terms, type `Y` and Enter. Say Yes to any Windows permission popup.

```
winget install --id Gyan.FFmpeg -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id Python.Python.3.12 -e
```

- [ ] All three finished with "Successfully installed".

Now close PowerShell, open a NEW PowerShell window and paste these one at a time:

```
ffmpeg -version
node -v
python --version
```

- [ ] `ffmpeg` prints a version, `node` prints v22 or higher, `python` prints Python 3.12.

**If it fails:** copy everything in the PowerShell window and send it.

## Step 3: Put the skill in place

- [ ] In the Code tab, paste `Install this skill for me: https://github.com/tenfoldmarc/video-edit-skill` and press Enter. Allow what it asks.
- [ ] Check: in File Explorer, click the address bar, paste `%USERPROFILE%\.claude\skills\video-edit` and press Enter. The folder opens and contains `SKILL.md`.

## Step 4: Run the machine check by itself

In PowerShell, paste:

```
python "$HOME\.claude\skills\video-edit\scripts\setup.py"
```

The first run takes 1 to 3 minutes (it downloads the transcription tools and six sound effects).

- [ ] The first line says `STATUS system Windows ...`
- [ ] The last line says `READY`

Then paste these two:

```
python "$HOME\.claude\skills\video-edit\tests\test_platform.py"
Get-Content "$HOME\.claude\skills\video-edit\.platform.json"
```

- [ ] The test ends with `OK`.

**Send back either way:** every line the three commands printed.

## Step 5: Restart Claude Code

- [ ] Quit Claude completely (right-click its icon near the clock, Quit) and open it again. This matters: it only sees newly installed programs after a restart.

## Step 6: First run of the skill

In the Code tab, type `/video-edit` and press Enter. Answer its questions (name, Instagram handle, look: pick **bold**, folders: accept the defaults). When Claude asks permission to run a command, allow it.

- [ ] Claude says setup is complete.

**If it fails:** go to "What to send back".

## Step 7: Make the test reel

Paste this:

```
/video-edit I dropped one clip in my Downloads. Make a short test reel from it, 10 seconds max, bold look, no animated inserts.
```

The first reel downloads about 2 GB of speech and cutout models, once. Let it run.

Tick each stage as Claude reports it:

- [ ] It found the clip and showed a transcript
- [ ] It showed the cut list (which lines it kept)
- [ ] It cut you out of the background. This is the slow step on a PC. Note how many minutes it took: ____
- [ ] It showed preview snapshots
- [ ] It rendered the reel and gave you two files: the full render and a phone copy

## Step 8: Watch the result

Open the phone copy (Claude tells you where it is, normally `C:\Users\<you>\reel-edits\...\renders\`).

- [ ] It plays, with your voice in sync
- [ ] Captions are readable, with no garbage characters (things like `â€™` instead of an apostrophe)
- [ ] The big words sit BEHIND your head, not on top of your face
- [ ] At each cut the picture changes cleanly (no double image, no black frame)
- [ ] You can hear the small sound effects, quieter than your voice

## Step 9 (if you have 20 more minutes): the other shell

Claude Code runs commands through PowerShell when Git for Windows is not installed, and through Git Bash when it is. Both need to work.

- [ ] Note whether Git for Windows was installed during steps 6 to 8 (in PowerShell: `git --version`).
- [ ] Switch to the other situation. No Git yet: paste `winget install --id Git.Git -e` in PowerShell, then restart Claude Code. Then repeat Step 7 with the same clip and tick the same boxes.

## Things you may see

- **"Python was not found"** when Claude tries `python3`: normal on Windows, it should move on to `python` by itself.
- **A black window flashing for a moment:** harmless.
- **A Smart App Control or antivirus popup:** screenshot it and send it. This one is a known risk.
- **The cutout step taking many minutes:** expected on a PC. Only report it if it runs over 15 minutes for a 10 second reel, or stops.

## What to send back

Open an issue at https://github.com/tenfoldmarc/video-edit-skill/issues with the items below. Issues are public: your Windows user name shows up in file paths, so replace it (and anything else private) before posting, and do not attach your video unless you are fine with it being public.

1. Windows version, processor, RAM, and whether Git for Windows was installed.
2. Everything printed in Step 4.
3. The number of the first step that failed, if any, and a screenshot of what Claude showed.
4. Ask Claude this and send the file it creates:
   ```
   Write a file on my Desktop called video-edit-windows-report.txt with: every command you ran for /video-edit in this session, in order, and for each one that failed the full error text exactly as printed. Add the contents of .platform.json from the skill folder.
   ```
5. Whether you got a finished reel and how it looked against the Step 8 boxes (a screenshot is enough).
6. How long the background cutout took, and how long the reel is.
