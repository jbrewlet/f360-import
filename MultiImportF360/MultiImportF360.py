"""
Multi-Import F360
Bulk import STEP, IGES, SAT, and SMT files into Fusion 360

Created by Portland CNC
URL: https://pdxcnc.com
Version: 1.0.0
Author: Portland CNC
"""

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


# Global variables to keep handlers in scope
_handlers = []

def run(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Get add-in path - this is the root of the add-in folder
        addinPath = os.path.dirname(os.path.abspath(__file__))
        
        # Use resources/icon folder for command icons
        iconFolder = os.path.join(addinPath, 'resources', 'icon')
        
        # Ensure folder exists and normalize the path
        if os.path.exists(iconFolder):
            iconFolder = os.path.normpath(os.path.abspath(iconFolder))
        else:
            iconFolder = ''
        
        # Remove OLD command definition completely
        oldCmdDef = ui.commandDefinitions.itemById('MultiImportCommand')
        if oldCmdDef:
            # Remove from all panels first
            designWorkspace = ui.workspaces.itemById('FusionSolidEnvironment')
            if designWorkspace:
                solidTab = designWorkspace.toolbarTabs.itemById('SolidTab')
                if solidTab:
                    for panelId in ['InsertPanel', 'SolidInsertPanel', 'SolidScriptsAddinsPanel']:
                        panel = solidTab.toolbarPanels.itemById(panelId)
                        if panel:
                            control = panel.controls.itemById('MultiImportCommand')
                            if control:
                                control.deleteMe()
            oldCmdDef.deleteMe()
        
        # Create NEW command with fresh icon folder path
        # Use absolute path and ensure it's properly formatted
        if iconFolder:
            # Ensure path uses forward slashes (works on both Windows and Mac)
            iconFolder = iconFolder.replace('\\', '/')
        
        # Create command - Fusion 360 will look for 16x16.svg/16x16.png and 32x32.svg/32x32.png
        cmdDef = ui.commandDefinitions.addButtonDefinition(
            'MultiImportCommand',
            'Multi-Import Files',
            'Bulk import STEP, IGES, SAT, and SMT files.\n\nClick to open file browser, then multi-select files for near-instant import.\n\nMade by PDX CNC',
            iconFolder
        )
        
        # Connect to the command created event
        onCommandCreated = MultiImportCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)
        
        # Get the Design workspace
        designWorkspace = ui.workspaces.itemById('FusionSolidEnvironment')
        if not designWorkspace:
            ui.messageBox('ERROR: Could not find Design workspace')
            return
            
        # Get the Solid tab
        solidTab = designWorkspace.toolbarTabs.itemById('SolidTab')
        if not solidTab:
            ui.messageBox('ERROR: Could not find Solid tab')
            return
        
        # Get INSERT panel - try all possible IDs
        insertPanel = solidTab.toolbarPanels.itemById('InsertPanel')
        if not insertPanel:
            insertPanel = solidTab.toolbarPanels.itemById('SolidInsertPanel')
        if not insertPanel:
            insertPanel = solidTab.toolbarPanels.itemById('SolidScriptsAddinsPanel')
        
        if not insertPanel:
            # Debug: list all panel IDs
            msg = 'Available panels:\n'
            for i in range(solidTab.toolbarPanels.count):
                panel = solidTab.toolbarPanels.item(i)
                msg += f'{i}: {panel.id}\n'
            ui.messageBox(msg)
            return
                
        # Remove existing control if it exists
        existingControl = insertPanel.controls.itemById('MultiImportCommand')
        if existingControl:
            existingControl.deleteMe()
        
        # Add command to INSERT panel - showInToolbar=True pins it
        control = insertPanel.controls.addCommand(cmdDef, 'MultiImportCommand', True)
        
        # CRITICAL: Promote to pin to toolbar
        control.isPromoted = True
        control.isPromotedByDefault = True
        
        print(f'Command added and pinned. Icon folder: {iconFolder}')
        print('=== MULTI-IMPORT ADD-IN LOADED SUCCESSFULLY ===')
        
    except Exception as e:
        error_msg = traceback.format_exc()
        print('=== ERROR IN RUN() ===')
        print(error_msg)
        print('======================')
        if ui:
            ui.messageBox('Failed:\n{}'.format(error_msg))

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Get the Design workspace
        designWorkspace = ui.workspaces.itemById('FusionSolidEnvironment')
        if designWorkspace:
            solidTab = designWorkspace.toolbarTabs.itemById('SolidTab')
            if solidTab:
                # Try to find and remove command from INSERT panel
                panelIds = ['SolidInsertPanel', 'InsertPanel', 'SolidCreatePanel']
                for panelId in panelIds:
                    panel = solidTab.toolbarPanels.itemById(panelId)
                    if panel:
                        control = panel.controls.itemById('MultiImportCommand')
                        if control:
                            control.deleteMe()
                            break
                
                # Also check all toolbar panels
                allPanels = ui.allToolbarPanels
                for i in range(allPanels.count):
                    panel = allPanels.item(i)
                    if 'Insert' in panel.id or 'Insert' in panel.name:
                        control = panel.controls.itemById('MultiImportCommand')
                        if control:
                            control.deleteMe()
                            break
        
        # Clean up the command definition
        cmdDef = ui.commandDefinitions.itemById('MultiImportCommand')
        if cmdDef:
            cmdDef.deleteMe()
        
    except Exception as e:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

