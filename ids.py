import argparse
import logging
import json
import time
from os import path
from datetime import datetime
from threading import Thread
from FileInformation import FileInformation
from DirectoryInformation import DirectoryInformation
from Report import Report
from discord_webhook import DiscordWebhook, DiscordEmbed

treatfilereport = []


def TreatFilesAndDirectory() -> list:
    global CONFIG
    for pathToCheck in CONFIG["toCheck"]:
        thread = Thread(target=TreatPath, args=[pathToCheck])
        thread.run()
    return treatfilereport


def TreatPath(pathToCheck):
    global treatfilereport
    if not path.exists(pathToCheck):
        logging.warning(f"{pathToCheck} not found")
        return
    if path.isdir(pathToCheck):
        dirInf = DirectoryInformation()
        dirInf.SetupDirectoryInformation(directory=pathToCheck)
        f = dirInf.GetSelfInformation()

        for file in dirInf.__dict__["child"]:
            treatfilereport.append(file)

        treatfilereport.append(f.__dict__)

    elif path.isfile(pathToCheck):
        f = FileInformation()
        f.SetupFileInformation(file=pathToCheck)
        treatfilereport.append(f.__dict__)
    logging.info(f"{pathToCheck} check")


def WriteReport(report: Report, file, result):
    if isinstance(report, dict):
        report.AddDivergence(file, result)
        return
    if all([not isinstance(x, dict) for x in result]):
        return
    report.AddDivergence(file, result)


def Build() -> None:
    global CONFIG
    logging.info("Build start")

    files_informations = TreatFilesAndDirectory()

    logging.info("Build end")

    json_report = json.dumps(files_informations, separators=(",", ":"))

    with open(CONFIG["buildFile"], "w") as outfile:
        outfile.write(json_report)
        logging.info("Build report write")


def Check():
    global CONFIG
    report = Report()
    logging.info("Check start")

    with open(CONFIG["buildFile"], "r") as infile:
        json_build = json.load(infile)
        infile.close()

    for file in json_build:

        pathToCheck = file["_file"]

        if not path.exists(pathToCheck):
            WriteReport(report, pathToCheck, {"Warning": "Not Found"})
        if path.isdir(pathToCheck):
            dirInf = DirectoryInformation()
            dirInf.SetupDirectoryInformation(directory=pathToCheck, include_child=False)
            f = dirInf.GetSelfInformation()
            WriteReport(report, pathToCheck, f.CheckEqual(file))

        elif path.isfile(pathToCheck):
            f = FileInformation()
            f.SetupFileInformation(file=pathToCheck)
            WriteReport(report, pathToCheck, f.CheckEqual(file))
        logging.info(f"{pathToCheck} check")

    logging.info("Check end")
    if report.state != "ok":

        message = ""

        for fd in report.divergence.keys():
            message += f"\n**->** {fd}"

        wh = DiscordWebhook(url=CONFIG["discord_webhook"])

        embed = DiscordEmbed(title="[  IDS Alerte  ]", description="**Différence trouvé**", color="CB0000")
        embed.add_embed_field(name="Fichiers|Dossiers concernés", value=message)
        embed.set_footer(text=f"Rapport de vérification  •  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        wh.add_embed(embed)
        response = wh.execute()
    report.WriteReportInFile(CONFIG["reportsFolder"])


def GetConf() -> dict:
    configFile = open("conf.json")
    configData = json.load(configFile)
    configFile.close()
    return configData


CONFIG = GetConf()

parser = argparse.ArgumentParser()

parser.add_argument(
    "--build", help="Build file state in json file", action="store_true"
)
parser.add_argument(
    "--check", help="Check file state in json file", action="store_true"
)

args = parser.parse_args()

logging.basicConfig(
    level=logging.DEBUG,
    filename=CONFIG["logFile"],
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)


def main() -> None:
    if args.build:
        Build()

    if args.check:
        Check()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
