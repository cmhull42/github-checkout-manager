import subprocess, os, json
from distutils.dir_util import copy_tree

class DeploymentManager:
    def __init__(self):
        # yeah this is not a very good solution. can't find a good way to structure the dependencies
        with open("config.json", "r") as f:
            self.repoconfig = json.loads(f.read())

    def receivepush(self, pushdata):
        pushedrepo = pushdata["repository"]["full_name"]
        foundrepo = None
        for repo in self.repoconfig["repos"]:
            canonicalname = repo["user"] + "/" + repo["name"]
            if (pushedrepo == canonicalname):
                foundrepo = repo
                break
        else:
            # no repo with that name configured
            print("Received a push for a repo with no configuration! (" + pushedrepo + "). Check that you have a definition for this repo in your config.")
            return

        repodirectory = os.path.expanduser(foundrepo["repodirectory"])

        myenv = os.environ.copy()

        deploykey = foundrepo.get("deploykeypath", "")
        if deploykey:
            myenv["GIT_SSH_COMMAND"] = "ssh -i " + deploykey
        
        subprocess.run("git reset --hard origin/master".split(), cwd=repodirectory, env=myenv)
        subprocess.run("git pull origin master".split(), cwd=repodirectory, env=myenv)

        copy_tree(repodirectory, os.path.expanduser(foundrepo["contentdirectory"]))