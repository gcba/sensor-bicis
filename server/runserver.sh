#!/bin/bash

. ./bin/activate

until ./server.py; do
    echo "Server 'server.py' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
