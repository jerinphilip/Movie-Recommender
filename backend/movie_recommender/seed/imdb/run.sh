#!/bin/bash

wget -c -i files.list
ls *.gz | xargs -I% gzip -d %
