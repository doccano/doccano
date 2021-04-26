# Doccano Offline Deployment

## Use Case
These offline deployment scripts are suited for deploying Doccano on an air gapped Ubuntu 18.04/20.04 virtual machine (VM 2) with no internet connectivity (such as in clinical environments).

The preparation requires another machine (VM 1) with internet access and `docker`/`docker-compose` preinstalled (with $USER in `docker` group) and running the same Ubuntu distribution as VM 2.  

The focus is primarily on the `docker-compose`-based production deployment.
The files mentioned in this document are located in the `tools/offline_deployment/` directory.

## Setup Steps

Run the following steps on VM 1:  
1. Clone this repository  
2. Run the scripts `offline_01_*.sh` in ascending order  
   Skip OR modify and run the script `offline_01_1-optional_use_https`  
   Do NOT run these scripts as `sudo`! The scripts will ask for sudo-permissions when it is needed.  

Now, move over to VM 2  

3. Copy the repository folder from VM 1 to VM 2  
4. Run the scripts `offline_02_*.sh` in ascending order  
   Do NOT run these scripts as `sudo`! The scripts will ask for sudo-permissions when it is needed.  
5. Make minor changes on `docker-compose.prod.yml` to change the admin credentials  
6. Run `docker-compose -f docker-compose.prod.yml up` in the repository root directory or use the script `offline_03_*.sh`  

## Remarks

The setup was tested on Ubuntu 18.04 machines.