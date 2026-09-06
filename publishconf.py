"""Production settings — GitHub Pages project site."""
import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *  # noqa: F401,F403

# A project site lives under the repo name, not at the domain root.
SITEURL = "https://ncarsner.github.io/nac-portfolio"
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = True
