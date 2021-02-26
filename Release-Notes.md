[[_TOC_]]

# Soft dPAC Docker Linux v20.2 - release - 20315
_Delivered on 10/11/2020 - for EAE 20.2 (ring 0, 1 & 2)_ 

Changes compared to previous version:

**Added features:**
* None

**Bugs fixed:**

* Including bug fix from core runtime release/v20.2 branch from 9/11/2020 concerning HMI client disconnection issue.

**Bugs identified/remaining:**

* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL
* Memory consumption reflects the host memory and not the docker memory
* Some information are missing in discovery view (device description and full version)  

**Not yet tested:**
* None

**Tested on:**

* ubuntu 20.04.4 amd64 with low-latency patch (docker 19.03.8)
* ubuntu 18.04.4 amd64 (docker 19.03.8)
* Raspbian buster (Rpi 4) (docker 19.03.09) 
* Debian 10.3.0 amd 64 (docker 19.03.8)
* Window 10 2004 with WSL2 support (docker desktop)
* Revolution Pi Connect (docker 19.03.13).
* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported. It will be solved when HMIBSC image will be updated to Yocto 3.0 and Docker 19.03.xx

**Not officially supported:**
* Window 10 2004 with WSL2 support (docker desktop)
---

# Soft dPAC Docker Linux v20.2 - release - 20308
_Delivered on 03/11/2020 - for EAE 20.2 (ring 0, 1 & 2)_ 

Changes compared to previous version:

**Added features:**
* None

**Bugs fixed:**

* Including bug fixes from core runtime release/v20.2 branch from 2/11/2020 (4086a3ef)
* Documentation provided to have macvlan working as expected on Raspberry Pi4 on every network configurations

**Bugs identified/remaining:**

* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL
* Memory consumption reflects the host memory and not the docker memory
* Some information are missing in discovery view (device description and full version)  

**Not yet tested:**
* None

**Tested on:**

* ubuntu 20.04.4 amd64 with low-latency patch (docker 19.03.8)
* ubuntu 18.04.4 amd64 (docker 19.03.8)
* Raspbian buster (Rpi 4) (docker 19.03.09) 
* Debian 10.3.0 amd 64 (docker 19.03.8)
* Window 10 2004 with WSL2 support (docker desktop)
* Revolution Pi Connect (docker 19.03.13).
* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported. It will be solved when HMIBSC image will be updated to Yocto 3.0 and Docker 19.03.xx

**Not officially supported:**
* Window 10 2004 with WSL2 support (docker desktop)
---

# Soft dPAC Docker Linux v20.2 - release - 20288
_Delivered on 14/10/2020 - for EAE 20.2 (ring 0, 1 & 2)_ 

Changes compared to previous version:

**Added features:**
* Heart-Beat to check that Runtime is still alive in Soft dPAC container
* Setting Gateway for Soft dPAC Network from softDpac start script

**Bugs fixed:**

* Documentation updated to include troubleshooting to solve bugs found on Revolution Pi (ipvlan support and uninstall script)
* Documentation updated to configure ntp client on supported targets.

**Bugs identified/remaining:**

* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL
* Memory consumption reflects the host memory and not the docker memory
* macvlan not working as expected on Raspberry Pi4 with some network configurations (one workaround is to ping first from inside the container)

**Not yet tested:**
* FB_DLL runtime feature
* BM_DLL runtime feature

**Tested on:**

* ubuntu 20.04.4 amd64 with low-latency patch (docker 19.03.8)
* ubuntu 18.04.4 amd64 (docker 19.03.8)
* Raspbian buster (Rpi 4) (docker 19.03.09) Known limitation for some users: only ipvlan is working as expected. To use macvlan, it is needed to ping from inside the container before the container becomes visible on the network by EAE.
* Debian 10.3.0 amd 64 (docker 19.03.8)
* Window 10 2004 with WSL2 support (docker desktop)
* Revolution Pi Connect (docker 19.03.13).
* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported. It will be solved when HMIBSC image will be updated to Yocto 3.0 and Docker 19.03.xx

**Not officially supported:**
* Window 10 2004 with WSL2 support (docker desktop)

---
# Soft dPAC Docker Linux v20.2 - release - 20280
_Delivered on 06/10/2020 - for EAE 20.2 (ring 0, 1 & 2)_ 

Changes compared to previous version:

**Added features:**
* Updating OPCUA stack to enable the UASERVER_SUPPORT_DEADBAND_PERCENT option.

**Bugs fixed:**

* Documentation updated to fix container memory size limit discarded on Raspberry Pi 4

**Bugs identified/remaining:**

* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL
* Memory consumption reflects the host memory and not the docker memory
* macvlan not working as expected on Raspberry Pi4 with some network configurations (one workaround is to ping first from inside the container)

**Not yet tested:**
* FB_DLL runtime feature
* BM_DLL runtime feature

**Tested on:**

* ubuntu 20.04.4 amd64 with low-latency patch (docker 19.03.8)
* ubuntu 18.04.4 amd64 (docker 19.03.8)
* Raspbian buster (Rpi 4) (docker 19.03.8) Known limitation for some users: only ipvlan is working as expected
* Debian 10.3.0 amd 64 (docker 19.03.8)
* Window 10 2004 with WSL2 support (docker desktop)
* Revolution Pi Connect (docker 19.03.8). Known limitation: only macvlan is supported
* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported

**Not officially supported:**
* Window 10 2004 with WSL2 support (docker desktop)
---

# Soft dPAC Docker Linux v20.2 - release - 20262
_Delivered on 18/09/2020 - for EAE 20.2 (ring 0, 1 & 2)_ 

Changes compared to previous version:

**Added features:**
* SFMEA features integration in non-regression automatic tests

**Bugs fixed:**

* Persistent data rotation settings now available for Soft_dPAC device type in SE.DPAC

**Bugs identified/remaining:**

* Container memory size limit is discarded on Raspberry Pi 4
* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL
* Memory consumption reflects the host memory and not the docker memory
* macvlan not working as expected on Raspberry Pi4 with some network configurations (one workaround is to ping first from inside the container)

**Not yet tested:**
* FB_DLL
* Archive runtime feature
* BM_DLL runtime feature

**Tested on:**

* ubuntu 20.04.4 amd64 with low-latency patch (docker 19.03.8)
* ubuntu 18.04.4 amd64 (docker 19.03.8)
* Raspbian buster (Rpi 4) (docker 19.03.8) Known limitation for some users: only ipvlan is working as expected
* Debian 10.3.0 amd 64 (docker 19.03.8)
* Window 10 2004 with WSL2 support (docker desktop)
* Revolution Pi Connect (docker 19.03.8). Known limitation: only macvlan is supported
* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported

**Not officially supported:**
* Window 10 2004 with WSL2 support (docker desktop)
---

# Soft dPAC Docker Linux v20.2 - develop - 20255-779
_Delivered on 11/09/2020 - for EAE 20.2 (ring 0, 1)_ 

Changes compared to previous version:

**Added features:**
* Archive runtime feature is enabled
* BM_DLL runtime feature is enabled

**Bugs fixed:**

* None

**Bugs identified/remaining:**

* Container memory size limit is discarded on Raspberry Pi 4
* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL
* Memory consumption reflects the host memory and not the docker memory
* macvlan not working as expected on Raspberry Pi4 with some network configurations (one workaround is to ping first from inside the container)

**Not yet tested:**
* FB_DLL
* Archive runtime feature
* BM_DLL runtime feature

**Tested on:**

* ubuntu 20.04.4 amd64 with low-latency patch (docker 19.03.8)
* ubuntu 18.04.4 amd64 (docker 19.03.8)
* Raspbian buster (Rpi 4) (docker 19.03.8) Known limitation for some users: only ipvlan is working as expected
* Debian 10.3.0 amd 64 (docker 19.03.8)
* Window 10 2004 with WSL2 support (docker desktop)
* Revolution Pi Connect (docker 19.03.8). Known limitation: only macvlan is supported
* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported

**Not officially supported:**
* Window 10 2004 with WSL2 support (docker desktop)
---

# Soft dPAC Docker Linux v20.2 - develop - 20252-770
_Delivered on 08/09/2020 - for EAE 20.2 (ring 0, 1 & 2)_ 

Changes compared to previous version:

**Added features:**
* SFMEA features in Soft dPAC device type (SE.DPAC library)
* [Enabler] Alpine version updated to 3.12
* Align versioning on EAE to have <year><day of the year> in the package name

**Bugs fixed:**

* None

**Bugs identified/remaining:**

* Container memory size limit is discarded on Raspberry Pi 4
* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL
* Memory consumption reflects the host memory and not the docker memory
* macvlan not working as expected on Raspberry Pi4 with some network configurations (one workaround is to ping first from inside the container)

**Not yet tested:**
* FB_DLL

**Tested on:**

* ubuntu 20.04.4 amd64 with low-latency patch (docker 19.03.8)
* ubuntu 18.04.4 amd64 (docker 19.03.8)
* Raspbian buster (Rpi 4) (docker 19.03.8) Known limitation for some users: only ipvlan is working as expected
* Debian 10.3.0 amd 64 (docker 19.03.8)
* Window 10 2004 with WSL2 support (docker desktop)
* Revolution Pi Connect (docker 19.03.8). Known limitation: only macvlan is supported
* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported

---

# Soft dPAC Docker Linux v20.2 - develop - 746
_Delivered on 25/08/2020 - for EAE 20.2 (ring 0, 1 &2)_ 

Changes compared to previous version:

**Added features:**
* Discovery for first time deployment (DPWS)
* Test of Real-time capabilities/behavior on Linux with RT patch (Basic KPI measurements on Revolution Pi and ubuntu 20.04.4 amd64 with low-latency patch)  

**Bugs fixed:**

* None

**Bugs identified/remaining:**

* Container memory size limit is discarded on Raspberry Pi 4
* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL
* Memory consumption reflects the host memory and not the docker memory
* macvlan not working as expected on Raspberry Pi4 with some network configurations (one workaround is to ping first from inside the container)

**Not yet tested:**
* FB_DLL

**Tested on:**

* ubuntu 20.04.4 amd64 with low-latency patch (docker 19.03.8)
* ubuntu 18.04.4 amd64 (docker 19.03.8)
* Raspbian buster (Rpi 4) (docker 19.03.8) Known limitation for some users: only ipvlan is working as expected
* Debian 10.3.0 amd 64 (docker 19.03.8)
* Window 10 2004 with WSL2 support (docker desktop)
* Revolution Pi Connect (docker 19.03.8). Known limitation: only macvlan is supported
* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported

**Not officially supported:**
* Window 10 2004 with WSL2 support (docker desktop)
---

# Soft dPAC Docker Linux v20.2 - develop - 727
_Delivered on 13/08/2020 - for EAE 20.2 (ring 0 & 1)_ 

Changes compared to previous version:

**Added features:**
* Adding container memory size limit
* Adding support for bridge network for running Softdpac docker linux on WSL2
* Adding support for Cyber-Security Service Function blocks based on OpenSSL (NETIO and RNBR)
* Test of Modbus TCP scanner performance : up to 64 devices at 10ms on Intel core i5 (x86)
* Test of Persistence data and offline parametrization


**Bugs fixed:**

* Thread priorities are now managed properly for real-time applications on a linux with low-latency patch.

**Bugs identified/remaining:**

* Container memory size limit is discarded on Raspberry Pi 4
* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL
* Memory consumption reflects the host memory and not the docker memory
* macvlan not working as expected on Raspberry Pi4 with some network configurations (one workaround is to ping first from inside the container)

**Not yet tested:**
* FB_DLL

**Tested on:**

* ubuntu 20.04.4 amd64 with low-latency patch (docker 19.03.8)
* ubuntu 18.04.4 amd64 (docker 19.03.8)
* Raspbian buster (Rpi 4) (docker 19.03.8) Known limitation for some users: only ipvlan is working as expected
* Debian 10.3.0 amd 64 (docker 19.03.8)
* Window 10 2004 with WSL2 support (docker desktop)
* Revolution Pi Connect (docker 19.03.8). Known limitation: only macvlan is supported
* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported

**Not officially supported:**
* Window 10 2004 with WSL2 support (docker desktop)
---

# Soft dPAC Docker Linux v20.2 - develop - 610
_Delivered on 07/07/2020 - for EAE 20.2 (ring 0)_ 

Changes compared to previous version:

**Added features:**
* Support for BM_FILE and IoNet library
* Support for FB_DLL

**Bugs fixed:**

* None

**Bugs identified/remaining:**

* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL
* Memory consumption reflects the host memory and not the docker memory
* Thread priorities not managed properly for real-time applications even on a linux with low-latency patch.
* macvlan not working as expected on Raspberry Pi4 with some network configurations (one workaround is to ping first from inside the container)

**Not yet tested:**

* Modbus TCP scanner performance and advanced modes
* Persistence data and offline parametrization

**Tested on:**

* ubuntu 18.04.4 amd64 (docker 19.03.8)

* Raspbian buster (Rpi 4) (docker 19.03.8) Known limitation for some users: only ipvlan is working as expected

* Debian 10.3.0 amd 64 (docker 19.03.8)

* Revolution Pi Connect (docker 19.03.8). Known limitation: only macvlan is supported

* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported

---

# Soft dPAC Docker Linux v20.2 - develop - 377
_Delivered on 15/06/2020 - for EAE 20.2 (ring 0)_ 

Changes compared to previous version:

**Added features:**
* Eco Runtime updated to master branch to include all new features developed for EAE v20.2
* OPCUA stack updated to v1.4.1
* Compilation options updated for better execution performance
* Start script updated to support bridge networks for test on windows WSL2

**Bugs fixed:**

* None

**Bugs identified/remaining:**

* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL

* Memory consumption reflects the host memory and not the docker memory

**Not yet tested:**

* Modbus TCP scanner performance and advanced modes

* Persistence data

**Tested on:**

* ubuntu 18.04.4 amd64 (docker 19.03.8)

* Raspbian buster (Rpi 4) (docker 19.03.8) Known limitation for some users: only ipvlan is supported

* Debian 10.3.0 amd 64 (docker 19.03.8)

* Revolution Pi Connect (docker 19.03.8). Known limitation: only macvlan is supported

* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported

---
# Soft dPAC Docker Linux v20.1 - release - 346
_Delivered on 26/05/2020 - Official version for EAE 20.1 (rings 0,1 & 2)_ 

Changes compared to previous version:

**Bugs fixed:**

* Fix OPCUA stack build to ensure consistency with EcoRT v20.1.

**Bugs identified/remaining:**

* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL

* Memory consumption reflects the host memory and not the docker memory

**Not yet tested:**

* Modbus TCP scanner performance and advanced modes

* Persistence data

**Tested on:**

* ubuntu 18.04.4 amd64 (docker 19.03.8)

* Raspbian buster (Rpi 4) (docker 19.03.8)

* Debian 10.3.0 amd 64 (docker 19.03.8)

* Revolution Pi Connect (docker 19.03.8). Known limitation: only macvlan is supported

* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported

---
# Soft dPAC Docker Linux v20.1 - develop - 258
_Delivered on 12/05/2020 - for EAE 20.1 (ring 0)_ 

Changes compared to previous version:

**Added features:**

* Cross communication with other targets.

* Soft dpac files managed in docker volumes instead of host binding

* OPCUA server starts at boot without deploying configuration

* Boot project

* Modbus TCP scanner basic mode with a single device

**Bugs fixed:**

* OPCUA deploy configuration from EAE

**Bugs identified/remaining:**

* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL

* Memory consumption reflects the host memory and not the docker memory

**Not yet tested:**

* Modbus TCP scanner performance and advanced modes

* Persistence data

**Tested on:**

* ubuntu 18.04.4 amd64 (docker 19.03.8)

* Raspbian buster (Rpi 4) (docker 19.03.8)

* Debian 10.3.0 amd 64 (docker 19.03.8)

* Revolution Pi Connect (docker 19.03.8). Known limitation: only macvlan is supported

* HMIBSC (Yocto with docker 18.9 package). Known limitation: only macvlan is supported

---

# Soft dPAC Docker Linux v20.1 - develop - 107
_Delivered on 03/04/2020 - for EAE 20.1 (ring 0)_ 

Changes compared to previous version:

**Added features:**

* Login/deploy application

* Debugging with watches

* Cross communication

* Most of the function blocks of the core nxt libraries

* Deploy device configuration (nb: ntp configuration is useless as it can’t be set for one docker and must be set for the host directly)

* CAT functionality with HMI part

* OPCUA server (very early version, only basic tests have been performed and we found a bug : the studio deploys config files with CRLF line ending whereas the EcoRT expects LF line endings => current workaround consists in changing the line ending manually on the target after deploy).

**Bugs identified:**

* Cpu load (MIBGET) is not correct due to the docker context. We have to adapt the OSAL

* Memory consumption reflects the host memory and not the docker memory

**Not yet tested:**

* Modbus TCP scanner and server (these are part of the EcoRT though so it should work)

* Boot project

* Cross communication with other targets.

**Tested on:**

* ubuntu 18.04.4 amd64 (docker 19.03.8)

* Raspbian buster (Rpi 4) (docker 19.03.8)
