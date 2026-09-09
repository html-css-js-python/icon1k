#define MyAppName "ICON1K"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "html-css-js-python"
#define MyAppExeName "ICON1K.exe"

#define MyAppSource32 "x86\ICON1K"
#define MyAppSource64 "x64\ICON1K"

[Setup]
AppId={{AA03DAB7-D6FF-4C4A-BA7C-7F70773B38A1}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

OutputDir=installer
OutputBaseFilename={#MyAppName}_Setup

Compression=lzma2
SolidCompression=yes
WizardStyle=modern

UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "{#MyAppSource64}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: Is64BitInstallMode
Source: "{#MyAppSource32}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: not Is64BitInstallMode

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; \
    ValueData: "{olddata};{app}"; \
    Check: NeedsAddPath

[Code]
function NeedsAddPath(): Boolean;
var
  CurrentPath: String;
begin
  CurrentPath := ExpandConstant('{olddata}');
  Result := Pos(';' + ExpandConstant('{app}') + ';', ';' + CurrentPath + ';') = 0;
end;

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
