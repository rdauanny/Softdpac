''''''''''''''''''''''''''''''''''''''''''''''''
''' TODO
'''

import os
import sys
import requests
import socket

from urllib3.connection import HTTPConnection
from urllib3.connectionpool import HTTPConnectionPool
from requests.adapters import HTTPAdapter


# Docker adapters

class DockerConnection(HTTPConnection):
    def __init__(self):
        super().__init__("localhost")

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect("/var/run/docker.sock")


class DockerConnectionPool(HTTPConnectionPool):
    def __init__(self):
        super().__init__("localhost")

    def _new_conn(self):
        return DockerConnection()


class DockerAdapter(HTTPAdapter):
    def get_connection(self, url, proxies=None):
        return DockerConnectionPool()

''''''''''''''''''''''''''''''


# class to manage the docker http session
class DockerHttp(object):
    def __init__(self):
        # create http session
        self.session = requests.Session()
        # connect to docker daemon socket
        self.session.mount("http://docker/", DockerAdapter())

    def format_url(self, ep):
        return 'http://docker{}'.format(ep)

    # return json or None if get failed
    def get_ep(self, ep, params=[]):
        url = self.format_url(ep)

        response = self.session.get(url, params=params)
        if response.status_code != 200:
            print('ERROR: cannot get {}: {}'.format(url, response.status))
            return None

        return response.json()

    def delete_ep(self, ep, expected_code, params=[]):
        url = self.format_url(ep)

        response = self.session.delete(url, params=params)
        if response.status_code != expected_code:
            print('ERROR: cannot delete {}: {}'.format(url, response))
            return None

        return response

    def post_ep(self, ep, expected_code, params=[]):
        url = self.format_url(ep)

        response = self.session.post(url, params=params)
        if response.status_code != expected_code:
            print('ERROR: cannot post {}: {}'.format(url, response.status))
            return None

        return response.json()


''''''''''''''''''''''''''''''
# Implement some docker apis

class DockerAPI(object):
    def __init__(self, docker_http):
        self.docker = docker_http

    def list_containers(self, params=[]):
        return self.docker.get_ep('/containers/json', params)

    def list_networks(self, params=[]):
        return self.docker.get_ep('/networks', params)

    def inspect_networks(self, name, params=[]):
        return self.docker.get_ep('/networks/{}'.format(name), params)

    def list_images(self, params=[]):
        return self.docker.get_ep('/images/json', params)

    def list_volumes(self, params=[]):
        return self.docker.get_ep("/volumes", params)

    def inspect_volume(self, name, params=[]):
        return self.docker.get_ep("/volumes/{}".format(name), params)

    def remove_volume(self, name, params=[]):
        return self.docker.delete_ep("/volumes/{}".format(name),
            204, params)

    def remove_container(self, id, params=[]):
        return self.docker.delete_ep('/containers/{}'.format(id),
            204, params)

    def remove_network(self, id, params=[]):
        return self.docker.delete_ep('/networks/{}'.format(id),
            204, params)

    def remove_image(self, id, params=[]):
        return self.docker.delete_ep('/images/{}'.format(id),
            200, params)




