#!/bin/sh
# auth andre.yang
dir=$1
workspace=$2
cd $workspace

str=$(sed -n '1,1p' $workspace/version.txt)

cd $dir

cat ${str#*:}.log change.log >change2.log

mv change2.log ${str#*:}.log

sort ${str#*:}.log | uniq >${str#*:}_2.log

mv ${str#*:}_2.log ${str#*:}.log
