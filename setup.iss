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

DisableWelcomePage=no
DisableProgramGroupPage=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "{#MyAppSource64}\*"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs; \
    Check: Is64BitInstallMode

Source: "{#MyAppSource32}\*"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs; \
    Check: not Is64BitInstallMode

[Registry]
Root: HKLM; \
    Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; \
    ValueName: "Path"; \
    ValueData: "{code:GetUpdatedPath}"; \
    Check: ShouldAddToPath

[Code]

var
  PathPage: TWizardPage;
  PathCheckBox: TNewCheckBox;
  OriginalPath: String;

function IsPathAlreadyPresent(Path: String): Boolean;
var
  SearchPath: String;
begin
  SearchPath := ';' + OriginalPath + ';';

  Result :=
    Pos(';' + Path + ';', SearchPath) > 0;
end;

function ShouldAddToPath(): Boolean;
begin
  Result :=
    PathCheckBox.Checked and
    (not IsPathAlreadyPresent(ExpandConstant('{app}')));
end;

function GetUpdatedPath(Param: String): String;
begin
  if OriginalPath = '' then
    Result := ExpandConstant('{app}')
  else if IsPathAlreadyPresent(ExpandConstant('{app}')) then
    Result := OriginalPath
  else
    Result := OriginalPath + ';' + ExpandConstant('{app}');
end;

procedure InitializeWizard;
begin
  { Read current system PATH }
  RegQueryStringValue(
    HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path',
    OriginalPath
  );

  { PATH configuration page }
  PathPage := CreateCustomPage(
    wpSelectDir,
    'PATH Configuration',
    'Choose whether ICON1K should be added to the system PATH.'
  );

  PathCheckBox := TNewCheckBox.Create(PathPage);
  PathCheckBox.Parent := PathPage.Surface;

  PathCheckBox.Left := ScaleX(0);
  PathCheckBox.Top := ScaleY(10);

  PathCheckBox.Width := PathPage.SurfaceWidth;
  PathCheckBox.Height := ScaleY(40);

  PathCheckBox.Caption :=
    'Add ICON1K to the system PATH';

  PathCheckBox.Checked := True;
end;
