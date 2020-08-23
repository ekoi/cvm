#!/bin/bash
echo "HELLO INDARTO" >> /tmp/status.log
until curl -sS -f "http://dataverse:8080/robots.txt" -m 2 2>&1 > /dev/null;
    do echo ">>>>>>>> Waiting for Dataverse...." >> /tmp/status.log; echo "---- Dataverse is not ready...." >> /tmp/status.log; sleep 5; done;
    echo "Dataverse is running...!" >> /tmp/status.log;
echo "---Enjoy Dataversing--" >> /tmp/status.log