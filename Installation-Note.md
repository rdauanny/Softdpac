[[_TOC_]]

# Soft dPAC Installation Notes

## Pre-requisites

#### **1- Check your system specifications**


|  | Minimum |Recommended  |Required for RT control  |
|--|--|--|--|
|OS  | Debian10.3/Ubuntu18.04 and 20.04/Raspbian 32 or 64 bits  | Debian10.3/Ubuntu18.04 and 20.04/Raspbian 32 or 64 bits | Ubuntu 20.04 with low-latency patch or other distribution with PREEMPT-RT patch |
|Docker   | docker 19.03.8 and above | docker 19.03.8 and above            | docker 19.03.8 and above |
|CPU      | X86/ARM 1 GHz or greater | Multi-core X86/ARM 1 GHz or greater | Dedicated cores          |
|RAM      | 256MB                    | 1GB                                 | 1GB                      |
|HDD/SSD  | 16GB                     | 32GB                                | 32GB                     |
|Network  | At least one NIC         | Two NICs to isolate control and device networks                             | One NIC per Container for RT field-buses    |
|Time synchronization |NTPv4 client|NTPv4 client support with monotonic and drift compensation|NTPv4 client support with monotonic and drift compensation|

 
**Note** : for remote installation, SSH server must be enabled on your system (disabled by default on Ubuntu).

  
**Important Note 1**: In non real-time operating systems, the accuracy of the time management is not high enough to match real-time requirements, therefore only non time-critical processes must be executed (like analytics and orchestration for example).  
Please follow the instructions in chapter "Real-Time System Optimizations" for more information.

:warning: **If you are using a non real-time Linux: Unexpected Application Behavior!** :warning:  
Do not use Soft dPAC on Non-real time linux to process application tasks that require real-time level behavior.  
**Failure to follow these instructions can cause death, serious injury or equipment damage.**

**Important Note 2**: In systems where Archive or Alarming features is used, the controllers need to be synchronized on the same date and time references.  
Please follow the instructions in chapter "Time Synchronization" for more information.

:warning: **If you are not using a synchronized controller: Alarm information will be wrong and could lead to bad decisions!**:warning:  
Do not use Soft dPAC where not time synchronization is available.  
**Failure to follow these instructions can lead to the degradation of main function.**


#### **2- Install docker daemon (requires internet connection)**

- [Verify if your platform is supported](https://docs.docker.com/install/#supported-platforms)

- [Example for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
 
_Note: in the left menu you can choose other linux platform._

- Recommended for supported platforms: Use the Docker **convenience script**:

`$ curl -fsSL get.docker.com -o get-docker.sh`  
`$ sh get-docker.sh`

####_Recommended option: Grant docker permission_

To avoid typing `sudo` for each docker command, you can add yourself to the docker group like explained [here](https://docs.docker.com/install/linux/linux-postinstall/)

`$ sudo usermod -aG docker your-user`


#### **3- Enable Memory Limit for Raspberry Pi 4**
The memory limit is not supported by default by the Raspbian operating system on Raspberry Pi 4.  
You need to add this setting to the /boot/cmdline.txt file to enable the memory limit:

`$cd /boot`  
`$sudo nano cmdline.txt`  

Add the following line at the end of the file:  
`cgroup_enable=memory`  
Save (Ctrl+S).
   
System reboot is needed to make the change take effect.  
`$sudo reboot`

#### **4- Install python3 (requires internet connection)**

Some of our scripts require python3. 

If not already installed, from [python official download page](https://www.python.org/downloads/), you can install it for all supported plateform:
  
    - Windows, Linux/UNIX, Mac OS X, Other

#### **5- Activate Docker IPv6 for Device Discovery**

`$ sudo echo '{ "ipv6": true, "fixed-cidr-v6": "fd00::/80" }' > /etc/docker/daemon.json`

`$ sudo systemctl restart docker`

## **Soft dPAC Installation procedure**

####1- Copy the softdpac package to the target in the folder of your choice (eg: `/home/<user>/workspace`) using **winscp** or with a usb stick.

####2- Untar the softdpac package with the UI or from the terminal (local or with putty in ssh):

1 - go to the folder: `$ cd /home/user/SoftdPAC`

2 - untar the folder: `$ tar -xvf softdpac-develop-258.tar`

3 - add execution rights to script in case you copied it manually: `$ chmod +x startSoftdPAC.sh`

NB : `$ ls -al` to check file permissions in a folder.

####3- Run the `install.py` script contained in the package to get the softDPAC docker image in your local docker registry:

`$ python3 install.py`

_OR_

`$ ./install.py`

_OR_

`$ sudo ./install.py` if you are **not** part of docker group

_Alternative to install.py script **in case your target does not support Python**_

`$ docker load -i <image-name>` (eg: *$ docker load -i softdpac-armhf-develop-258.docker*) 

## Soft dPAC usage after installation

### *Summary of the two possible usages*

**Run Soft dPAC**: Use `startSoftdPAC.sh` script to setup a working docker environment and run the SoftDPAC image as a container in unique or multiple isntances.

**Uninstall Soft dPAC**: Use `uninstall.py` script to uninstall softdpac docker environment in order to clean-up you target for preparation of a use a new release.

### **Run Soft dPAC**

It will basically:

- create a macvlan (or ipvlan) persistent network, see below for choice criterias

- run on this network X instance(s) of docker SoftDPAC of the desired image with IP addresses in the range you have chosen.

#### 1- Run script usage:

 `$ ./startSoftdPAC.sh --image-name <valid image name> [--ipbase <ip addr base>] [--gateway <ip addr>] [--itname <interface name>] [--nbcontainer <nb container>] [--cname <container name>] [--network <type of network>] [--net-name <network name>]  [--publish-on <port number>]`

- Example

`$ ./startSoftdPAC.sh --ipbase 192.168.20.140 --itname ens33 --image-name softdpac:x86-develop-258 --nbcontainer 2`

#### 2- Run script options:


```
--image-name              : set image name to use (mandatory parameter);
-i,  --ipbase             : set ip address base value and subnet mask. Only IPv4 and CIDR notation (default: 192.168.1.10/24);
-g,  --gateway            : set gateway (default: calculated from ipbase);
--itname                  : set interface name (default: eth0);
-n,  --nbcontainer        : set number of container to create (default: 1);
--cname                   : set container base name (default: softdpac_);
--network                 : set network type (default: macvlan); other value: ipvlan or bridge (bridge value used only on Windows);
--net-name                : set network name (default: softdpacNet);
--publish-on              : set port translation only used with bridge network type (default: 51499);
-h                        : print this message.
```

#### 3- Choose between MACvlan and IPvlan ( `--network` option):

Choose **IPvlan** (`--network ipvlan`) if:

- Parent interface is wireless

- The Linux host that is connected to the external switch / router has policy configured that allows only one mac per port.

- No of virtual devices created on a master exceed the mac capacity and puts the NIC in promiscuous mode and degraded performance is a concern.

- If the slave device is to be put into the hostile / untrusted network namespace where L2 on the slave could be changed / misused.

Choose **Bridge** (`--network bridge`) if:

- Docker host is on Windows WSL2 (macvlan and ipvlan don't work with Windows WSL2).

- Remark 1: is not recommended to use it on Linux.

- Remark 2: in this mode, publish port translation was used to communicate with Soft dPAC.

**Otherwise, choose MACvlan** which is the default network type (nothing or `--network macvlan`)  
Important notice: **when using macvlan network**, you will probably need to **set the gateway** accordingly otherwise your Soft dPAC containers will not be pingable from your workstation and you will not be able to login with EAE.

### **Uninstall Soft dPAC**

The `uninstall.py` script will automatically uninstall softdpac docker environment.

When running this command, a summary will:

- display all elements to be removed

- ask you to confirm 

- do the uninstall

#### 1- Uninstall script usage

`$ python3 uninstall.py`

_OR_

`$ ./uninstall.py`

_OR_

`$ sudo ./uninstall.py` if you are **not** part of docker group


#### 2- Uninstall script Options

`--force: remove user confirmation`

#### 3- Uninstall script alternatives (in case your target does not support python)

Use **portainer** web user interface to remove sofdpac containers + network + previous image + volumes in case you want a full fresh start.

_OR_

**If you don't have portainer,** use the docker command line interface to remove all softdpac items/artefacts manually :

1- List the running containers and identify the softdpac containers (name or ID): `$ docker ps`

2- Delete all the softdpac conainers : `$ docker rm -f <container name or ID>`

3- List the docker networks and identify the softdpac network (name or ID): `$ docker network ls` 

4- Delete the softdpac network : `$ docker network rm -f <network name>`

5- List the docker images and identify the softdpac images (name or ID): `$ docker images` 

6- Delete the softdpac images : `$ docker rmi -f <image name or ID>`  

7- List the docker volumes and identify the softdpac volumes (name or ID): `$ docker volumes` 

8- Delete the softdpac volumes : `$ docker volumes rm -f <volume name or ID>`

_AND_ 

Delete former softdpac files/package in the folder where you downloaded the softdpac package (eg in `/home/<user>/workspace`) :

`$ rm <filename> (for files)`

`$ rm -rf <foldername> (for folder)`

**Be aware that there is no trash folder to recover the removed files.**

NB: This part of the procedure is also applicable when the uninstall script is supported. 



## Soft dPAC Versioning

Pattern is: softdpac-[architecture]-[SoftDPAC branch]-[Build version]

*Example:* softdpac-x86-v20.2-158.docker

- Image_name is:            *softdpac*

- Architecture is:          *x86*

- SoftDPAC branch is:      *v20.2*

- Build version:            *158*


## Real-Time System Optimisation (Required for real-time control)

### Realtime kernel

#### 1- Before installing the patched version, you can start a test to check your Linux kernel version and mesure the latency of the standard Linux kernel (system without stress) :

```
sudo apt update
sudo apt install rt-tests
uname -a
sudocyclictest --mlockall --smp --priority=80 --interval=200 --distance=0
```
![image.png](/.attachments/image-616eecae-24b9-4522-a6f2-381d45be6d5b.png)

You can check that cyclic test max time is unpredictable and may fluctuate in a unacceptable way. 

For more information about cyclictestsoftware, see its documentation : https://wiki.linuxfoundation.org/realtime/documentation/howto/tools/cyclictest/start?s%5B%5D=cyclictest
 
#### 2- With Ubuntu distribution, the real time patched kernel could easily be installed using the following command (to use this kernel, it is necessary to reboot the PC) :

```
sudo apt update
sudo apt install linux-lowlatency
sudo reboot
```

#### 3- After rebooting, you can check your Linux kernel patched version and mesure its latency

```
uname -a
sudocyclictest --mlockall --smp --priority=80 --interval=200 --distance=0
```

![image.png](/.attachments/image-ad7e75b4-a399-45cb-86b5-f4f7b21c51ff.png)

In that case, cyclic test max time is much more predictable and ranged. 

### System cleanup

The Ubuntu distribution is provided with a special daemon, kerneloops, which is able to capture kernel crashed. This daemon sometimes introduces curious delay in any real-time executions. This tool has to be removed to keep real-time performance

```
sudo apt-get remove --purge kerneloops-applet kerneloops-daemon
sudo reboot
```

## Time Synchronization (Required to use Archive and Alarming features)

Prerequisite 1 : A NTP server must be configured and available on your network or your Host server must be connected to the Internet.

Prerequisite 2 : Your Host server must have NTP Client running.

####Example of configuration with Debian based distributions (Debian 10.x, Ubuntu 18.04 and later, Raspbian Buster)

#### _Configure NTP Client for Ubuntu_
 	
A NTP Client [systemd-timesyncd.service] is running by default on Ubuntu, so it's easy to set NTP Client.  

Check current status:
```
$ systemctl status systemd-timesyncd
*  systemd-timesyncd.service - Network Time Synchronization
     Loaded: loaded (/lib/systemd/system/systemd-timesyncd.service; enabled; ve>
     Active: active (running) since Mon 2020-04-27 01:20:36 UTC; 2min 6s ago
       Docs: man:systemd-timesyncd.service(8)
   Main PID: 662 (systemd-timesyn)
     Status: "Initial synchronization to time server 91.189.94.4:123 (ntp.ubunt>
      Tasks: 2 (limit: 4621)
     Memory: 1.5M
     CGroup: /system.slice/systemd-timesyncd.service
             +- 662 /lib/systemd/systemd-timesyncd
```

Add the NTP server IP setting to the end of the timesyncd.conf
root@client:~# nano /etc/systemd/timesyncd.conf

Example: `NTP=dlp.srv.world`

Check new status:
```
$ systemctl status systemd-timesyncd
*  systemd-timesyncd.service - Network Time Synchronization
     Loaded: loaded (/lib/systemd/system/systemd-timesyncd.service; enabled; ve>
     Active: active (running) since Mon 2020-04-27 01:29:22 UTC; 6s ago
       Docs: man:systemd-timesyncd.service(8)
   Main PID: 1108 (systemd-timesyn)
     Status: "Initial synchronization to time server 10.0.0.30:123 (dlp.srv.world>
      Tasks: 2 (limit: 4621)
     Memory: 1.3M
     CGroup: /system.slice/systemd-timesyncd.service
             +- 1108 /lib/systemd/systemd-timesyncd
```

#### _Configure NTP Client for Raspbian_
 	
A NTP Client [systemd-timedatectl.service] is running by default on Raspbian, so it's easy to set NTP Client.  

1- Check current status:
```
$ timedatectl status`
               Local time: Tue 2020-10-13 18:59:40 CEST
           Universal time: Tue 2020-10-13 16:59:40 UTC
                 RTC time: n/a
                Time zone: Europe/Paris (CEST, +0200)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```
NTP service should be active otherwise:  

```
$ sudo timedatectl set-ntp true
```


2- Change the synchronization server.  
You can do this in the configuration file. Open the file timesyncd.conf:   
`$ sudo nano /etc/systemd/timesyncd.conf`  
Comment out the last line and replace default servers by the servers you want to use (on Internet or from the local network)  
For example:  
`[Time] #NTP= FallbackNTP=0.us.pool.ntp.org 1.us.pool.ntp.org`


3- Set time zone
To set the current time zone, use this command:

`$ sudo timedatectl set-timezone <time zone>`

# Troubleshooting 

## Revolution Pi: start script has Docker errors

Please use the default "pi" user or be sure your user is part of groups below:

_pi adm dialout cdrom sudo audio video plugdev games users input docker gpio i2c spi_


## Revolution Pi: ./uninstall script errors

./uninstall script may crash when being executed from Revolution PI, with the following error :

```
==== Inspecting Docker resources ====
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/util/timeout.py", line 127, in _validate_timeout
    float(value)
TypeError: float() argument must be a string or a number, not 'Timeout'
....
  File "/usr/lib/python3/dist-packages/urllib3/util/timeout.py", line 130, in _validate_timeout
    "int, float or None." % (name, value))
ValueError: Timeout value connect was Timeout(connect=None, read=None, total=None), but it must be an int, float or None.
```

To avoid it, The "requests" python package has to be upgraded. Execute the following code to solve the issue : 

` pip3 install --upgrade requests `