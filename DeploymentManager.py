import subprocess, os, json, distutils, shutil
import distutils.dir_util

class DeploymentManager:
    def __init__(self):
        # yeah this is not a very good solution. can't find a good way to structure the dependencies
        scriptdirectory = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(scriptdirectory, "config.json"), "r") as f:
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
        
        if foundrepo.get("type", "") == "go":
            self.do_go_update(foundrepo)
        else:
            self.do_raw_copy(foundrepo)

    def do_raw_copy(self, repo):
        configdirectory = os.path.expanduser(repo["configdirectory"])
        repodirectory = os.path.join(configdirectory, repo["name"])
        scriptdirectory = os.path.dirname(os.path.realpath(__file__))

        myenv = os.environ.copy()
        myenv["GIT_SSH"] = os.path.join(scriptdirectory, "ssh-wrapper.sh")

        deploykey = os.path.join(configdirectory, "id_rsa")

        if os.path.isfile(deploykey):
            print ("Found key: " + deploykey)
            myenv["GIT_SSH_COMMAND"] = "ssh -o StrictHostKeyChecking=no -i " + os.path.expanduser(deploykey)

        subprocess.run("git reset --hard origin/master".split(), cwd=repodirectory, env=myenv)
        subprocess.run("git pull origin master".split(), cwd=repodirectory, env=myenv)

        # copy_tree caches directory structures it's created so if the folder has been deleted
        # since the last call, it will fail. weird bug.
        # so next line clears the cache
        distutils.dir_util._path_created = {}

        distutils.dir_util.copy_tree(repodirectory, repo["contentdirectory"])

    def do_go_update(self, repo):
        contentdirectory = repo["contentdirectory"]

        subprocess.run(("go get -u github.com/"+repo["user"]+"/"+repo["name"]).split())

        sourcepath = os.path.expandvars("$GOPATH")
        sourcepath = os.path.join(sourcepath, "bin", repo["name"])
        destpath = os.path.join(contentdirectory, repo["name"])

        shutil.copyfile(sourcepath, destpath+".new")
        os.replace(destpath+".new", destpath)