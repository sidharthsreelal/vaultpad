# vaultpad

A notepad-adjacent calculator utility. Does basic math. Also mounts encrypted VeraCrypt volumes if you know the right keysequence.

Looks like a calculator. Acts like a calculator. Just has a second job.

---

## what it does

- Fully functional calculator (add, subtract, multiply, divide, percent, decimals)
- Hidden trigger: type a configurable key sequence (default `1 3 0 0 1 3 =`) and a password prompt appears
- Correct password → mounts your real encrypted volume
- Decoy password → mounts a separate decoy volume instead
- Wrong password → generic "Access Denied" warning, nothing else happens
- Mounting happens in a background thread so the UI doesn't freeze

---

## setup

**Requirements:**
- Python 3.x (tkinter is included in the standard install on Windows)
- [VeraCrypt](https://veracrypt.fr/en/Downloads.html) installed

**Steps:**

1. Clone or download this repo
2. Open `vaultpad.py` and edit the variables at the top of the file (clearly marked)
3. Run it:

```
python vaultpad.py
```

That's it.

---

## configuration

All the stuff you'd want to change is grouped at the top of the file under the `USER-CONFIGURABLE VARIABLES` section:

```python
CONTAINER_PATH = r"D:\path\to\your\real.hc"
DECOY_PATH     = r"D:\path\to\your\decoy.hc"

MAIN_DRIVE  = "X:"   # drive letter for real volume
DECOY_DRIVE = "Y:"   # drive letter for decoy volume

MAIN_PASS  = "yourpassword"
DECOY_PASS = "yourfakepassword"

CRYPT_PATH = r"C:\Program Files\VeraCrypt\VeraCrypt.exe"

COMBO_KEYS = ['1', '3', '0', '0', '1', '3', '=']  # trigger sequence
```

Change the combo to whatever sequence feels natural to you. Just make sure it's something you'd plausibly type on a calculator so it doesn't look weird.

---

## decoy volume

The decoy system relies on VeraCrypt's hidden volume feature. Basically:

- One `.hc` container file = one password = your real data
- Second `.hc` container file = different password = fake/empty data
- From the outside they look identical

If you're not familiar with setting this up, the [VeraCrypt documentation](https://veracrypt.fr/en/Hidden%20Volume.html) covers it well.

---

## notes

- The calculator remembers the last expression above the main display, like most modern calcs
- Operator stacking is handled (pressing `+ -` will just replace the `+`)
- Result display cleans up floats — `4.0` shows as `4`, etc.
- The window is intentionally not resizable, keeps it looking like a plain utility app

---

## known limitations

- Windows only (relies on VeraCrypt's CLI and Windows drive letters)
- No history, no scientific functions — it's meant to look basic on purpose
- The password prompt is a standard dialog box; not much you can do about that with tkinter

---

## license

Do whatever you want with it.
