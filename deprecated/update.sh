#!/usr/bin/env bash


echo "Starting site maintenance."

maintenanceon

reset

updateall

maintenanceoff

echo "Site maintenance complete!"