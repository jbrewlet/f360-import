# Created by Portland CNC
# URL: https://pdxcnc.com

import adsk.core, adsk.fusion, traceback
import os

def run(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        # Counters for imported files and a list for failed imports by name
        success_count = 0
        fail_count = 0
        failed_files = []

        # Create a file dialog to select supported files
        fileDialog = ui.createFileDialog()
        fileDialog.title = 'Select Files to Import'
        fileDialog.filter = 'All Supported (*.stp; *.step; *.igs; *.iges; *.sat; *.smt; *.smb);;STEP Files (*.stp; *.step);;IGES Files (*.igs; *.iges);;SAT Files (*.sat);;SMT Files (*.smt; *.smb)'
        fileDialog.filterIndex = 0
        fileDialog.isMultiSelectEnabled = True
        dialogResult = fileDialog.showOpen()
        
        if dialogResult == adsk.core.DialogResults.DialogOK:
            filenames = fileDialog.filenames
            for filename in filenames:
                try:
                    # Extract the file name without extension to use as the component name
                    componentName = os.path.splitext(os.path.basename(filename))[0]
                    
                    # Get file extension to determine import method
                    fileExt = os.path.splitext(filename)[1].lower()
                    
                    # Import the file directly into the root component using appropriate method
                    importOptions = None
                    if fileExt in ['.stp', '.step']:
                        importOptions = app.importManager.createSTEPImportOptions(filename)
                    elif fileExt in ['.igs', '.iges']:
                        importOptions = app.importManager.createIGESImportOptions(filename)
                    elif fileExt == '.sat':
                        importOptions = app.importManager.createSATImportOptions(filename)
                    elif fileExt in ['.smt', '.smb']:
                        importOptions = app.importManager.createSMTImportOptions(filename)
                    else:
                        # Unsupported file type
                        fail_count += 1
                        failed_files.append(os.path.basename(filename))
                        print(f'Unsupported file type: {os.path.basename(filename)}')
                        continue
                    
                    app.importManager.importToTarget(importOptions, rootComp)

                    # Find the last created occurrence and rename it
                    lastOcc = rootComp.occurrences[-1]
                    lastOcc.component.name = componentName

                    # Increment successful import count
                    success_count += 1

                except Exception as e:
                    # Increment fail count for this file and add its base name to the failed_files list
                    fail_count += 1
                    failed_files.append(os.path.basename(filename))
                    print(f'Error importing {os.path.basename(filename)}: {str(e)}')  # Optional: Log the specific error to the console

            # Modify the message box to include information about failed file names
            if failed_files:
                failed_message = '\n'.join(failed_files)
                ui.messageBox(f'{success_count} files imported successfully\n{fail_count} files failed\n\nFAILED:\n{failed_message}')
            else:
                ui.messageBox(f'{success_count} files imported successfully.\n{fail_count} files failed')

        else:
            ui.messageBox('No file selected')

    except Exception as e:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
