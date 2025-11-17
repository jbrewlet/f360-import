# Fusion 360 Batch File Importer

**This add-in makes for super quick and direct bulk file imports to Fusion 360.**

- Imports multiple file formats in bulk: **STEP**, **IGES**, **SAT**, and **SMT** files
- Creates a component for each file and names the component the file name.
- Reports the number of successful and failed imports via a message box
  - Lists Failed files - (tip: screenshot this)


![Import](./assets/multi-import.gif)

![Fails](./assets/multi-import-fail-files.png)

## Installation - Add-in (Recommended)

1. **Download the Add-in**: Clone or download this GitHub repo to get the add-in folder.
2. **Fire Up Fusion 360**: Open Fusion 360 and go to `Tools > Add-ins`.
3. **Add Add-in**: In the `Scripts and Add-Ins` dialog, click the green `+` button and choose "Add Add-in".
4. **Select the Folder**: Navigate to the `MultiImportF360` folder in this repository and select it.
5. **Enable the Add-in**: Check the box next to "Multi-Import F360" to enable it.
6. **Access the Command**: The "Multi-Import Files" command will appear in:
   - The Tools toolbar
   - The Tools menu

### Note for Teams

- Stick the add-in folder in a shared location (Google Drive / Dropbox) so the whole team can easily access it.
- Each team member needs to add the add-in from the shared location.

## Installation - Script (Legacy)

If you prefer to use the standalone script instead of the add-in:

1. **Download the Script**: Use the `Multi-Import-F360.py` file from this repo.
2. **Fire Up Fusion 360**: Open Fusion 360 and go to `Tools > Add-ins`.
3. **Add Script**: In the `Scripts and Add-Ins` dialog, click the green `+` button or choose "Add Script".
4. **Find the File**: Navigate to the folder where you downloaded the script and select it. 
  - I'd suggest moving the file to a better location than the Downloads folder.
5. **Run It**: After the script shows up in your add-ins list, hit the `Run` button.
6. **Check It**: You'll see a message box with the number of successful and failed imports.

### Watch our Tutorial Video
[![Fastest Fusion 360 STEP Import](https://img.youtube.com/vi/7SlQlq7Tulg/maxresdefault.jpg)](https://www.youtube.com/watch?v=7SlQlq7Tulg)
[Watch Video](https://www.youtube.com/watch?v=7SlQlq7Tulg)

---


## How to Use

### Using the Add-in (Recommended)

1. **Access the Command**:
   - Click the "Multi-Import Files" button in the Tools toolbar, OR
   - Go to `Tools > Multi-Import Files` from the menu
2. **Select Files**: Finder or Explorer opens. Select one or multiple supported files (STEP, IGES, SAT, or SMT files) and confirm.
3. **Import**: Watch as the files import in no time without any uploading or processing needed.
4. **Review Results**: You'll see a message box with the number of successful and failed imports.

### Using the Script (Legacy)

1. **Open Script**:
   - Type `s` on keyboard to search, then "Script" to open Scripts and Add-ins.
   - Find Multi-Import-F360
2. **Run**: Click the `Run` button
3. **Select Files**: Finder or Explorer opens. Select one or multiple supported files (STEP, IGES, SAT, or SMT files) and confirm.
4. **Import**: Watch as the files import in no time without any uploading or processing needed.
5. **Review Results**: You'll see a message box with the number of successful and failed imports.


---
[pdxcnc.com](https://pdxcnc.com?ref=multi-import-github)
