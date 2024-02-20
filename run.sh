#!/bin/bash

while getopts s: flag
do
    case "${flag}" in
        s) sensor=${OPTARG};;
    esac
done

echo "Processing sensor: $sensor";
