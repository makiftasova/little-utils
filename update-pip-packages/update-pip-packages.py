#!/usr/bin/env python3

"""
Tries to update all pip packages tolatest versions.
User should give requried user permissions before running script
(eg. root permissions if pacages are installed system wide)

Requires pip
"""

from  pip.commands import InstallCommand,  ListCommand

__author__ = "Mehmet Akif TAŞOVA"
__copyright__ = "Copyright 2017, Mehmet Akif TAŞOVA"
__credits__ = ["Mehmet Akif TAŞOVA"]
__license__ = "GPL3"
__version__ = "1.0"
__maintainer__ = "Mehmet Akif TAŞOVA"
__email__ = "makiftasova@gmail.com"
__status__ = "Production"

class UpdateCommand(InstallCommand):
    def __init__(self, *args, **kw):
        super(UpdateCommand, self).__init__(*args, **kw)
        self.args = ["--upgrade"]

    def add_package(self, name):
        self.args.append(name)

    def run_update(self):
        self.main(self.args)

class ListOutdatedCommand(ListCommand):

    def __init__(self, *args, **kw):
        super(ListOutdatedCommand, self).__init__(*args, **kw)
        self.output = []
        self.main(["--outdated", "--format=json"])

    def output_package_listing(self, packages, options):
        for dist in packages:
            info = {
                    "name": dist.project_name,
                    "version": str(dist.version),
                    "latest_version": str(dist.latest_version)
                    }
            self.output.append(info)

    def get_output(self):
        return self.output

def ask_yes_or_no(question = "Continue?", default = "no"):
    valid = {"yes": True, "Yes": True, "y": True, "Y": True,
             "no": False, "No": False, "n": False, "N": False}
    if None == default:
        prompt = "[y/n]"
    else:
        default = default.lower()
        if "yes" == default:
            prompt = "[Y/n]"
        elif "no" == default:
            prompt = "[y/N]"
        else:
            raise ValueError("Invalid default answer: {ans}".format(ans=default))

    while True:
        answer = input("{q} {p}>".format(q=question, p=prompt)).lower()
        if default is not None and answer == "":
            return valid[default]
        elif answer in valid:
            return valid[answer]
        else:
            print("Please respons with 'yes' or 'no' (or 'y' or 'n')")


def print_package_list(packages):
    print("Packages to update:")
    for p in packages:
        print("\t{name}: {cur_ver} --> {new_ver}".format(name=p['name'], cur_ver=p['version'], new_ver=p['latest_version']))


def main():
    print("Checking installed packages")
    loc = ListOutdatedCommand()
    packages = loc.get_output()

    if len(packages) == 0:
        print("No packages to update.")
        return
    else:
        print_package_list(packages)
        if ask_yes_or_no():
            print("Updating {num} packages".format(num=len(packages)))
            uc = UpdateCommand()
            for p in packages:
                uc.add_package(p['name'])
            uc.run_update()
        else:
            print("Skipping update")

if "__main__" == __name__:
    main()
