# Created by Portland CNC
# URL: https://pdxcnc.com

import adsk.core
import adsk.fusion
import traceback
import os


class MultiImportCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
        self._handlers = []
    
    def notify(self, args):
        try:
            cmd = args.command
            onExecute = MultiImportCommandExecuteHandler()
            cmd.execute.add(onExecute)
            # Keep handler in scope
            self._handlers.append(onExecute)
        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class MultiImportCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            design = app.activeProduct
            
            if not design:
                ui.messageBox('No active design. Please open a design first.')
                return
            
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

