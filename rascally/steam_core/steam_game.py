import binascii


class SteamGame():
    """ Class to instance a SteamGame
    """

    def __init__(
        self,
        AppName: str,
        Exe: str,
        appid=0,
        StartDir="./",
        icon="",
        ShortcutPath="",
        LaunchOptions="",
        IsHidden=0,
        AllowDesktopConfig=1,
        AllowOverlay=1,
        OpenVR=0,
        Devkit=0,
        DevkitGameID="",
        DevkitOverrideAppID=0,
        LastPlayTime=0,
        FlatpakAppID="",
        tags={},
    ) -> None:

        self.appid = appid if appid != 0 else SteamGame.generate_app_id(Exe, AppName)
        self.AppName = AppName
        self.Exe = Exe
        self.StartDir = StartDir
        self.icon = icon
        self.ShortcutPath = ShortcutPath
        self.LaunchOptions = LaunchOptions
        self.IsHidden = IsHidden
        self.AllowDesktopConfig = AllowDesktopConfig
        self.AllowOverlay = AllowOverlay
        self.OpenVR = OpenVR
        self.Devkit = Devkit
        self.DevkitGameID = DevkitGameID
        self.DevkitOverrideAppID = DevkitOverrideAppID
        self.LastPlayTime = LastPlayTime
        self.FlatpakAppID = FlatpakAppID
        self.tags = tags

    def __repr__(self) -> str:
        return self.get_SteamGame().__str__()

    def get_SteamGame(self) -> dict:
        return {
            'appid': int(self.appid),
            'AppName': str(self.AppName),
            'Exe': str(self.Exe),
            'StartDir': str(self.StartDir),
            'icon': str(self.icon),
            'ShortcutPath': str(self.ShortcutPath),
            'LaunchOptions': str(self.LaunchOptions),
            'IsHidden': int(self.IsHidden),
            'AllowDesktopConfig': int(self.AllowDesktopConfig),
            'AllowOverlay': int(self.AllowOverlay),
            'OpenVR': int(self.OpenVR),
            'Devkit': int(self.Devkit),
            'DevkitGameID': str(self.DevkitGameID),
            'DevkitOverrideAppID': int(self.DevkitOverrideAppID),
            'LastPlayTime': int(self.LastPlayTime),
            'FlatpakAppID': str(self.FlatpakAppID),
            'tags': dict(self.tags)
        }

    def get_appid_human(self) -> int:
        return self.appid + 2**32
    
    def set_name(self,s:str) -> None:
        self.AppName = s
    
    def set_exe(self,s:str) -> None:
        self.Exe = s
    
    def set_startDir(self, sd:str) -> None:
        self.StartDir = sd
    
    def set_launchOptions(self, lo:str) -> None:
        self.LaunchOptions = lo
    
    @staticmethod
    def generate_app_id(exe: str, name: str) -> int:
        key = exe + name
        crcValue = binascii.crc32(key.encode())
        top = int(crcValue) | 0x80000000
        return top - 2**32
    
    @staticmethod
    def dict_to_game(dicc:dict) -> 'SteamGame':
        try:
            return SteamGame(
                appid = dicc['appid'],
                AppName = dicc['AppName'],
                Exe = dicc['Exe'],
                StartDir = dicc['StartDir'],
                icon = dicc['icon'],
                ShortcutPath = dicc['ShortcutPath'],
                LaunchOptions = dicc['LaunchOptions'],
                IsHidden = dicc['IsHidden'],
                AllowDesktopConfig = dicc['AllowDesktopConfig'],
                AllowOverlay = dicc['AllowOverlay'],
                OpenVR = dicc['OpenVR'],
                Devkit = dicc['Devkit'],
                DevkitGameID = dicc['DevkitGameID'],
                DevkitOverrideAppID = dicc['DevkitOverrideAppID'],
                LastPlayTime = dicc['LastPlayTime'],
                FlatpakAppID = dicc['FlatpakAppID'],
                tags = dicc['tags']
            )
        except:
            return SteamGame()