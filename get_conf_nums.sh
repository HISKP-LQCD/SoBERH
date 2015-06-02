#!/bin/bash
ls -lh *values* | awk '{if($5!=0) print $9}' | cut -c 13-16 | sort -u 
