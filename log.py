#!/usr/bin/python2.7

import argparse
import re
import sys, os, signal

def ft_exit(sig, fr):
    exit(1)

signal.signal(signal.SIGINT, ft_exit)

levels = {
    "dev":              "33",
    "debug":            "34",
    "info":              "3",
    "notice":         "11",
    "warning":        "202",
    "err":             "52",
    "crit":            "196",
    "alert":          "1",
    "emerg":         "53"
}

replacements = {
        # r"([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}[: -][0-9]+|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})": r"\033[38;5;99m\1\033[0m",
        # r"#012": r"\n",
        r"smartserver":     r"smart",
        r"frontalRfc":      r"front",
        r"scheduler":       r"sched",
        r"API":             r"API  ",
        r"CRUD":            r"CRUD "
}

replacements2 = {
        r"([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}[: -][0-9]+|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})": r"\033[38;5;99m\1\033[0m",
        r"(\[opsise\-module\-\w+\])": r"\033[3;38;5;80m\1\033[0m",
        r"(\[library_\w+\])": r"\033[3;38;5;80m\1\033[0m",
        r"([eE][rR][rR][oO][rR])": r"\033[31m\1\033[0m",
        r"\`(\w+_?\w*)\`": r"\033[3;38;5;30m\1\033[0m",
        r"(http)":     r"\033[33m\1\033[0m",
        r"(GET)":      r"\033[33m\1\033[0m",
        r"(AS)":      r"\033[33m\1\033[0m",
        r"(POST)":     r"\033[33m\1\033[0m",
        r"(SELECT)":   r"\033[33m\1\033[0m",
        r"(READ)":     r"\033[33m\1\033[0m",
        r"(WHERE)":    r"\033[33m\1\033[0m",
        r"( IS )":    r"\033[33m\1\033[0m",
        r"( FROM )":    r"\033[33m\1\033[0m",
        r"( NOT)":    r"\033[33m\1\033[0m",
        r"( NULL )":    r"\033[33m\1\033[0m",
        r" (LEFT) ":    r" \033[33m\1\033[0m ",
        r" (AND) ":    r" \033[33m\1\033[0m ",
        r" (OR) ":    r" \033[33m\1\033[0m ",
        r"( JOIN )":    r"\033[33m\1\033[0m",
        r"( JO )":    r"\033[33m\1\033[0m",
        r"( IN )":    r"\033[33m\1\033[0m",
        r"( ON )":    r"\033[33m\1\033[0m",
        r"(LIMIT)":    r"\033[33m\1\033[0m",
        r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)": r"\033[38;5;99m\1\033[0m",
        r"(\(40\d\))": r"\033[31m\1\033[0m",
        r"(\(50\d\))": r"\033[31m\1\033[0m",
        r"(\(20\d\))": r"\033[32m\1\033[0m",
        r"(<40\d>)": r"\033[31m\1\033[0m",
        r"(<50\d>)": r"\033[31m\1\033[0m",
        r"(<20\d>)": r"\033[32m\1\033[0m",
        r"(\"\w+\"):(\"?(?:\w|-|_| )*\"?)": r"\033[38;5;85m\1\033[0m:\033[38;5;130m\2\033[0m",
        r"\\\\" : r"",
        r"\\\/\\\/" : r""
}

fd = sys.stdin
sys.stdout.write("\x1b[0m")


regex = r"\w\w\w\s*\d* (\d\d:\d\d:\d\d) \w+.(\w+) - .* - (\w+)\[(\d*)\]:\s*{\"message\":\"(.*)\",\"session_id\":\"(.*)\"}"
regex2= r"\w\w\w\s*\d* (\d\d:\d\d:\d\d) \w+.(\w+) - .* - (\w+)\[(\d*)\].*\"message\":\"(.*)\"}(?:\n|$)"
regex3= r"\w\w\w\s*\d* (\d\d:\d\d:\d\d) \w+.(\w+) - .* - (\w+)\[(\d*)\]:\s*{\"session_id\":\"(.*)\",\"message\":\"(.*)\"}"

while True:
    line = fd.readline()
    if not line: break
    line = line[0:-1]
    out = line
    str = ""
    # try:
    if out.find("session_id") != -1:
        if re.search(regex, out):
            match = re.search(regex, out)
            # print "Match at index %s, %s" % (match.start(), match.end())
            # print "Full match: %s" % (match.group(0))

            str += "%s " % (match.group(1))#date
            str +="\x1b[38;5;%sm%s\x1b[0m " % (40 + int(match.group(4))%80 * 2, replacements[match.group(3)])#name
            str += "\x1b[38;5;%sm%s\x1b[0m" % (levels[match.group(2)], match.group(2).ljust(7))#loglevel
            str +="\x1b[38;5;%dm[%s]\x1b[0m" % (40 + int(match.group(4))%80 * 2, match.group(4).ljust(6))#pid
            if match.group(6) != "":
                #str +="[\x1b[38;5;%dm%s\x1b[0m]:" % (40 + int(match.group(6), 16)%80 * 2, match.group(6))
                str += "                        "
            else:
                str += "                        "
            str += re.sub("\\\/","/", ("\x1b[0m%s\x1b[0m" % (re.sub("\\\\\"", "\"", match.group(5)))))#message
        elif re.search(regex3, out):
            match = re.search(regex3, out)

            str += "%s " % (match.group(1))#date
            str +="\x1b[38;5;%sm%s\x1b[0m " % (40 + int(match.group(4))%80 * 2, replacements[match.group(3)])#name
            str += "\x1b[38;5;%sm%s\x1b[0m" % (levels[match.group(2)], match.group(2).ljust(7))#loglevel
            str +="\x1b[38;5;%dm[%s]\x1b[0m" % (40 + int(match.group(4))%80 * 2, match.group(4).ljust(6))#pid
            if match.group(6) != "":
                #str +="[\x1b[38;5;%dm%s\x1b[0m]:" % (40 + int(match.group(5), 16)%80 * 2, match.group(5))
                str += "                        "
            else:
                str += "                        "
            str += re.sub("\\\/","/", ("\x1b[0m%s\x1b[0m" % (re.sub("\\\\\"", "\"", match.group(6)))))#message
    elif re.search(regex2, out):
        match = re.search(regex2, out)

        str += "%s " % (match.group(1))#date
        str +="\x1b[38;5;%sm%s\x1b[0m " % (40 + int(match.group(4))%80 * 2, replacements[match.group(3)])#name
        str += "\x1b[38;5;%sm%s\x1b[0m" % (levels[match.group(2)], match.group(2).ljust(7))#loglevel
        str +="\x1b[38;5;%dm[%s]\x1b[0m[            ]:" % (40 + int(match.group(4))%80 * 2, match.group(4).ljust(6))#pid
        str += re.sub("\\\/","/", ("\x1b[0m%s\x1b[0m" % (re.sub("\\\\\"", "\"", match.group(5)))))#message
    else:
        continue

    for r in replacements2:
        str = re.sub(r, replacements2[r], str)
    print str

