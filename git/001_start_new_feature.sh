#!/usr/bin/env bash

branchName="${1}"
while [[ -z ${branchName} ]]
do
  read -p "Indiquer le nom de la branche à créer : " branchName
done
git checkout -b ${branchName}
