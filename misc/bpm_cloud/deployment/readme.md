# Deployment

## Contents

This section contains deployment examples for the dockerized version. See how to run the application in a classic environment state in [readme.md](../readme.md#markdown-header-running-the-application)

## Requirements

> A docker repository is mandatory to deploy using Swarm or Kubernetes

### Configurations

Use the [minimal.yml](./swarm/minimal.yml) configuration as a base to deploy your application.

### Passwords

You can generate password by either using ```generate-password.sh``` or ```generate-password.ps1``` depending on your current OS. Those scripts require **openssl** to be installed.

### Repository login

You need to be logged on your repository to be able to deploy. The only alternative is to set credentials in the config.json file of your Docker service (in your current user's main folder in Windows) and restart the service.

## Swarm

For **Swarm**'s yml files, the user is **expected to set** the ```BPM_REPO``` environment variable.

Use following command lines:
```sh
export BPM_REPO=nexus.serphydose.local:5000
```
or
```ps1
Set-Item -path env:BPM_REPO -value "nexus.serphydose.local:5000"
```

This needs to be done before running the ```stack deploy``` command.

Once passwords are generated and environment variable is set, simply run:

```sh
 docker stack deploy -c minimal.yml --with-registry-auth --resolve-image always $STACKNAME
```

The ```--resolve-image always``` option is not mandatory.



