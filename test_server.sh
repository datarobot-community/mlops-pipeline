#!/bin/bash
nohup python server.py &
sleep 10
pytest servertest.py -o junit_family=xunit2 --junitxml=/python-test-server/reports/result.xml
tail -f /dev/null