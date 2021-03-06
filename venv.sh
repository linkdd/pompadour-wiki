#!/bin/sh

cwd=`pwd`
vdir=$cwd/pompadour_wiki/.venv

if [ "$1" != "update" ]
then
     rm -rf $vdir > /dev/null 2>&1

     echo "-- Creating virtual environment: $vdir..."
     virtualenv $vdir || exit 1

     echo "-- Activating virtual environment: $vdir..."
     source $vdir/bin/activate || exit 1

     echo "-- Installing dependencies in virtual environment..."
     pip install -r requirements.txt
else
     echo "-- Updating virtual environment: $vdir..."
     pip install -U -r requirements.txt
fi

