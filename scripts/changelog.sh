#!/bin/sh -e

while getopts "t:d:p:" flag
do
    case ${flag} in
        t) token=${OPTARG};;
        d) data=${OPTARG};;
        p) project_id=${OPTARG};;
    esac
done

curl \
-k \
--request POST \
--header "PRIVATE-TOKEN: ${token}" \
--data "${data}" "https://gitlab.medsigroup.ru/api/v4/projects/${project_id}/repository/changelog"