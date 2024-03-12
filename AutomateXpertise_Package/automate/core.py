# automate/core.py

"""Import module"""
import os
import ipaddress
import socket
import sys
import subprocess
import psutil
import docker

client = docker.from_env()

def create_macvlan_link(interface):
    """Crée le lien macvlan à la carte réseau"""
    os.system(f"sudo ip link add automatex link {interface} type macvlan mode bridge 2> /dev/null")

def add_host_ip_to_network(ip, network):
    """Ajoute l'adresse IP hôte au réseau"""
    os.system(f"sudo ip addr add {ip}/{network.prefixlen} dev automatex 2> /dev/null")

def activate_network():
    """Active le réseau"""
    os.system("sudo ip link set automatex up")

def pull_docker_image():
    """Récupère l'image docker"""
    os.system("docker pull skillseries/automatexpertise")

def get_user_input():
    """Demande à l'utilisateur l'adresse IP désirée pour le conteneur"""
    while True:
        ip_conteneur = input("Veuillez entrer l'adresse IP (IPv4) désirée pour le conteneur: ")
        try:
            ip = ipaddress.IPv4Address(ip_conteneur)
            return ip
        except ipaddress.AddressValueError:
            print("Adresse IP invalide. Veuillez saisir une adresse IPv4 valide.")

def run_container_host(enterprise):
    """Lancement du conteneur en mode host"""
    container_name = f"automatexpertise-{enterprise}"
    containers = client.containers.list(all=True)

    if container_name not in [container.name for container in containers]:
        os.system(f"""
        docker run -d \
        --name {container_name} \
        --network host \
        --cap-add NET_RAW \
        --cap-add NET_ADMIN \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v /etc/localtime:/etc/localtime \
        -v /etc/timezone:/etc/timezone \
        skillseries/automatexpertise 
        """)
        print(f"Le conteneur {container_name} a été créé avec succès. Son IP: localhost")
    else:
        print(f"Le conteneur {container_name} existe déjà.")

def run_container_macvlan(ip, enterprise):
    """Lance du conteneur en mode macvlan"""
    containers = client.containers.list(all=True)
    container_name = f"automatexpertise-{enterprise}"

    if container_name not in [container.name for container in containers]:
        os.system(f"""
        docker run -d \
        --name {container_name} \
        --network automatex --ip {ip} \
        --cap-add NET_RAW \
        --cap-add NET_ADMIN \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v /etc/localtime:/etc/localtime \
        -v /etc/timezone:/etc/timezone \
        skillseries/automatexpertise
        """)
        print(f"Le conteneur {container_name} a été créé avec succès. Son IP: {ip}")
    else:
        print(f"Le conteneur {container_name} existe déjà.")

def macvlan_mode(name):
    """Configuration du macvlan"""
    global selected_interface

    # Obtenir le nom de l'entreprise
    enterprise = name
    # Obtenir le nom d'hôte de la machine locale
    hostname = socket.gethostname()

    # Obtenir la liste des objets de réseau
    interfaces = psutil.net_if_addrs()

    # Affiche une liste numérotée d'interfaces
    print("Voici la liste de vos interfaces")
    for i, (interface, addrs) in enumerate(interfaces.items(), 1):
        print(f"{i}. {interface}")

    # Demande à l'utilisateur de choisir une interface
    selected_interface = None
    while selected_interface is None:
        try:
            selection = int(input("Sélectionnez le numéro de l'interface: "))
            if 1 <= selection <= len(interfaces):
                selected_interface = list(interfaces.keys())[selection - 1]
            else:
                print("Numéro invalide. Veuillez sélectionner un numéro valide.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")

    # Obtenir l'adresse IP associée à l'interface sélectionnée
    selected_interface_addrs = interfaces[selected_interface]

    selected_ip = next((
        addr.address for addr in selected_interface_addrs if addr.family == socket.AF_INET)
        , None)

    # Obtenir le masque de sous-réseau de l'interface sélectionnée
    selected_netmask = next((
        addr.netmask for addr in selected_interface_addrs if addr.family == socket.AF_INET and addr.netmask
        ), None)

    # Calcul de l'adresse réseau et du CIDR en fonction de l'adresse IP et du masque
    ip_network = ipaddress.IPv4Network(f"{selected_ip}/{selected_netmask}", strict=False)

    # Création du réseau macvlan docker
    networks = client.networks.list()
    automatex_network_exists = any(network.name == "automatex" for network in networks)

    if not automatex_network_exists:
        os.system(f"""
        docker network create -d macvlan \
        --subnet={ip_network.network_address}/{ip_network.prefixlen} \
        --aux-address='{hostname}={selected_ip}' \
        -o macvlan_mode=bridge \
        -o parent={selected_interface} \
        --attachable automatex
        """)
        client.close()
        create_macvlan_link(selected_interface)
        add_host_ip_to_network(selected_ip, ip_network)
        activate_network()
        pull_docker_image()
        ip_conteneur = get_user_input()
        run_container_macvlan(ip_conteneur, enterprise)
    else:
        client.close()
        create_macvlan_link(selected_interface)
        add_host_ip_to_network(selected_ip, ip_network)
        activate_network()
        pull_docker_image()
        ip_conteneur = get_user_input()
        run_container_macvlan(ip_conteneur, enterprise)

def host_mode(name):
    """Configuration du mode host"""
    enterprise = name

    # Obtenir la liste des objets de réseau
    interfaces = psutil.net_if_addrs()

    # Affiche une liste numérotée d'interfaces
    print("Voici la liste de vos interfaces")
    for i, (interface, addrs) in enumerate(interfaces.items(), 1):
        print(f"{i}. {interface}")

    # Demande à l'utilisateur de choisir une interface
    selected_interface = None
    while selected_interface is None:
        try:
            selection = int(input("Sélectionnez le numéro de l'interface: "))
            if 1 <= selection <= len(interfaces):
                selected_interface = list(interfaces.keys())[selection - 1]
            else:
                print("Numéro invalide. Veuillez sélectionner un numéro valide.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")

    pull_docker_image()
    run_container_host(enterprise)

def create_container(name):
    """Demande à l'utilisateur le mode de création du conteneur"""
    while True:
        print("""
Voici les modes de configuration disponible:
1. Host
2. MacVlan
q. Quit
""")
        mode = input("Quel est votre choix: ")
        if mode == "1":
            host_mode(name)
            sys.exit(0)
        elif mode == "2":
            macvlan_mode(name)
            sys.exit(0)
        elif mode.lower() == "q":
            sys.exit(0)
        else:
            print("Veuillez choisir une option valide.")

def list_containers():
    """Listing des conteneurs"""
    try:
        # Liste tous les conteneurs Docker
        all_containers = client.containers.list(all=True)

        # Filtrer les conteneurs qui commencent par "automatexpertise-"
        automatexpertise_containers = [container for container in all_containers if container.name.startswith('automatexpertise-')]

        # Filtrer les conteneurs actifs et inactifs
        active_containers = [container for container in automatexpertise_containers if container.status == 'running']
        inactive_containers = [container for container in automatexpertise_containers if container.status != 'running']

        # Affichage des résultats
        print("Containeurs actifs :")
        for container in active_containers:
            print(container.name)

        print("\nConteneurs inactifs :")
        for container in inactive_containers:
            print(container.name)
    except docker.errors.APIError as e:
        print(f"Erreur lors du listing des conteneurs: {str(e)}")
    finally:
        client.close()

def configure_network_host():
    """Configuration du réseau host"""
    # Obtenir la liste des objets de réseau
    interfaces = psutil.net_if_addrs()

    # Affiche une liste numérotée d'interfaces
    print("Voici la liste de vos interfaces")
    for i, (interface, addrs) in enumerate(interfaces.items(), 1):
        print(f"{i}. {interface}")

    # Demande à l'utilisateur de choisir une interface
    selected_interface = None
    while selected_interface is None:
        try:
            selection = int(input("Sélectionnez le numéro de l'interface: "))
            if 1 <= selection <= len(interfaces):
                selected_interface = list(interfaces.keys())[selection - 1]
            else:
                print("Numéro invalide. Veuillez sélectionner un numéro valide.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")

def configure_network_macvlan():
    """Configuration du réseau macvlan"""
    # Obtenir la liste des objets de réseau
    interfaces = psutil.net_if_addrs()

    # Affiche une liste numérotée d'interfaces
    print("Voici la liste de vos interfaces")
    for i, (interface, addrs) in enumerate(interfaces.items(), 1):
        print(f"{i}. {interface}")

    # Demande à l'utilisateur de choisir une interface
    selected_interface = None
    while selected_interface is None:
        try:
            selection = int(input("Sélectionnez le numéro de l'interface: "))
            if 1 <= selection <= len(interfaces):
                selected_interface = list(interfaces.keys())[selection - 1]
            else:
                print("Numéro invalide. Veuillez sélectionner un numéro valide.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")

    # Obtenir l'adresse IP associée à l'interface sélectionnée
    selected_interface_addrs = interfaces[selected_interface]

    selected_ip = next((
        addr.address for addr in selected_interface_addrs if addr.family == socket.AF_INET)
        , None)

    # Obtenir le masque de sous-réseau de l'interface sélectionnée
    selected_netmask = next((
        addr.netmask for addr in selected_interface_addrs if addr.family == socket.AF_INET and addr.netmask
        ), None)

    # Calcul de l'adresse réseau et du CIDR en fonction de l'adresse IP et du masque
    ip_network = ipaddress.IPv4Network(f"{selected_ip}/{selected_netmask}", strict=False)

    # Création du réseau macvlan docker
    create_macvlan_link(selected_interface)
    add_host_ip_to_network(selected_ip, ip_network)
    activate_network()
    client.close()

def run_command_macvlan(command):
    """Démarrage conteneur en mode macvlan"""
    try:
        # Exécute la commande en utilisant subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        # Vérifie si la commande s'est exécutée avec succès
        if result.returncode == 0:
            # Récupère la sortie (output) de la commande
            output = result.stdout.strip()
            return output
        else:
            error_message = result.stderr.strip()
            return f"Erreur lors de l'exécution de la commande : {error_message}"
    except Exception as e:
        return f"Erreur : {str(e)}"

def start_container(container_name):
    """Démarrer le conteneur"""
    try:
        # Récupérer le conteneur spécifique inactif avec le nom saisi
        container = client.containers.get(container_name)

        # Vérifie le mode réseau du conteneur
        network_mode = container.attrs['HostConfig']['NetworkMode']

        # Démarrer le conteneur spécifique
        container.start()

        # Rétablir la configuration réseau en fonction du mode initial
        if network_mode == 'host':
            configure_network_host()
            print(f"Le conteneur {container_name} a été créé avec succès. Son IP: localhost")
        elif network_mode == 'automatex':
            configure_network_macvlan()
    except docker.errors.NotFound:
        print(f"Le conteneur {container_name} n'a pas été trouvé.")
    except docker.errors.APIError as e:
        print(f"Erreur lors du démarrage du conteneur {container_name}: {str(e)}")
    finally:
        # exécuter une commande "docker inspect" pour obtenir l'adresse IP
        command = f"docker inspect -f '{{{{ .NetworkSettings.Networks.automatex.IPAddress }}}}' {container_name}"
        container_ip = run_command_macvlan(command)
        print(f"Le conteneur {container_name} a démarré avec succès. Son IP est: {container_ip}")
        client.close()

def stop_container(container_name):
    """Arrêt du conteneur"""
    try:
        # Récupère le conteneur par son nom
        container = client.containers.get(container_name)

        # Arrête le conteneur
        container.stop()

        print(f"Le conteneur {container_name} a été arrêté avec succès.")
    except docker.errors.NotFound:
        print(f"Le conteneur {container_name} n'a pas été trouvé.")
    except docker.errors.APIError as e:
        print(f"Erreur lors de l'arrêt du conteneur {container_name}: {str(e)}")
    finally:
        client.close()

def delete_container(container_name):
    """Suppression du conteneur"""
    try:
        # Récupère le conteneur par son nom
        container = client.containers.get(container_name)

        if container.status == 'running':
            print(f"Le conteneur {container_name} est en cours d'exécution. Arrêtez le d'abord.")
        else:
            # Supprime le conteneur
            container.remove()
            print(f"Le conteneur {container_name} a été supprimé avec succès.")
    except docker.errors.NotFound:
        print(f"Le conteneur {container_name} n'a pas été trouvé.")
    except docker.errors.APIError as e:
        print(f"Erreur lors de la suppression du conteneur {container_name}: {str(e)}")
    finally:
        client.close()
