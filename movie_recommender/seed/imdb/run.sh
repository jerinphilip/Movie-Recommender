#!/bin/bash

wget -c -i files.list -q --show-progress
ls *.gz | xargs -I% gzip -d %
