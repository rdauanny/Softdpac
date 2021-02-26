#!/bin/sh
# startSoftdPAC.sh
# short-description: Script use to create network and to start containers
# 14-02-20 : add parameters and checks
# 07-04-20 : add subnet mask and change folder and instance name

i=1
nCPUs=$(nproc)
readonly maxIp=254
readonly maxPublishPortValue=65535
readonly minPublishPortValue=1024
readonly maxMemoryArm=256
readonly maxMemoryX86=512
readonly maxLogSize=10

# default value for parameters
containerName="softdpac_"
ipBase="192.168.1.10"
gateway=""
ipMask=24
nbContainer=1
maxMemory=$maxMemoryArm

networkType="macvlan"
networkName="softdpacNet"
readonly volumeName="softdpacVol"
readonly labelSoftdpac="softdpac"
interfaceName="eth0"

portNumber=51499

imageName=""
dirSuffix="_data"
maxIndexFolderAlreadyCreated=0


usage()
{
    printf "Usage: %s --image-name <valid image name> \
[--ipbase <ip addr base>] [--itname <interface name>] [--gateway <ip addr>] [--nbcontainer <nb container>] \
[--cname <container name>] [--network <type of network>] [--net-name <network name>]  \
[--publish-on <port number>]\n" "$0"

    printf "Options:\n"
    printf "\t     --image-name              : set image name to use (mandatory parameter);\n"
    printf "\t-g,  --gateway                 : set gateway ip address. Only IPv4 (default: Deduced from ipbase);\n"
    printf "\t-i,  --ipbase                  : set ip address base value and subnet mask. Only IPv4 and CIDR notation (default: 192.168.1.10/24);\n"
    printf "\t     --itname                  : set interface name (default: eth0);\n"
    printf "\t-n,  --nbcontainer             : set number of container to create (default: 1);\n"
    printf "\t     --cname                   : set container base name (default: softdpac_);\n"
    printf "\t     --network                 : set network type (default: macvlan; other value: ipvlan / bridge (bridge value used only on Windows WSL2);\n"
    printf "\t     --net-name                : set network name (default: softdpacNet);\n"
    printf "\t     --publish-on              : set port translation only used with bridge network type (default: 51499);\n"
    printf "\t-h                             : print this message.\n"
}

#check the kernel architecture
#set the memory limit
CheckKernelArchitecture()
{
    case $(uname -m) in
    *x86*) maxMemory=$maxMemoryX86;;
    *) maxMemory=$maxMemoryArm;;
    esac
    printf "Set the memory limit value to %sm\n" "$maxMemory"
}

CheckIPV4String()
{
    reqAddr=$(echo "$1" | grep -E -o '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
    echo "$reqAddr"
}

# check format of the ip address
# Format of the IP address must be x.x.x.x or x.x.x.x/y
CheckIPV4AddressValidity()
{
    ipAddress=$1
    reqAddr=$(CheckIPV4String "$ipAddress")
    if [ -n "$reqAddr" ]; then
        ipBase="$reqAddr"
    else
        reqAddrMask=$(echo "$ipAddress" | grep -E -o '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([1-9]|[1-2][0-9]|3[0-2]))$')
        if [ -n "$reqAddrMask" ]; then
            ipBase="${reqAddrMask%%/*}"
            ipMask="${reqAddrMask##*/}"
        else
            printf "Error: bad base ip address value or subnet mask\n"
            printf "Note that IP format must be : x.x.x.x/y or x.x.x.x with \"x\" between 0 and 255 and \"y\" between 1 and 32\n"
            exit 1
        fi
    fi
}

# check format of the publish port number
# There is 2 formatsForma
# - First only port number: 0 to 65535. we will used only value between 1024 to 65535. In this case all connections on this port on all IP address of the host are forward to container on relateve container port.
# - Second include the host IP address that we will used (not implemented): Format of the IP address must be x.x.x.x:y with y for port number. In this case, only all connections on this port and this IP address are forward to container on relateve container port.
CheckPublishPortNumberValidity()
{
    re=$(echo "$portNumber" | grep -E -o '^[0-9]+$')
    if [ -n "$re" ] ; then
        if [ "$portNumber" -lt "$minPublishPortValue" ] || [ "$portNumber" -gt "$maxPublishPortValue" ]; then
            printf "Error: bad publish port number\n"
            printf "Note publish port number must be an unsigned integer between 1024 to 65535\n"
            exit 1
        else
            maxPortNumberCalcul="$((portNumber+nbContainer-1))"
            if [ "$maxPortNumberCalcul" -gt "$maxPublishPortValue" ]; then
                printf "Error publish port: number of containers exceed max value\n"
                exit 1
            fi
        fi
    else
        printf "Error: bad publish port number\n"
        printf "Note publish port number must be an unsigned integer between 1024 to 65535\n"
        exit 1
    fi
}

# calculate subnet and gateway with IP base and mask value set in --ipbase parameter
calculSubnetAndBroadcast ()
{
    # Number of args to shift, 255..255, first non-255 byte, zeroes
    set -- $(( 5 - (ipMask / 8) )) 255 255 255 255 $(( (255 << (8 - (ipMask % 8))) & 255 )) 0 0 0
    if [ "$1" -gt 1 ]; then
        shift "$1"
    else
        shift
    fi
    subnetMask="${1-0}.${2-0}.${3-0}.${4-0}"

    sub1=$(echo "$subnetMask" | tr "." " " | awk '{ print $1 }')
    sub2=$(echo "$subnetMask" | tr "." " " | awk '{ print $2 }')
    sub3=$(echo "$subnetMask" | tr "." " " | awk '{ print $3 }')
    sub4=$(echo "$subnetMask" | tr "." " " | awk '{ print $4 }')

    ipRes1=$((ip1&sub1))
    ipRes2=$((ip2&sub2))
    ipRes3=$((ip3&sub3))
    ipRes4=$((ip4&sub4))
    subnet="$ipRes1.$ipRes2.$ipRes3.$ipRes4"
    broadcast="$((ipRes1+255-sub1)).$((ipRes2+255-sub2)).$((ipRes3+255-sub3)).$((ipRes4+255-sub4))"
}

calculateGateway()
{
    gateway="$ipRes1.$ipRes2.$ipRes3.$((ipRes4+1))"
    printf "Gateway will be: %s\n" "$gateway"
}

CheckInterfaceName()
{
    ip link show "$interfaceName" >/dev/null 2>&1
}

CheckNetwork()
{
    # Check interface we want to use
    # If interface already in use, exit script otherwise check network name and network type
    networkId="$(docker network ls -q --filter name="$networkName")"
    if [ -n "$networkId" ]; then
        netType="$(docker network ls -q --filter driver="$networkType" --filter id="$networkId")"
        if [ -n "$netType" ]; then
            printf "A network already exist with this name and driver type\n"
        else
            printf "A network already exist with this name\n"
        fi
        read -rp "Do you want to reset network and create a new one (y/N)?" RESULT_NETWORK
        case $RESULT_NETWORK in
            [Yy]* )
                EraseNetwork
                return 0
                ;;

            [Nn]* | * )
                return 1
                ;;
        esac
    else
        # check if interface is already in use in another network
        # exist if it's the case

        # The behavior is the one expected so it's necessary to disable the shellcheck parsing SC2046 for this line
        # shellcheck disable=2046
        interfaceInUse="$(docker network inspect -f '{{.Options.parent}}' $(docker network ls -q) | grep $interfaceName)"
        if [ -n "$interfaceInUse" ]; then
            printf "Only one network is authorized on interface %s\n" "$interfaceName"
            exit 1
        else
            return 0
        fi
    fi
}


# check if image is loaded
CheckImageName()
{
    docker image ls -q "$imageName"
}

#check if there are already containers linked to this network
CheckContainers()
{
    docker container ls -q --filter network="$networkName"
}

#check if ipbase or all ip you want to add are already used
CheckIPUser()
{
    loopIp=0
    while [ "$loopIp" -lt "$nbContainer" ]
    do
        ipLoop="$ip1.$ip2.$ip3.$((ip4+loopIp))"

        # The behavior is the one expected so it's necessary to disable the shellcheck parsing SC2046 for this line
        # shellcheck disable=2046
        ipBaseChecked="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aq) | grep "$ipLoop")"
        if [ -n "$ipBaseChecked" ]; then
            return 1
        fi

        loopIp=$((loopIp+1))
    done
    return 0
}

EraseContainers()
{
    # for each container in this network do not remove associated volume
    printf "Erase existing containers on network %s\n" "$networkName"

    # The behavior is the one expected so it's necessary to disable the shellcheck parsing SC2046 for this line
    # shellcheck disable=2046
    for containerList in $(docker container inspect --format '{{.Config.Hostname}}' $(docker ps -aq --filter network="$networkName")); do
        #check if container running before remove directory
        # stop container in that case
        statusContainer="$(docker container inspect --format '{{.State.Status}}' "$containerList")"
        if [ "$statusContainer" = "running" ]; then
            docker stop "$containerList"  >/dev/null
        fi

        docker container rm -f "$containerList"
    done
}

EraseNetwork()
{
    #to be able to remove the network its necessary to delete all containers on that network before
    if [ -n "$(CheckContainers)" ]; then
        EraseContainers
    fi
    printf "Erase existing networks %s\n" "$networkName"
    docker network rm $networkName
}

GetFolderMaxIndex()
{
    for dirList in *
    do
        dirName="$(echo "$dirList" | grep "$containerName")"
        if [ -n "$dirName" ]; then
            suffixFirstStep="${dirName#$containerName}"
            suffix="${suffixFirstStep%$dirSuffix}"
            if [ "$maxIndexFolderAlreadyCreated" -lt "$suffix" ]; then
                maxIndexFolderAlreadyCreated="$suffix"
            fi
        fi
    done
}

EraseVolume() {
    docker volume rm "$1"
}

CheckVolume() {
    index=$1

    exist=$(docker volume ls -q --filter label=softdpac --filter label=reference="${containerName}${index}")
    if [ -n "$exist" ]; then
        created=$(docker volume inspect --format '{{index .Labels "created"}}' "${volumeName}${index}")

        printf "A volume already exist with the name [%s] created on [%s], was used by container [%s]\n" "${volumeName}${index}" "${created}" "${containerName}${index}"
        read -rp "Do you want to reset volume and create a new one (Y), or reuse the exiting one (N): (y/N)?" RESULT_VOLUME
        case $RESULT_VOLUME in
            [Yy]* )
                EraseVolume "${volumeName}${index}"
                return 0
                ;;

            [Nn]* | * )
                return 1
                ;;
        esac
    fi
}

CreateVolume() {
    index=$1

    if CheckVolume "${index}"; then
        docker volume create --driver local --label "${labelSoftdpac}"=true \
            --label reference="${containerName}${index}" \
            --label created="$(date +%F-%T)" \
            "${volumeName}${index}"

        printf "Created volume [%s]\n" "${volumeName}${index}"
    fi
}

##################################### MAIN ########################################

if [ $# -eq 0 ]
then
    usage
fi

OPTS=$( getopt -o hi:n:g: -l gateway:,ipbase:,cname:,nbcontainer:,network:,net-name:,publish-on:,itname:,image-name: -- "$@" )
result="$?"

if [ "$result" != 0 ]
then
    printf "Error\n"
    exit 1
fi

eval set -- "$OPTS"

while true ; do
    case "$1" in
        -h) usage
            exit 0
            ;;
        -i | --ipbase)
                ipBase="$2"
                shift 2
                ;;
        -g | --gateway)
                gateway="$2"
                shift 2
                ;;
        --itname)
                interfaceName="$2"
                shift 2
                ;;
        --image-name)
                imageName="$2"
                shift 2
                ;;
        --cname)
                containerName="$2"
                shift 2
                ;;
        -n | --nbcontainer)
                nbContainer="$2"
                shift 2
                ;;
        --network)
                networkType="$2"
                shift 2
                ;;
        --net-name)
                networkName="$2"
                shift 2
                ;;
        --publish-on)
                portNumber="$2"
                shift 2
                ;;
        --)
                shift;
                break;;
    esac
done

#check that image name is set
if [ -z "$imageName" ]; then
    printf "Error: parameter --image-name is mandatory\n"
    exit 1
else
    #check that image is load
    if [ -z "$(CheckImageName)" ]; then
        printf "Error: No image corresponding to this name: %s\n" "$imageName"
        exit 1
    fi
fi

# check kernel architecture to set the memory limit
CheckKernelArchitecture

# check ip format
CheckIPV4AddressValidity "$ipBase"
# check also gateway if needed
if [ -n "$gateway" ]; then
    gw=$(CheckIPV4String "$gateway")
    if [ -z "$gw" ]; then
        printf "gateway %s has invalid format" "$gw"
        exit 1
    fi
fi

ip1=$(echo "$ipBase" | tr "." " " | awk '{ print $1 }')
ip2=$(echo "$ipBase" | tr "." " " | awk '{ print $2 }')
ip3=$(echo "$ipBase" | tr "." " " | awk '{ print $3 }')
ip4=$(echo "$ipBase" | tr "." " " | awk '{ print $4 }')

calculSubnetAndBroadcast
# calcul subnet and gateway if needed
if [ -z "$gateway" ]; then
    calculateGateway
fi

if [ "$ipBase" = "$gateway" ] || [ "$ipBase" = "$subnet" ] || [ "$ipBase" = "$broadcast" ]; then
    printf "Error: bad base ip address value or subnet mask\n"
    printf "Note that IP must be different of gateway (%s), subnet (%s) and broadcast address (%s)\n" "$gateway" "$subnet" "$broadcast"
    exit 1
fi


#check interface name
if ! CheckInterfaceName; then
    printf "Error: bad interface name: %s\n" "$interfaceName"
    exit 1
fi

#check that number of containers doesn't exceed authorized value
maxIpCalcul="$((ip4+nbContainer))"
if [ "$maxIpCalcul" -gt "$maxIp" ]; then
    printf "Error: number of containers exceed max value\n"
    exit 1
fi

# Test if network already exist and create it only if it doesn't exist
# Create a ipvlan network or a macvlan network
# Add label to allow system to delete network easily
if CheckNetwork; then
    if [ "$networkType" = "ipvlan" ]; then
        docker network create -d ipvlan -o ipvlan_mode=l2 \
        --ipv6 --subnet="fe80::1/64" --gateway=fe80::1 \
        --subnet="$subnet/$ipMask" --gateway="$gateway" \
        -o parent="$interfaceName" \
        --label="$labelSoftdpac"=true \
        "$networkName" || exit 1

    elif [ "$networkType" = "macvlan" ]; then
        docker network create -d macvlan \
        --ipv6 --subnet="fe80::1/64" --gateway=fe80::1 \
        --subnet="$subnet/$ipMask" --gateway="$gateway" \
        -o parent="$interfaceName" \
        --label="$labelSoftdpac"=true \
        "$networkName" || exit 1

    elif [ "$networkType" = "bridge" ]; then
        printf "Warning: used network bridge is only recommended for Docker on Windows WSL2\n"
        docker network create -d bridge \
        --subnet="$subnet/$ipMask" --gateway="$gateway" \
        -o parent="$interfaceName" \
        --label="$labelSoftdpac"=true \
        "$networkName" || exit 1
    else
        printf "Error: network type is not managed\n"
        exit 1
    fi
fi

#check publish port value incase of used bridge network type
if [ "$networkType" = "bridge" ]; then
    CheckPublishPortNumberValidity
fi

#check if there are already containers on network name
if [ -n "$(CheckContainers)" ]; then
    printf "Containers already exist on that network\n"
    read -rp "Do you want to create $nbContainer new containers and delete existing ones (y/N)?" RESULT_CONTAINERS
    case $RESULT_CONTAINERS in
        [Yy]* )
            EraseContainers
            ;;

        [Nn]* | * )
            printf "Increment existing containers based on IP %s\n" "$ipBase"
            if ! CheckIPUser; then
                printf "One or several IP you want to add are already used\n"
                exit 1
            fi
            ;;
    esac
fi

# get max index value of the folder name associated to the container
GetFolderMaxIndex

while [ "$i" -le "$nbContainer" ]
do

    # variable "i" start at 1 but IpEnd must start with ip4 base value
    ipEnd="$((ip4+i-1))"
    ipNr="$ip1.$ip2.$ip3.$ipEnd"
    cpu="$(((i-1) % nCPUs))"
    publishMsg=""
    publishParam=""

    indexNewFolder=$((i+maxIndexFolderAlreadyCreated))

    if [ ! "$(docker ps -q -f name="$containerName$indexNewFolder")" ]; then

        CreateVolume "$indexNewFolder"

        if [ "$networkType" = "bridge" ]; then
            portNumberContainer="$((portNumber+i-1))";
            publishMsg=", publish port $portNumberContainer"
            publishParam="--publish  $portNumberContainer:51499"
        fi

        printf "Setup %s on IP %s, on cpu %s%s\n" "$containerName$indexNewFolder$dirSuffix" "$ipNr" "$cpu" "$publishMsg"

        # The behavior is the one expected so it's necessary to disable the shellcheck parsing SC2086 for this line
        # shellcheck disable=2086
        docker run -d --restart unless-stopped --privileged --cpuset-cpus "$cpu" --cap-add sys_nice \
            -v "${volumeName}${indexNewFolder}":/var/lib/nxtSRT61499N/data \
            --network "$networkName" \
            --ip "$ipNr" \
            --name "$containerName$indexNewFolder" \
            --hostname "$containerName$indexNewFolder" \
            --memory "${maxMemory}m" \
            --log-opt max-size="${maxLogSize}m" \
            --log-opt max-file=1 \
            $publishParam \
            "$imageName" || exit 1

    else
        printf "Container %s already created\n" "$containerName$indexNewFolder"
    fi

    i=$((i+1))
done

exit 0
