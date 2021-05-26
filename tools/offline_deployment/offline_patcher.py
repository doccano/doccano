#!/usr/bin/env python3
import sys, os, re
import uuid
from urllib.parse import urljoin
import requests

"""Script Information

This script scans all files of a given directory [1] for URL addresses and
hyperlink references.
All found URLs are requested for Content-Type.
For certain Content-Types (like js, css, or fonts), the file is downloaded and
stored locally into a given directory [2] and the existing URLs are altered
to a local URL location (with a given URL prefix [3]).

Downloaded files are scanned for URLs recursively.
Relative references in CSS files are an edge case that is
handled separately by a specific regex pattern.

Arguments:
 1. <root directory [1]>
 2. <local offline storage directory [2]>
 3. <HTTP URL location prefix [3]>

Example:
 - Given:
   - File ./webspace/index.html, containing URL: https://example.com/library.js
   - Directory ./webspace/static, containing static files,
       serving content on HTTP location: /staticfiles

 - Call:
   $> python3 offline_patcher.py webspace/ webspace/static /staticfiles

 - Result:
   - Library from https://example.com/library.js is stored as file:
       webspace/static/offline_<uuid>.js
   - Link in file webspace/index.html is replaced to:
       /staticfiles/offline_<uuid>.js
   - File webspace/static/offline_<uuid>.js is scanned recursively for URLs

Author: Johann Frei
"""


def main():
    # root folder to scan for URLs
    root_folder = sys.argv[1]
    # offline folder to store static offline files
    offline_folder = sys.argv[2]
    # offline link prefix
    offline_prefix = sys.argv[3]

    offline_file = os.path.join(offline_folder, "offline_{}.{}")
    offline_link = offline_prefix + "/offline_{}.{}"

    mime_ptn = re.compile(r"(?P<mime>(?P<t1>[\w^\/]+)\/(?P<t2>[\S\.^\;]+))(\;|$)", re.IGNORECASE)

    # regex to find matches like: "https://<host>[:<port>]/a/link/location.html"
    link_ptn = re.compile(r"[\(\'\"\ ](?P<link>https?:\/\/(?P<host>(?P<h_host>((?=[^\(\)\'\"\ \:\/])(?=[\S]).)+))(?P<port>\:[0-9]+)?\/[^\(\)\'\"\ ]+)(?P<encl_stop>[\(\)\'\"\ ])")
    # regex to find matches like: url(../relative/parent_directory/links/without/quotes/are/hard)
    link_ptn_url = re.compile(r"url\([\"\']?(?P<link>((?=[^\)\"\'])(?=[\S]).)+)[\"\']?\)")

    # block special hosts
    forbidden_hosts = [
        re.compile(r"^.*registry\.npmjs\.org$"), # No yarnpkg repository
        re.compile(r"^.*yarnpkg\.com$"), # No yarnpkg repository
        re.compile(r"^[0-9\.]+$"), # avoid IP addresses
        re.compile(r"^[^\.]+$"), # needs a dot in host
    ]

    # only support certain content types
    supported_mime_types = [
        # (filter function -> bool, file extension -> str)
        (lambda m: m["t2"] == "javascript", lambda m: "js"),
        (lambda m: m["t2"] == "css", lambda m: "css"),
        (lambda m: m["t1"] == "font", lambda m: m["t2"]),
    ]


    # load all initial files
    files_to_check = []
    for cur_dir, n_dir, n_files in os.walk(root_folder):
        files_to_check += [ os.path.join(cur_dir, f) for f in n_files ]

    cached_urls = {}
    valid_urls = {}
    file_origins = {}

    i = 0
    while i < len(files_to_check):
        file_i = files_to_check[i]
        try:
            print("Inspect", file_i)
            with open(file_i, "r", encoding="utf-8") as f:
                t = f.read()

            link_findings_default = [ {
                "abs": match.group("link"),
                "found": match.group("link"),
                "host": match.group("host")
             } for match in link_ptn.finditer(t) ]

            # extract relative urls and convert them to absolute http urls
            link_findings_url_prefix = []
            for match in link_ptn_url.finditer(t):
                if os.path.abspath(file_i) in file_origins and not match.group("link").startswith("http"):
                    link_abs = urljoin(file_origins[os.path.abspath(file_i)], match.group("link"))
                    item = {
                        "abs": link_abs,
                        "found": match.group("link"),
                        "host": link_ptn.match( "\"" + link_abs + "\"").group("host")
                    }
                    link_findings_url_prefix.append(item)

            for spot in link_findings_default + link_findings_url_prefix:
                absolute_link = spot["abs"]
                found_link = spot["found"]

                if absolute_link not in valid_urls:
                    # check link
                    if True in [ True for fh in forbidden_hosts if fh.match(absolute_link) is not None ]:
                        # host is forbidden
                        valid_urls[absolute_link] = False
                    else:
                        # host is not forbidden
                        # check mime type
                        response = requests.head(absolute_link, allow_redirects=True)
                        mime = response.headers.get("Content-Type", None)
                        if mime is None:
                            valid_urls[absolute_link] = False
                        else:
                            mime_match = mime_ptn.match(mime)
                            if mime_match is None:
                                valid_urls[absolute_link] = False
                            else:
                                final_fext = None
                                # try supported content types
                                for smt, get_fext in supported_mime_types:
                                    if smt(mime_match):
                                        final_fext = get_fext(mime_match)
                                        break
                                if final_fext is None:
                                    # mime not supported
                                    valid_urls[absolute_link] = False
                                else:
                                    # mime is supported -> store and remember file
                                    valid_urls[absolute_link] = True
                                    file_unique = uuid.uuid4()
                                    target_link = offline_link.format(file_unique, final_fext)
                                    target_file = offline_file.format(file_unique, final_fext)

                                    # download file
                                    try:
                                        file_response = requests.get(absolute_link, allow_redirects=True)
                                        file_response.raise_for_status()
                                        with open(target_file, 'wb') as download_file:
                                            for chunk in file_response.iter_content(100000):
                                                download_file.write(chunk)
                                        # also check downloaded file for links later
                                        files_to_check.append(target_file)

                                        print("Downloaded file:", absolute_link)
                                    except:
                                        print("Link could not been downloaded:", absolute_link)

                                    # register downloaded file
                                    cached_urls[absolute_link] = {
                                        "input_link": absolute_link,
                                        "target_link": target_link,
                                        "file": target_file,
                                        "fext": final_fext,
                                        "found": [ {"file": file_i, "found_link": found_link} ]
                                    }
                                    # store reverse lookup for recursive url("../rel/link") patterns
                                    file_origins[os.path.abspath(target_file)] = absolute_link

                if valid_urls[absolute_link]:
                    # add to cached urls entries
                    cached_urls[absolute_link]["found"].append({"file": file_i, "found_link": found_link})

            print("Checked file:", file_i)
        except UnicodeDecodeError:
            print("Skip file (No unicode):", file_i)
        except:
            print("Unknown error... Skip file:", file_i)

        # look at next file
        i+= 1

    # replace files with offline link
    for _, cached in cached_urls.items():
        for edit_file in cached["found"]:
            with open(edit_file["file"], "r", encoding="utf-8") as f:
                file_content = f.read()
            with open(edit_file["file"], "w", encoding="utf-8") as f:
                f.write(file_content.replace(edit_file["found_link"], cached["target_link"]))
        print("Patched to", len(cached["found"]), "file with link:", cached["target_link"])

    print("Done")

if __name__ == "__main__":
    main()
