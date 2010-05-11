#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "kibot-modules",
    version = "0.2.0",
    author = "Peter Teichman",
    author_email = "peter@teichman.org",
    url = "http://wiki.github.com/pteichman/kibot-modules/",
    description = "A suite of useful modules for kibot.",
    packages = find_packages(),
    install_requires = ["kibot>=0.0.13",
                        "cobe>=1.0.3"],
    namespace_packages = ["kibot", "kibot.modules"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: End Users/Desktop",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Topic :: Communications :: Chat :: Internet Relay Chat"
    ],
    entry_points = {
        "kibot.modules" : [
            "cobe = kibot.modules.cobe",
            "eightball = kibot.modules.eightball",
            "tumblr = kibot.modules.tumblr",
            "woo = kibot.modules.woo"
        ]
    }
)
