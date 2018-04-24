#!/usr/bin/env bash

branchName="${1}"
while [[ -z ${branchName} ]]
do
  read -p "Indiquer le nom de la branche à fusionner : " branchName
done

git checkout development
git pull origin development
git checkout ${branchName}
git rebase development

git rebase -i development

git checkout development
git merge ${branchName}
git push origin development
