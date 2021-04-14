import sys, os, re
from glob import glob
import uuid
import requests

def main():
    # root folder to scan for URLs
    root_folder = sys.argv[1]
    # offline folder to store static offline files
    offline_folder = sys.argv[2]


    offline_file = os.path.join(offline_folder, "offline_{}.{}")
    offline_link = "offline/offline_{}.{}"

    mime_ptn = re.compile(r"(?P<mime>(?P<t1>[\w^\/]+)\/(?P<t2>[\S\.^\;]+))(\;|$)", re.IGNORECASE)
    #link_ptn = re.compile(r"(?P<encl>[\S\"\'])(?P<link>https?:\/\/(?P<host>[\S^:\/)]+)(?P<port>\:[0-9]+)?\/((?!(?P=encl)).)+)(?P=encl)", re.IGNORECASE)
    link_ptn = re.compile(r"[\(\'\"\ ](?P<link>https?:\/\/(?P<host>[\S^:\/)]+)(?P<port>\:[0-9]+)?\/[^\(\)\'\"\ ]+)(?P<encl_stop>[\(\)\'\"\ ])")

    # Block special hosts
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

    i = 0
    while i < len(files_to_check):
        file_i = files_to_check[i]
        try:
            print("Inspect", file_i)
            with open(file_i, "r", encoding="utf-8") as f:
                t = f.read()

            for match in link_ptn.finditer(t):
                found_link = match.group("link")
                found_host = match.group("host")

                if found_link not in valid_urls:
                    # check link
                    if True in [ True for fh in forbidden_hosts if fh.match(found_link) is not None ]:
                        # host is forbidden
                        valid_urls[found_link] = False
                    else:
                        # host is not forbidden
                        # check mime type
                        response = requests.head(found_link, allow_redirects=True)
                        mime = response.headers.get("Content-Type", None)
                        if mime is None:
                            valid_urls[found_link] = False
                        else:
                            mime_match = mime_ptn.match(mime)
                            if mime_match is None:
                                valid_urls[found_link] = False
                            else:
                                final_fext = None
                                for smt, get_fext in supported_mime_types:
                                    if smt(mime_match):
                                        final_fext = get_fext(mime_match)
                                        break
                                if final_fext is None:
                                    # mime not supported
                                    valid_urls[found_link] = False
                                else:
                                    # mime is supported -> store and remember file
                                    valid_urls[found_link] = True
                                    file_unique = uuid.uuid4()
                                    target_link = offline_link.format(file_unique, final_fext)
                                    target_file = offline_file.format(file_unique, final_fext)

                                    # download file
                                    try:
                                        file_response = requests.get(found_link, allow_redirects=True)
                                        file_response.raise_for_status()
                                        with open(target_file, 'wb') as download_file:
                                            for chunk in file_response.iter_content(100000):
                                                download_file.write(chunk)
                                        # also check downloaded file
                                        files_to_check.append(target_file)

                                        print("Downloaded file:", found_link)
                                    except:
                                        print("Link could not been downloaded:", found_link)

                                    # register downloaded file
                                    cached_urls[found_link] = {
                                        "input_link": found_link,
                                        "target_link": target_link,
                                        "file": target_file,
                                        "fext": final_fext,
                                        "found": [ file_i ]
                                    }

                if valid_urls[found_link]:
                    # add to cached urls entries
                    cached_urls[found_link]["found"].append(file_i)

            print("Checked file:", file_i)
        except:
            print("Skip file:", file_i)

        # look at next file
        i+= 1

    # replace files with offline link
    for _, cached in cached_urls.items():
        for edit_file in cached["found"]:
            with open(edit_file, "r", encoding="utf-8") as f:
                file_content = f.read()
            with open(edit_file, "w", encoding="utf-8") as f:
                f.write(file_content.replace(cached["input_link"], cached["target_link"]))
        print("Patched to", len(cached["found"]), "file with link:", cached["target_link"])

    print("Done")

if __name__ == "__main__":
    main()