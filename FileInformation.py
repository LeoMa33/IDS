import logging
import os
import hashlib

class FileInformation:
    def __init__(self):
        self._file = ""
        self._SHA512 = ""
        self._SHA256 = ""
        self._MD5 = ""
        self._lastEdit = ""
        self._creationDate = ""
        self._owner = ""
        self._group = ""
        self._size = ""


    def SetupFileInformation(self, file)->None:   #async
        self._file = file
        try:
            stat = os.stat(self._file)
        except FileNotFoundError:
            logging.warning(f"{self._file} not found")
            return
        
        self._size = stat.st_size
        self._owner = stat.st_uid
        self._group = stat.st_gid
        self._lastEdit = stat.st_mtime
        self._creationDate = stat.st_ctime
        self._MD5 = self.GetMD5()
        self._SHA256 = self.GetSHA256()
        self._SHA512 = self.GetSHA512()
    

    def GetMD5(self)->str:   #async
        with open(self._file, "rb") as file:
            fileContent = file.read()     #Await
            md5 = hashlib.md5(fileContent)     #Await
        
        return md5.hexdigest()
    

    def GetSHA256(self)->str:   #async
        with open(self._file, "rb") as file:
            fileContent = file.read()     #Await
            sha256 = hashlib.sha256(fileContent)     #Await
        
        return sha256.hexdigest()
    

    def GetSHA512(self)->str:   #async
        with open(self._file, "rb") as file:
            fileContent = file.read()     #Await
            sha512 = hashlib.sha512(fileContent)     #Await
        
        return sha512.hexdigest()
    
    
    def CheckEqual(self, other):
        file = self._file, other["_file"]
        if not file:
            file = {"new":self._file, "old":other["_file"]}
        eSHA512 = self._SHA512 == other["_SHA512"]
        if not eSHA512:
            eSHA512 = {"new":self._SHA512, "old":other["_SHA512"]}
        eSHA256 = self._SHA256 == other["_SHA256"]
        if not eSHA256:
            eSHA256 = {"new":self._SHA256, "old":other["_SHA256"]}
        eMD5 = self._MD5 == other["_MD5"]
        if not eMD5:
            eMD5 = {"new":self._MD5, "old":other["_MD5"]}
        lastEdit = self._lastEdit == other["_lastEdit"]
        if not lastEdit:
            lastEdit = {"new":self._lastEdit, "old":other["_lastEdit"]}
        creationDate = self._creationDate == other["_creationDate"]
        if not creationDate:
            creationDate = {"new":self._creationDate, "old":other["_creationDate"]}
        owner = self._owner == other["_owner"]
        if not owner:
            owner = {"new":self._owner, "old":other["_owner"]}
        group = self._group == other["_group"]
        if not group:
            group = {"new":self._group, "old":other["_group"]}
        size = self._size == other["_size"]
        if not size:
            size = {"new":self._size, "old":other["_size"]}

        return (file, eSHA512, eSHA256, eMD5, lastEdit, creationDate, owner, group, size)