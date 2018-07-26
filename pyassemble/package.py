# To support both python 2 and python 3
from __future__ import division, print_function, unicode_literals

import shlex
import subprocess
import os
from setuptools import Command
import shutil

WHEELHOUSE = "wheelhouse"


class Package(Command):
    """Package Code and Dependencies into wheelhouse"""
    description = "Run wheels for dependencies and submodules dependencies"
    user_options = []

    def __init__(self, dist):
        Command.__init__(self, dist)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def localize_requirements():
        """
        After the package is unpacked at the target destination,
        pip install -r requirements.txt --no-index --find-links wheelhouse
        or

        Since the original requirements.txt might have links to a non pip repo such as github
        (https) it will parse the links for the archive from a url and not from the wheelhouse.

        This functions creates a new requirements.txt with the only name and version for each of
        the packages, thus eliminating the need to fetch / parse links from http sources and install
        all archives from the wheelhouse.
        """
        # remove empty item (None)
        dependencies = filter(None, open("requirements.txt").read().split("\n"))
        local_dependencies = []

        for dependency in dependencies:
            # https://pip.readthedocs.io/en/1.1/requirements.html
            if dependency:
                if "egg=" in dependency: # may contain git, in this case split by "egg="
                    pkg_name = dependency.split("egg=")[-1]
                    local_dependencies.append(pkg_name)
                elif "git+" in dependency:
                    pkg_name = dependency.split("/")[-1].split(".")[0]
                    local_dependencies.append(pkg_name)
                else:
                    local_dependencies.append(dependency)

        print("local packages in wheel: %s" % local_dependencies)
        os.rename("requirements.txt", "requirements.orig")

        with open("requirements.txt", "w") as requirements_file:
            requirements_file.write("\n".join(local_dependencies))

    @staticmethod
    def execute(command, capture_output=False):
        """
        The execute command will loop and keep on reading the stdout and check for the return code
        and displays the output in real time.
        """

        print("Running shell command: %s" % command)

        if capture_output:
            return subprocess.check_output(shlex.split(command))

        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)

        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        return_code = process.poll()

        if return_code != 0:
            print("Error running command %s - exit code: %s" % (command, return_code))
            raise IOError("Shell Command Failed")

        return return_code

    @staticmethod
    def restore_requirements_txt():
        if os.path.exists("requirements.orig"):
            print("Restoring original requirements.txt file")
            os.remove("requirements.txt")
            os.rename("requirements.orig", "requirements.txt")

    def run(self):
        print("recreate {0} directory".format(WHEELHOUSE))
        shutil.rmtree(WHEELHOUSE, ignore_errors=True)
        os.makedirs(WHEELHOUSE)
        print("Packing dependencies in requirements.txt into wheelhouse")
        self.execute("pip wheel --wheel-dir={dir} -r requirements.txt".format(dir=WHEELHOUSE))
        print("Generating local requirements.txt")
        self.localize_requirements()
        print("Packing code and wheelhouse into dist")
        self.run_command("sdist")
        self.restore_requirements_txt()
