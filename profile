# -*- mode: shell-script -*-
if [[ -z "$TOP" ]]; then
    _topset=1
    # keep going up until we get to the rpm directory
    export TOP=$(dirname $PWD)
    while [[ ! -d $TOP/configtools ]]; do
        TOP=$(dirname $TOP)
        if [[ "$TOP" = "/home/$USER" || "$TOP" = "/home" || "$TOP" = "/" ]]; then
            break
        fi
    done
else
    _topset=0
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
if [[ ! -f $prefix/configtools/bin/getconf.2.py ]]
then
    echo "Cannot find getconf.py"
else
    (cd $prefix/configtools; make > /dev/null 2>&1)
    if [[ $? -eq 0 ]]; then
        pathins $prefix/configtools/build/bin
        export PYTHONPATH
        ppathins $prefix/configtools/build/lib
    fi
fi
unset prefix
