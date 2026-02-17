import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class CmdFeatures(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.dangerWords = [
            "del",
            "erase",
            "remove",
            "format",
            "shutdown",
            "diskpart",
            "reg delete",
            "bcdedit",
            "bootrec",
            "attrib -R",
            "icacls",
            "schtasks",
            "malware.exe",
            "payload.exe",
            "winlogon.exe",
            "lsass.exe",
            "WinDefend",
            "regedit",
            "Invoke-WebRequest",
            "curl",
            "wget",
        ]
        self.systemPaths = [
            "c:\\windows",
            "c:\\system32",
            "c:\\",
            "c:\\boot.ini",
            "c:\\importantfile.txt",
        ]
        self.networkKeywords = [
            "\\\\attacker\\",
            "mail",
            "http://",
            "https://",
            "ftp",
            "tftp",
            "Invoke-WebRequest",
            "curl",
            "wget",
        ]

    def fit(self, X, y=None):
        return self

    def transform(self, X: list[str]):
        features = []
        for cmd in X:
            cmdLower = cmd.lower()
            lenth = len(cmd)
            numSleshes = cmd.count("\\") + (cmd.count("/"))
            numAsterisks = cmd.count("*")
            numSpaces = cmd.count(" ")
            dangerousWordCount = sum(word in cmdLower for word in self.dangerWords)
            systemPathCount = sum(path in cmdLower for path in self.systemPaths)
            hasNetwork = int(any(nk in cmdLower for nk in self.networkKeywords))
            features.append(
                [
                    lenth,
                    numSleshes,
                    numAsterisks,
                    numSleshes,
                    numSpaces,
                    dangerousWordCount,
                    systemPathCount,
                    hasNetwork,
                ]
            )
        return np.array(features)
