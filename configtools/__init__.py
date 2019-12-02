""" Configtools """
from __future__ import print_function

import os, sys

# python3
from configparser import ConfigParser

from optparse import OptionParser

import logging

def uniq(l):
    # uniquify the list without scrambling it
    seen = set()
    seen_add = seen.add
    return [x for x in l if x not in seen and not seen_add(x)]

def file_list(root):
    # read the root file, get its [config] section
    # and use it to construct the file list.
    conf = ConfigParser()
    conf.read(root)
    try:
        dirlist = conf.get("config", "path").replace(' ', '').split(',')
    except:
        dirlist = []
    try:
        files = conf.get("config", "files").replace(' ', '').split(',')
    except:
        files = []

    root = os.path.abspath(root)
    # all relative pathnames will be relative to the rootdir
    rootdir = os.path.dirname(root)
    flist = [root]
    dirlist = [os.path.abspath("%s/%s" % (rootdir, x)) if not os.path.isabs(x) else os.path.abspath(x) for x in dirlist]
    # insert the directory of the root file at the beginning
    dirlist.insert(0, rootdir)

    # import pdb; pdb.set_trace()
    for d in dirlist:
        for f in files:
            fnm = "%s/%s" % (d, f)
            if fnm in flist:
                continue
            if os.access(fnm, os.F_OK):
                fnmlist = file_list(fnm)
                flist += fnmlist
    return uniq(flist)

def init(opts):
    """init"""
    # config file
    conf = ConfigParser()
    if opts.filename:
        conf_file = opts.filename
    elif 'CONFIG' in os.environ:
        conf_file= os.environ['CONFIG']
    else:
        return (None, [])

    conffiles = file_list(conf_file)
    conffiles.reverse()
    files = conf.read(conffiles)

    return (conf, files)

def parse_args(options=[], usage=None):
    """parse_args"""
    if usage:
        parser = OptionParser(usage=usage)
    else:
        parser = OptionParser()
    # standard options
    parser.add_option("-C", "--config", dest="filename",
                  help="config FILE", metavar="FILE")
    parser.add_option("-D", "--debug", action="store_true", dest="debug",
                      help="commands logged but not executed")
    # specific options
    for o in options:
        parser.add_option(o)

    return parser.parse_args()

def parse_range(s):
    """s is of the form <prefix>[<range>]<suffix>.
       Parse and return the three components separately.
    """
    pos = s.find('[')
    rpos = s.find(']')
    if pos >= 0:
        prefix = s[0:pos]
        if rpos >= 0:
            rng = s[pos+1:rpos]
            suffix = s[rpos+1:]
        else:
            prefix = s
            rng = suffix = ""
    else:
        prefix = s
        rng = suffix = ""

    return (prefix, suffix, rng)

def expand_range(s):
    """Expand a range `foo[N-M]bar' or 'foo[1, 2, 3]bar' or 'foo[a, b, c]bar'
       into a list - no multiple ranges or nesting allowed.
       Always return a list, maybe a singleton if no expansion is necessary.
    """
    prefix, suffix, rng = parse_range(s)
    if not rng:
        return ["%s%s" % (prefix, suffix)]

    try:
        nfields = [x for x in rng.split('-')]
        if len(nfields) == 2:
            # expand the range
            try:
                l = map(str, range(int(nfields[0]), int(nfields[1])+1))
            except:
                l = map(chr, range(ord(nfields[0]), ord(nfields[1])+1))
            return ["%s%s%s" % (prefix, x, suffix) for x in l]
        elif len(nfields) == 1:
            # split it on ,
            l = map(str.strip, rng.split(','))
            return ["%s%s%s" % (prefix, x, suffix) for x in l]
    except:
        return [s]

def get_list(s):
    """get_list"""
    if not s:
        return []
    l = [x.strip().strip('\\\n') for x in s.split(',')]
    try:
        nl = []
        for x in l:
            nl += expand_range(x)
        return nl
    except:
        return l

def get(conf, option, sections):
    """get option from section list"""
    for s in sections:
        try:
            return conf.get(s, option)
        except:
            pass
    return None

def get_debug(conf, section="DEFAULT", opts=None):
    if opts and opts.debug:
        return True
    try:
        return int(conf.get(section, "debug")) > 0
    except:
        return False

def print_list(l, sep):
    print(sep.join([str(x) for x in l]))

def get_host_classes(conf):
    hostclasses = conf.options("hosts")
    # remove DEFAULT options
    for h in hostclasses:
        if conf.has_option(None, h):
            hostclasses.remove(h)
    return hostclasses

def log(cmd):
    logging.debug("%s: %s" % (hostname, cmd))
    logflush()

def logflush():
    logging.getLogger().handlers[0].flush()

def do_cmd(cmd, dbg=False):
    status = 0
    log(cmd)
    if not dbg:
        status = os.system(cmd)
    return os.WEXITSTATUS(status)

def do_cmd_with_stdout(cmd, dbg=False):
    import subprocess

    log(cmd)
    if not dbg:
        p = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        p.wait()
        return p.stdout.read()
    else:
        return ""
