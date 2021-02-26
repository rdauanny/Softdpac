#!/usr/bin/env python3

import re
import os
import sys
import fnmatch
import subprocess
import ast
import argparse
import json

from helpers import run_cmd
from common import constants


''''''''''''''''''''''''''''''''''''''''''''''''
''' Script to install docker softdpac images
'''

""""""""""""""""""""""""""""""

class HostConfig(object):

    ipv6_docker ={ "ipv6": True, "fixed-cidr-v6": "fd00::/80" }
    ipv6_docker_file = '/etc/docker/daemon.json'

    def __init__(self, args):
        self.args = args

    def is_root_user(self):
        return os.geteuid() == 0

    def configure_host(self):
        if not self.args.no_interactive:
            response = input('Do you want to configure your host ? Press ENTER to continue or (n/N) to skip totally this part: ')
            if response == 'n' or response == 'N':
                return
            self.args.no_host_config = False

        if not self.args.no_host_config:
            if not self.is_root_user():
                print('ERROR: You need root rights, please run this script again with sudo or root user....')
                sys.exit(3)

            self.enable_ipv6_docker()

    def enable_ipv6_docker(self):
        print('INFO: Enabling docker ipv6')

        try:
            config = dict()
            # check if file exist => merge with existing config
            if os.path.exists(self.ipv6_docker_file):
                with open(self.ipv6_docker_file) as f:
                    config = json.load(f)

                config['ipv6'] = self.ipv6_docker['ipv6']

                if 'fixed-cidr-v6' in config and len(config['fixed-cidr-v6']) > 0 and not self.args.no_interactive:
                    response = input('Do you want to keep your current "fixed-cidr-v6" value ({}) or update to ({}) ? Press ENTER to update or (n/N) to keep current setting: '.format(
                        config['fixed-cidr-v6'], self.ipv6_docker['fixed-cidr-v6']))
                    if response != 'n' and response != 'N':
                        config['fixed-cidr-v6'] = self.ipv6_docker['fixed-cidr-v6']
            else:
                # file not exist
                config = self.ipv6_docker

            # save
            with open(self.ipv6_docker_file, 'w') as json_file:
              json.dump(config, json_file)

            # restart docker daemon
            out, ret = run_cmd.run_cmd('systemctl reload docker')
            if ret != 0:
                print('ERROR: failed to reload docker daemon: {}'.format(out))
            else:
                print('INFO: docker ipv6 enabled OK')

        except Exception as inst:
            print('ERROR: {}'.format(inst))
            print('ERROR: docker ipv6 NOT enabled...')


class Install(object):

    ## constructor
    def __init__(self):
        # expected pattern: see wiki at:
        # https://waat00424.gmea.gad.schneider-electric.com/nxtControl/UAP_SOFTDPAC/_wiki/wikis/UAP_SOFTDPAC.wiki?wikiVersion=GBwikiMaster&pagePath=%2FWelcome%2FNaming%20Convention%20and%20Versioning&pageId=377
        # basically: <softdpac>-<arch>-<dockersotdpac branch>[-dockersotdpac build number]
        self.reg_version = re.compile("^({})-([a-z0-9]+)-([a-zA-Z0-9._]+)(-[0-9-]+)?\.{}$".format(
            constants.ECORT_NAME, constants.COMPRESSED_IMAGE_EXTENSION))

        self.dir_path = os.path.dirname(os.path.realpath(__file__))

        # contain supported archs: x86, armh
        self.supported_archs, self.archs_dict = Install.get_supported_archs()
        # will contains .docker images found in the package
        self.images = []
        # will contains candidate image to install depending on the host 'arch' command
        self.image_to_install = {}

    @staticmethod
    def get_supported_archs():
        # tricks to parse python dict from string, needed so constants.py can be sourced by shells
        SUPPORTED_ARCHS = ast.literal_eval(constants.SUPPORTED_ARCHS)

        supported_archs = []
        for supported_arch in SUPPORTED_ARCHS:
            supported_archs.append(supported_arch)

        return supported_archs, SUPPORTED_ARCHS

    ## find all COMPRESSED_IMAGE_EXTENSION in the current folder
    def find_tar(self):
        print('INFO: working directory: {}'.format(self.dir_path))
        files = os.listdir(self.dir_path)
        pattern = '*.{}'.format(constants.COMPRESSED_IMAGE_EXTENSION)

        for entry in files:
            if fnmatch.fnmatch(entry, pattern):
                    print('INFO: compressed docker image [{}] found OK'.format(entry))
                    self.get_docker_tag_from_tar(entry)

        if len(self.images) == 0:
            print('ERROR: compressed docker image not found, exiting...')
            sys.exit(1)


    ## from file matching COMPRESSED_IMAGE_EXTENSION, run the regexp
    def get_docker_tag_from_tar(self, filename):
        res = self.reg_version.match(filename)
        if res is None:
            return

        # non relase mode, need to remove the - prefix fot build
        if len(res.groups()) == 4 and res.group(4) is not None:
            for arch in self.supported_archs:
                if arch in res.group(2):
                    image = {'filename' :res.group(0),
                            'name': res.group(1),
                            'arch': res.group(2),
                            'branch': res.group(3),
                            'build_version': res.group(4)[1:],
                            'release_mode': False }

                    self.images.append(image)

                    print('INFO: image name: [{}] branch: [{}] build version: [{}] arch: [{}]'.format(image['name'],
                        image['branch'], image['build_version'], image['arch']))
        # release mode
        elif len(res.groups()) == 4:
            for arch in self.supported_archs:
                if arch in res.group(2):
                    image = {'filename' :res.group(0),
                            'name': res.group(1),
                            'arch': res.group(2),
                            'branch': res.group(3),
                            'release_mode': True }

                    self.images.append(image)

                    print('INFO: image name: [{}] branch: [{}] arch: [{}]'.format(image['name'],
                        image['branch'], image['arch']))

    def get_current_host_arch(self):
        out, ret = run_cmd.run_cmd('arch')
        out = str(out, 'utf-8')
        if ret == 0:
            print('INFO: Your current architecture is: {}'.format(out))
            return out

        print('ERROR: command arch failed with code {}, aborting... : {}'.format(ret, out) )
        sys.exit(5)

    def check_docker_registry(self):
        out, ret = run_cmd.run_cmd('docker images {} -q'.format(Install.get_image_with_tag(self.image_to_install)))
        if ret == 0:
            out = out.strip()
            if len(out) > 0:
                print('INFO: Found existing docker image {} in your local registry with IDs: {}'.format(
                    Install.get_image_with_tag(self.image_to_install),
                    out))
            return len(out) == 0
        else:
            print('ERROR: Please install docker first or set permissions, look at install.md for more details.')
            sys.exit(4)

    def set_image_from_arch(self):
        host_arch = self.get_current_host_arch()

        for supported_arch, host_arch_keywords in self.archs_dict.items():
            for keyword in host_arch_keywords:
                if keyword in host_arch:
                    # found keyword, search corresponding image
                    for image in self.images:
                        if supported_arch == image['arch']:

                            self.image_to_install = image
                            print('INFO: Image [{}] is candidate'.format(Install.get_image_with_tag(image)))
                            return True


        print('ERROR: There is no images corresponding to your architecture ({}), supported architecture are {}'.format(
            host_arch,
            self.supported_archs))
        sys.exit(3)

    def load_docker(self):
        out, ret = run_cmd.run_cmd('docker load --input {}'.format(self.image_to_install['filename']))
        if ret == 0:
            print('INFO: image has been loaded, docker response is: {}'.format(out))
            return True
        else:
            print('ERROR: cannot load docker image: {}'.format(out))
            sys.exit(2)

    @staticmethod
    def get_tag_from_image(image_dict):
        if image_dict['release_mode'] is True:
            tag = '{}-{}'.format(image_dict['arch'],
                image_dict['branch'])
        else:
            tag = '{}-{}-{}'.format(image_dict['arch'],
                image_dict['branch'],
                image_dict['build_version'])
        return tag

    @staticmethod
    def get_image_with_tag(image_dict):
        return '{}:{}'.format(constants.ECORT_NAME, Install.get_tag_from_image(image_dict))

################################
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_host_config", help="Disable host configuration" , default=False, action="store_true")
    parser.add_argument("--no_interactive", help="disable interactive mode" , default=False, action="store_true")

    args = parser.parse_args()
    return args
##################################

def main():
    args = get_args()

    h = HostConfig(args)
    h.configure_host()

    i = Install()
    i.find_tar()
    if i.set_image_from_arch():
        if i.check_docker_registry():
            i.load_docker()
        else:
            print('INFO: docker image [{}] already exist in your docker registry, nothing to do...'.format(
                Install.get_image_with_tag(i.image_to_install) ))


if __name__ == '__main__':
    main()
