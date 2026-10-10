import argparse
import os
import subprocess
import json

def get_containers():
    containers = subprocess.check_output(['docker', 'ps', '-a']).decode('utf-8')
    return containers.split('\n')

def get_logs(container_name):
    logs = subprocess.check_output(['docker', 'logs', container_name]).decode('utf-8')
    return logs.split('\n')

def create_container(name, image):
    subprocess.run(['docker', 'run', '-d', '--name', name, image])

def delete_container(name):
    subprocess.run(['docker', 'rm', '-f', name])

def main():
    parser = argparse.ArgumentParser(description='Controlla CLI utility')
    parser.add_argument('--start', help='Start a new container')
    parser.add_argument('--stop', help='Stop a container')
    parser.add_argument('--delete', help='Delete a container')
    parser.add_argument('--logs', help='Get logs of a container')
    args = parser.parse_args()

    if args.start:
        create_container(args.start, 'alpine')
        print(f'Container {args.start} started')

    elif args.stop:
        delete_container(args.stop)
        print(f'Container {args.stop} stopped')

    elif args.delete:
        delete_container(args.delete)
        print(f'Container {args.delete} deleted')

    elif args.logs:
        logs = get_logs(args.logs)
        for log in logs:
            print(log)

    else:
        containers = get_containers()
        for container in containers:
            if container:
                print(container)

if __name__ == '__main__':
    main()