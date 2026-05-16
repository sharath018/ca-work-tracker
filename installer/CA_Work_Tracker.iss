; Inno Setup script template for CA Work Tracker
#ifndef AppVersion
#define AppVersion "1.0.0"
#endif

[Setup]
AppName=CA Work Tracker
AppVersion={#AppVersion}
DefaultDirName={pf}\CA Work Tracker
DefaultGroupName=CA Work Tracker
OutputDir=output
OutputBaseFilename=CA_Work_Tracker_Installer
Compression=lzma
SolidCompression=yes

[Files]
; Adjust the Source path to point to the PyInstaller --onedir output (dist\CA_Work_Tracker\)
Source: "dist\CA_Work_Tracker\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Icons]
Name: "{group}\CA Work Tracker"; Filename: "{app}\main.exe"
Name: "{commondesktop}\CA Work Tracker"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\main.exe"; Description: "Launch CA Work Tracker"; Flags: nowait postinstall skipifsilent
