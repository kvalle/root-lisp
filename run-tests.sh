#!/bin/sh

while inotifywait -r -e modify . ; do
    nosetests
done
