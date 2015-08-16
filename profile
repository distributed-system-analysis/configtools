# -*- mode: shell-script -*-
if [[ -z "$TOP" ]]; then
    # keep going up until we get to the rpm directory
    export TOP=$PWD
    while [[ ! -f $TOP/setup.py && ! -d $TOP/configtools ]]; do
        TOP=$(dirname $TOP)
        if [[ "$TOP" = "/home/$USER" || "$TOP" = "/home" || "$TOP" = "/" ]]; then
            break
        fi
    done
fi
prefix=$TOP

pathins() {
    if [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]]; then
        PATH="$1:$PATH"
    fi
}
ppathins() {
    if [ -d "$1" ] && [[ ":$PYTHONPATH:" != *":$1:"* ]]; then
        PYTHONPATH="$1:$PYTHONPATH"
    fi
}

# this file is *only* used by unit tests and for in-tree
# development: it is *not* part of the RPM.

# So *always* use the in-tree version of configtools here.
# prefix better be right at this point
if [[ ! -f $prefix/build/bin/getconf.py ]]
then
    echo "Cannot find getconf.py: $prefix/build/bin/getconf.py"
else
    (cd $prefix; make > /dev/null 2>&1)
    if [[ $? -eq 0 ]]; then
        pathins $prefix/build/bin
        export PYTHONPATH
        ppathins $prefix/build/lib
    fi
fi
unset prefix
