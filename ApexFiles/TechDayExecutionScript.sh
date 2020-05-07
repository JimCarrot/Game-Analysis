#!/bin/bash
echo "Password Accepted"

#cd /usr/local/src/floodlight-master
#xterm -hold -e 'java -jar target/floodlight.jar' &
#sleep 3s

#Run Docker Image
sudo xterm -hold -e 'sudo docker run -it --net="host" --name ONAP_APEX --rm  nexus3.onap.org:10003/onap/policy-apex-pdp:2.1-SNAPSHOT-latest' &
sleep 10s

#Copy ApexFiles to Docker
sudo xterm -e 'sudo docker cp ~/Documents/ApexFiles/ ONAP_APEX:/home/apexuser/examples' &

#Run Apex Engine
sudo xterm -hold -e 'sudo docker exec -ti ONAP_APEX sh -c "apexApps.sh engine -c examples/ApexFiles/config/MyFirstPolicyConfigWs2WsServerJsonEvent.json"' &
sleep 5s

#Run Full Client
sudo xterm -hold -e 'sudo docker exec -ti ONAP_APEX sh -c "apexApps.sh full-client"' &

read -p "Press Cntrl-C to close... "


