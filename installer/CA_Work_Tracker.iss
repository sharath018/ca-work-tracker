; Inno Setup script template for CA Work Tracker
[Setup]
AppName=CA Work Tracker
AppVersion={#emit:AppVersion}
DefaultDirName={pf}\CA Work Tracker
DefaultGroupName=CA Work Tracker
OutputBaseFilename=CA_Work_Tracker_Installer
Compression=lzma
SolidCompression=yes

[Files]
; Adjust the Source path to point to the PyInstaller --onedir output (dist\CA_Work_Tracker\)
Source: "dist\CA_Work_Tracker\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\CA Work Tracker"; Filename: "{app}\main.exe"
Name: "{commondesktop}\CA Work Tracker"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\main.exe"; Description: "Launch CA Work Tracker"; Flags: nowait postinstall skipifsilent
