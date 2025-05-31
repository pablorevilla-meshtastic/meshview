#!/bin/bash
/opt/conda/envs/meshview/bin/python /app/startdb.py --config /app/config.ini &
/opt/conda/envs/meshview/bin/python /app/main.py --config /app/config.ini &
wait