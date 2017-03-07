import json
import time
import datetime
import os
import sys
import getpass
from os.path import expanduser
from subprocess import Popen, PIPE, STDOUT
import subprocess as sb
import stat
import tempfile
import pwd

import bit.config as config
import big.git as git
import bit.owncloud as oc
import bit.rsync as rsync


def check_reqs(requirements,configdic,config_file=None, gitssh=None):
    if "owncloud_address" in requirements:
        configdic["owncloud_address"]=config.get_owncloud_address()
    if "owncloud_upload_folder" in requirements:
        configdic["owncloud_upload_folder"]=config.get_owncloud_upload_folder()
    if "owncloud_download_folder" in requirements:
        configdic["owncloud_download_folder"]=config.get_owncloud_download_folder()
    if "owncloud_user" in requirements:
        configdic["owncloud_user"]=config.get_owncloud_user(config_file=config_file)
    if "owncloud_pass" in requirements:
        configdic["owncloud_pass"]=config.get_owncloud_pass(config_file=config_file)
    if "github_address" in requirements:
        configdic["github_address"]=config.get_github_address()
    if "github_organization" in requirements:
        configdic["github_organization"]=config.get_github_organization()
    if "github_user" in requirements:
        configdic["github_user"]=config.get_github_user(config_file=config_file,gitssh=gitssh )
    if "github_pass" in requirements:
        configdic["github_pass"]=config.get_github_pass(config_file=config_file,gitssh=gitssh )
    if "local_path" in requirements:
        configdic["local_path"]=get_local_path()
    if "user_group" in requirements:
        configdic["user_group"]=config.get_user_group()
    return configdic

requirements=["owncloud_address","owncloud_upload_folder",\
"owncloud_download_folder","owncloud_user",\
"owncloud_pass","github_address",\
"github_organization","github_user",\
"github_pass","local_path", "user_group" ]

special_reqs=["owncloud_user","owncloud_pass",\
"github_user","github_pass"]

start_reqs=["github_address","github_organization",\
"github_user","github_pass","local_path"]

def init_user(path_to_project,github_address,github_organization,github_repo,github_user=None,github_pass=None,gitssh=None):
    user_name=getpass.getuser()
    response=git.git_clone(path_to_project+"/scripts."+user_name , github_address, github_organization, github_repo, github_user=github_user, github_pass=github_pass, gitssh=gitssh)
    response=git.git_clone(path_to_project+"/wiki."+user_name , github_address, github_organization, github_repo+".wiki", github_user=github_user, github_pass=github_pass, gitssh=gitssh)
    while response == 1:
        raw_input("\n\n*************\n\nThe wiki for this project has not yet been created.\n\n Please go to %s/%s/%s/wiki and click on 'Create the first page' and then 'Save Page'.\n\nPress Enter once you have saved the first wiki page.\n\n*************\n\n" %(github_address,github_organization,github_repo) )
        response=git.git_clone(path_to_project+"/wiki."+user_name ,github_address,github_organization,github_repo+".wiki",github_user=github_user,github_pass=github_pass,gitssh=gitssh)
