#!/usr/bin/env bash

SCRIPT=$(readlink -f "${0}")
THIS_PATH=$(dirname "${SCRIPT}")

cd ${THIS_PATH}

./parse.py /home/dlezz/projects/robottelo-fork/tests