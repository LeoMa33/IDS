import logging
import os
import hashlib
from threading import Thread
from FileInformation import FileInformation

class DirectoryInformation:
    def __init__(self):
        self._directory = ""
        self._size = ""
        self._owner = ""
        self._group = ""
        self._lastEdit = ""
        self._creationDate = ""
        self._MD5 = ""
        self._SHA256 = ""
        self._SHA512 = ""
        self.child = []

    def SetupDirectoryInformation(self, directory, include_child = True)->None:   #async
        self._directory = directory
        try:
            stat = os.stat(self._directory)
        except FileNotFoundError:
            logging.warning(f"{self._directory} not found")
            return
        
        self._size = stat.st_size
        self._owner = stat.st_uid
        self._group = stat.st_gid
        self._lastEdit = stat.st_mtime
        self._creationDate = stat.st_ctime
        self._MD5 = self.GetMD5()
        self._SHA256 = self.GetSHA256()
        self._SHA512 = self.GetSHA512()
        if include_child :
            self.TreatFilesAndDirectory()
    

    def GetMD5(self)->str:   #async
        t= str(os.stat(self._directory)).encode("utf-8")    #Await
        md5 = hashlib.md5(t)     #Await
        
        return md5.hexdigest()
    

    def GetSHA256(self)->str:   #async
        t= str(os.stat(self._directory)).encode("utf-8")     #Await
        sha256 = hashlib.sha256(t)     #Await
        
        return sha256.hexdigest()
    

    def GetSHA512(self)->str:   #async
        t= str(os.stat(self._directory)).encode("utf-8")     #Await
        sha512 = hashlib.sha512(t).hexdigest()     #Await
        
        return sha512
    

    def GetSelfInformation(self):
        f = FileInformation()
        f._file = self._directory
        f._size = self._size
        f._owner = self._owner
        f._group = self._group
        f._lastEdit = self._lastEdit
        f._creationDate = self._creationDate
        f._MD5 = self._MD5
        f._SHA256 = self._SHA256
        f._SHA512 = self._SHA512
        return f
    
    
    def TreatFilesAndDirectory(self):
        for childName in os.listdir(self._directory):
            pathToCheck = f"{self._directory}/{childName}"
            thread = Thread(target=self.TreatPath, args=[pathToCheck])
            thread.run()
    
    
    def TreatPath(self, pathToCheck):   #async
        if not os.path.exists(pathToCheck):
            logging.warning(f"{pathToCheck} not found")
            return
        if os.path.isdir(pathToCheck):
            dirInf = DirectoryInformation()
            dirInf.SetupDirectoryInformation(directory=pathToCheck)

            f = dirInf.GetSelfInformation()
            for file in dirInf.__dict__["child"]:
                 self.child.append(file)
            
            self.child.append(f.__dict__)
        elif os.path.isfile(pathToCheck):
            f = FileInformation()
            f.SetupFileInformation(file=pathToCheck)
            self.child.append(f.__dict__)     #Await
        logging.info(f"{pathToCheck} check")
