# github-checkout-manager
A HTTP server that will listen for a webhooks push from github, and automatically grab the latest changes and deploy them to a directory.
Useful for websites, so that you can update the live site by pushing to a branch of your choosing

#Setup

Grab the source and stick it in a directory of your choosing on your webserver. Permissions will be easiest to manage and most secure if you create a new user for github-checkout-manager.

Config file
Put as many repos as you would like in the json config file. Each repo needs the following information:
user - The github username the repo belongs to i.e. (cmhull42)
name - The official name of the repository i.e. (github-checkout-manager)
branch - The branch you would like to track updates to - currently only supports master
configdirectory - this directory should contain a cloned copy of the repo (with the same name) and optionally a private key id_rsa to authenticate to github with.
contentdirectory - the directory to deploy the code to i.e. (/var/www/connoor.io)
