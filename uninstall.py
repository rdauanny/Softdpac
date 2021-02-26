#!/usr/bin/env python3

''''''''''''''''''''''''''''''''''''''''''''''''
''' Script to uninstall docker softdpac resources (networks, containers, images, volumes) if any
'''

import os
import sys
import argparse

from helpers import run_cmd
from apis import docker
from common import constants

''''''''''''''''''''''''''''''
def fix_names(objects_json):
    if 'Names' in objects_json:
        name = objects_json['Names'][0][1:]
        objects_json['Names'][0] = name
    return objects_json

def filter_by_label(objects_json):
    objects = []
    for object in objects_json:
        if object['Labels'] is not None and constants.IMAGE_LABEL in object['Labels']:
            objects.append(fix_names(object))

    return objects

def ask_user(msg):
    prompt = '{} - Press ENTER to continue, (N/n) to skip or (E) to exit now : '.format(msg)
    response = input(prompt)

    if response == 'E':
        print('Exiting...')
        sys.exit(1)

    return response != 'n' and response != 'N'

''''''''''''''''''''''''''''''


class Uninstall(object):



    def __init__(self, dockerAPI):
        self.dockerAPI = dockerAPI

    def acquire_containers(self):
        params = {'all': 'true'}
        conts = self.dockerAPI.list_containers(params)
        if conts is None:
            print('ERROR: cannot get container list')
            return None

        active_containers = []
        dead_containers = []

        #print(json.dumps(conts, indent=2))
        for container in conts:
            #print(json.dumps(container, indent=2))
            if container['Labels'] is not None and constants.IMAGE_LABEL in container['Labels']:
                if container['State'] == 'exited':
                    dead_containers.append(container)
                    print('Found {} {} container with name {}'.format(container['State'], container['Image'], container['Names']))
                else:
                    active_containers.append(container)

        return active_containers, dead_containers

    def acquire_images(self):
        params = {'all': 'false'}
        images = self.dockerAPI.list_images(params)
        if images is None:
            print('ERROR: cannot get image list')
            return None

        images = filter_by_label(images)

        for image in images:
            if 'RepoTags' in image:
                print('Found image {}'.format(image['RepoTags']))

        return images

    def acquire_networks(self, containers):
        networks = self.dockerAPI.list_networks()
        if networks is None:
            print('ERROR: cannot get network list')
            return None

        used_networks = []

        for network in networks:
            net = self.dockerAPI.inspect_networks(network['Name'])
            if net is None:
                print('ERROR: cannot inspect network {}'.format(network['Name']))
                return None

            ids = []
            for cont_id in net['Containers']:
                # check with our containers to know it is in use
                for known_container in containers:
                    if known_container['Id'] == cont_id:
                        if net['Name'] not in ['bridge']:
                            ids.append(cont_id)

                            print('Found running [{}] container with name [{}] on network [{}]'.format(
                                known_container['Image'],
                                known_container['Names'][0],
                                network['Name']))

            if len(ids) > 0:
                remaining = list(set(net['Containers']) - set(ids) )
                # if remaining is empty, no other container use this network
                if len(remaining) == 0:
                    used_networks.append(net)
            # if no container attached to the net, check labels
            else:
                if self.acquire_labelled_network(net):
                    print('Found unused network [{}] labelled [{}]'.format(net['Name'], constants.NETWORK_LABEL ))
                    used_networks.append(net)

        return used_networks

    def acquire_labelled_network(self, network):
        return constants.NETWORK_LABEL in network['Labels']


    def acquire_volumes(self):
        # get volume containing the label
        response = self.dockerAPI.list_volumes()
        if response is None:
            print('ERROR: cannot get volumes')
            return None

        volumes = []
        for volume in response['Volumes']:
            if volume['Labels'] is not None and constants.NETWORK_LABEL in volume['Labels']:
                volumes.append(volume)
                print('Found volume {}, used by container {}'.format(volume['Name'], volume['Labels']['reference']))

        return volumes

    def remove_containers(self, results):
        for dc in results['dead_containers']:
            print('Removing container {}'.format(dc['Names'][0]))
            self.dockerAPI.remove_container(dc['Id'])

        for c in results['containers']:
            print('Removing running container {}'.format(c['Names'][0]))
            # force will do a kill before remove
            params = {'force': 'true', 'v': 'false'}
            self.dockerAPI.remove_container(c['Id'], params)

    def remove_volumes(self, results):
        for v in results['volumes']:
            self.dockerAPI.remove_volume(v['Name'])

    def remove_networks(self, results):
        for n in results['networks']:
            print('Removing network {}'.format(n['Name']))
            self.dockerAPI.remove_network(n['Id'])

    def remove_images(self, results):
        for i in results['images']:
            print('Removing image {}'.format(i['Id']))

            # Remove the image even if it is being used by stopped containers or has other tags
            params = {'force' : 'true'}
            self.dockerAPI.remove_image(i['Id'], params)

    def summary(self, results):
        print('\n==== SUMMARY ====')

        for dc in results['dead_containers']:
            print('Will remove exited container [{}]'.format(dc['Names'][0]))

        for c in results['containers']:
            print('Will kill then remove [{}] container [{}]'.format(c['State'], c['Names'][0]))

        for v in results['volumes']:
            print('Will delete volume [{}]'.format(v['Name']))

        for n in results['networks']:
            print('Will delete network [{}]'.format(n['Name']))

        for i in results['images']:
            print('Will remove image [{}]'.format(i['RepoTags']))

    def acquire_all(self):
        print('==== Inspecting Docker resources ====')

        c, dc = self.acquire_containers()
        if c is None:
            return False

        n = self.acquire_networks(c)

        v = self.acquire_volumes()

        i = self.acquire_images()

        results = {'containers': c,
                'dead_containers': dc,
                'networks': n,
                'volumes': v,
                'images': i}

        return results, len(c)>0 or len(dc)>0 or len(n)>0 or len(v)>0 or len(i)>0

    def remove_all(self, results):
        print('\n==== Cleaning ====')

        self.remove_containers(results)

        self.remove_volumes(results)

        self.remove_networks(results)

        self.remove_images(results)

    def process(self, force):
        results, has_resources = self.acquire_all()
        if not has_resources:
            print('Nothing to do')
            return

        self.summary(results)

        if force:
            print('==> force mode')
            self.remove_all(results)
        elif ask_user('Continue with deletion ?'):
            self.remove_all(results)

        print('Done')

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action='store_true', help="if used, no user confirmation before uninstalling everything")
    args = parser.parse_args()
    return args


''''''''''''''''''''''''''''''

def main():
    args = get_args()

    httpPool = docker.DockerHttp()
    dockerAPI = docker.DockerAPI(httpPool)

    uninstall = Uninstall(dockerAPI)

    uninstall.process(args.force)




if __name__ == '__main__':
    main()
