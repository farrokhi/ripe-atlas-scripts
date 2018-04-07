#!/bin/sh
for domain in `cat top100.txt`; do
    printf "${domain}\t\t"
    res=`dig +short DNSKEY ${domain} | sed -e 's/\r//g'`
    if [ -n "${res}" ]; then
        echo "YES\t\t ${res}"
    else
        echo "NO"
    fi
done
