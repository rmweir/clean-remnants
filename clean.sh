#!/bin/bash

projects_output="$(kubectl get projects --all-namespaces | grep -E -o ".p-.{0,6}")"

for i in "${!projects_output[@]}"; do
	echo "$i"
done
