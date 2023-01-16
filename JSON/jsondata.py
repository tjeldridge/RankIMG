import json
from os.path import isfile, isdir
from os import mkdir


class jsondata:
    def __init__(self, json_file: str = "data.json"):
        self.json_file = "JSON/" + json_file
        self.json_log_file = "JSON/" + json_file[:-5] + "_log.json"
        self.competitors = {}
        self.competition_log = {}
        self.load_data()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def load_data(self):
        try:
            with open(self.json_file) as infile:
                self.competitors = json.load(infile)
            with open(self.json_log_file) as infile_log:
                self.competition_log = json.load(infile_log)
        except IOError:
            self.store_data()

    def update_data(self):
        self.store_data(overwrite=True)

    def store_data(self, overwrite: bool = False):
        # Competitor File
        create_json(self.json_file, self.competitors, overwrite=overwrite)
        # Competition Log File
        create_json(self.json_log_file, self.competition_log, overwrite=overwrite, sort=True)

    def transfer_logs(self):
        for key, value in self.competitors.items():
            try:
                for logkey, logvalue in value["competition log"].items():
                    self.competition_log[key][logkey] = logvalue
                value.pop("competition log")
            except KeyError as KE:
                print("Cannot transfer logs because keyword %s is not among competitor items." % KE)
        self.update_data()


def create_json(filename: str, data: dict, overwrite: bool = False, sort: bool = False):
    if any([not isfile(filename), overwrite]):
        with open(filename, "w") as outfile:
            json.dump(data, outfile, sort_keys=sort, indent=4)
    else:
        raise FileExistsError("The file '%s' already exists and cannot be overwritten." % filename)


def autonamejson(directory: str, character: str = None) -> str:
    if character is not None:
        chardir = "JSON/" + character
        if not isdir(chardir):
            mkdir(chardir)
        character += "/"
    else:
        character = ""
    dirname = directory.split("/")[-1]
    jsonname = character + dirname + ".json"
    return jsonname

# End
