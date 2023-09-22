# Created by Portland CNC
# URL: https://pdxcnc.com

import adsk.core, adsk.fusion, traceback
import os

def run(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        # Counters for imported files
        success_count = 0
        fail_count = 0

        # Create a file dialog to select STEP, IGS, files
        fileDialog = ui.createFileDialog()
        fileDialog.title = 'Select STEP, IGS Files'
        fileDialog.filter = 'STEP Files (*.stp; *.step; *.igs; *.iges)'
        fileDialog.filterIndex = 0
        fileDialog.isMultiSelectEnabled = True
        dialogResult = fileDialog.showOpen()
        
        if dialogResult == adsk.core.DialogResults.DialogOK:
            filenames = fileDialog.filenames
            for filename in filenames:
                try:
                    # Extract the file name without extension to use as the component name
                    componentName = os.path.splitext(os.path.basename(filename))[0]
                    
                    # Import the file directly into the root component
                    importOptions = app.importManager.createSTEPImportOptions(filename)
                    app.importManager.importToTarget(importOptions, rootComp)

                    # Find the last created occurrence and rename it
                    lastOcc = rootComp.occurrences[-1]
                    lastOcc.component.name = componentName

                    # Increment successful import count
                    success_count += 1

                except:
                    # Increment fail count for this file
                    fail_count += 1

            ui.messageBox(f'{success_count} files imported successfully. {fail_count} files failed.')

        else:
            ui.messageBox('No file selected')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
