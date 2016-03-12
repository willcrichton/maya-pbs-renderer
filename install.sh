#!/bin/bash

# Maya installation script for CentOS/RHEL. Uses network, not standalone, licenses.

# Download the most recent version of Maya for Linux (if there's a service pack available, choose
# that one) and put this install script in that directory. Create a subdirectory called "mentalray"
# and put the mentalray files in there (download the plugin renderer, not the standalone). Update
# the variables below as needed.

LICENSE_SERVER=<your license server here>
PRODUCT_CODE=657H1

sudo yum install libXp
sudo rpm -ivh --replacepkgs Maya*.rpm mentalray/mentalrayForMaya*.rpm
/usr/autodesk/maya/bin/licensechooser /usr/autodesk/maya network ${PRODUCT_CODE} maya
sudo mkdir -p /var/flexlm
sudo chmod 777 /var/flexlm
printf "SERVER ${LICENSE_SERVER} 0\nUSE_SERVER" > /var/flexlm/maya.lic
