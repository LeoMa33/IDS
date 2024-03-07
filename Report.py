from json import dumps, load
from logging import info

class Report:

    Car = ["file", "eSHA512", "eSHA256", "eMD5", "lastEdit", "creationDate", "owner", "group", "size"]

    def __init__(self):
        self.state = "ok"
    
    def AddDivergence(self, file,report):
        if not hasattr(self, 'divergence'):
            self.divergence = {}
        self.state = "divergent"
        self.divergence[file] = {}
        if isinstance(report,dict):
            self.divergence[file] = report
            return
        for i, carRes in enumerate(report):
            if isinstance(carRes, dict):
                self.divergence[file][Report.Car[i]] = carRes
    
    
    def WriteReportInFile(self, folder):
        try:
            with open(f"{folder}/check.json", "r+") as outfile:
                self.Write(outfile)
        except:
            with open(f"{folder}/check.json", "+a") as outfile:
                self.Write(outfile)
    
    
    def Write(self, file):
        try:
            reports = load(file)
        except Exception as e:
            print(e)
            reports = {}
        file.seek(0)
        reports[len(reports.keys())] = self.__dict__

        file.write(dumps(reports, separators=(",",":")))
        file.truncate()
        info("Check report write") 
