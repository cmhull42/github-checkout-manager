import subprocess, os, json, distutils
import distutils.dir_util

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

        repodirectory = os.path.join(os.path.expanduser(foundrepo["configdirectory"]), foundrepo["name"])
        scriptdirectory = os.path.dirname(os.path.realpath(__file__))

        myenv = os.environ.copy()

        deploykey = foundrepo.get("deploykeypath", "")
        if deploykey:
            myenv["GIT_SSH"] = scriptdirectory + os.pathsep + "ssh-wrapper.sh"
        
        subprocess.run("git reset --hard origin/master".split(), cwd=repodirectory, env=myenv)
        subprocess.run("git pull origin master".split(), cwd=repodirectory, env=myenv)

        # copy_tree caches directory structures it's created so if the folder has been deleted
        # since the last call, it will fail. weird bug.
        # so next line clears the cache
        distutils.dir_util._path_created = {}

        distutils.dir_util.copy_tree(repodirectory, os.path.expanduser(foundrepo["contentdirectory"]))