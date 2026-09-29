#!/usr/bin/env python3
"""The old Smith Foundation site's addresses (smithfoundation.co), sent to their new pages on
gordonsmithgallery.com with permanent (301) redirects. README.md says how the file is used.

redirects.csv is the record: one row per old address, edited by hand. This script turns it into the
file the old server reads (Apache, .htaccess), and checks it. Nothing here writes to the store or to
either site.

  python3 proposals/foundation-redirects/redirects.py write
      redirects.csv into smithfoundation.co.htaccess.
  python3 proposals/foundation-redirects/redirects.py test
      Starts Apache on this computer with the file, asks for every old address in the forms people
      and search engines use, and checks where each is sent. Needs httpd and curl (both on a Mac).
  python3 proposals/foundation-redirects/redirects.py targets <address> [--theme <id>]
      Checks that every new page answers. Before release: the store's address with the review
      theme's ID. On the day: https://gordonsmithgallery.com.
  python3 proposals/foundation-redirects/redirects.py live [--ip <server>]
      After the upload: asks the real smithfoundation.co for every old address. --ip asks one
      server directly, whatever the domain's DNS says.

A row's old address covers itself, with or without its last slash, and anything under it
(/attachment/..., /embed/, /feed/) that has no row of its own. An old address that ends in a file
name covers that file only. Anything with no row goes to the new home page, the media library's
pictures included (P-63).
"""
import argparse
import csv
import http.cookiejar
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROWS = HERE / "redirects.csv"
OUT = HERE / "smithfoundation.co.htaccess"
OLD_HOST = "smithfoundation.co"
NEW_SITE = "https://gordonsmithgallery.com"
PORT = 8377


# WordPress's own rules, as they are in the old server's .htaccess. Only the test uses them.
WORDPRESS = """
# BEGIN WordPress
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
RewriteRule ^index\\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>
# END WordPress
"""


def rows():
    found = list(csv.DictReader(ROWS.open(newline="")))
    olds = [r["old"] for r in found]
    problems = [f"twice: {o}" for o in set(olds) if olds.count(o) > 1]
    problems += [f"{r['old']}: both addresses start with /" for r in found
                 if not (r["old"].startswith("/") and r["new"].startswith("/"))]
    problems += [f"{r['old']}: the new address has no last slash, query or space" for r in found
                 if r["new"] != "/" and (r["new"].endswith("/") or re.search(r"[?#\s]", r["new"]))]
    if problems:
        sys.exit("redirects.csv:\n  " + "\n  ".join(problems))
    return found


def is_file(old):
    return not old.endswith("/")


def pattern(old):
    """The old address as Apache matches it in .htaccess: no first slash."""
    if old == "/":
        return r"^(index\.php)?$"
    path = re.sub(r"([.+*?()\[\]{}|^$\\])", r"\\\1", old.strip("/"))
    return f"^{path}$" if is_file(old) else f"^{path}(/.*)?$"


def rule(old, new):
    # The last "?" drops the old address's query (?portfolioCats=60, ?utm_source=...).
    return f"RewriteRule {pattern(old)} {NEW_SITE}{new}? [R=301,NC,L]"


def build():
    found = rows()
    pages = sorted((r for r in found if not is_file(r["old"]) and r["old"] != "/"),
                   key=lambda r: (-r["old"].count("/"), r["old"]))  # the deepest first
    files = sorted((r for r in found if is_file(r["old"])), key=lambda r: r["old"])
    by_id = {}
    for r in found:
        if r["wp_id"]:
            by_id.setdefault(r["new"], []).append(r["wp_id"])
    host = OLD_HOST.replace(".", r"\.")
    out = f"""# {OLD_HOST}: every old address goes to its new page on gordonsmithgallery.com.
#
# Made by proposals/foundation-redirects/redirects.py from redirects.csv. Change the list and
# make the file again. Don't edit this file by hand.
#
# Where it goes: the top of the .htaccess file in the website's main folder on the old server
# (public_html, beside wp-config.php), above everything already in that file. What is there
# stays: the host's PHP settings are kept in it. Keep a copy of the file first.
# {len(found)} old addresses are listed. Anything else goes to the new home page.

<IfModule mod_rewrite.c>
RewriteEngine On

# 1. Only {OLD_HOST}. Any other site in this hosting account is left alone.
RewriteCond %{{HTTP_HOST}} !^(www\\.)?{host}(:[0-9]+)?$ [NC]
RewriteRule ^ - [L]

# 2. Left alone: the checks that renew the security certificate, and robots.txt (none means
# search engines may read every address, which is how they find the redirects).
RewriteRule ^\\.well-known/ - [L]
RewriteRule ^robots\\.txt$ - [L]

# 3. WordPress's sign-in and admin keep working, so staff can still get at the old site.
# Delete these three lines when WordPress is removed, or sooner if nobody needs to sign in.
RewriteRule ^(wp-admin|wp-includes)(/|$) - [L]
RewriteRule ^wp-content/(plugins|themes)/ - [L]
RewriteRule ^wp-(login|cron)\\.php$ - [L]

# 4. WordPress's numbered addresses (/?p=126, /?page_id=9).
"""
    for new in sorted(by_id):
        ids = "|".join(sorted(by_id[new], key=int))
        out += f"RewriteCond %{{QUERY_STRING}} (^|&)(p|page_id)=({ids})(&|$)\n"
        out += f"RewriteRule ^(index\\.php)?$ {NEW_SITE}{new}? [R=301,L]\n"
    out += "\n# 5. Pages, exhibitions and events. Each rule covers the address and anything under it.\n"
    out += "\n".join(rule(r["old"], r["new"]) for r in pages) + "\n"
    out += "\n# 6. Documents, each to the page that holds it or what replaced it. And the sitemap.\n"
    out += "\n".join(rule(r["old"], r["new"]) for r in files) + "\n"
    out += f"""
# 7. Everything else: the old home page, and the media library's pictures and other files,
# whether or not they are still on the server (P-63).
RewriteRule ^ {NEW_SITE}/? [R=301,L]
</IfModule>
"""
    return out


# ---------------------------------------------------------------------------
# Checks

def expected():
    """(what to ask for, where it must be sent), for every row in the forms that are in use."""
    cases = []
    for r in rows():
        old, new = r["old"], NEW_SITE + r["new"]
        cases.append((old, new))
        if is_file(old):
            continue
        if old != "/":
            cases += [(old.rstrip("/"), new), (old.upper(), new), (old + "attachment/a-photo/", new),
                      (old + "embed/", new)]
        cases.append((old + "?portfolioCats=59%2C60%2C58", new))
        if r["wp_id"]:
            cases += [(f"/?p={r['wp_id']}", new), (f"/?page_id={r['wp_id']}", new),
                      (f"/index.php?p={r['wp_id']}&preview=true", new)]
    home = NEW_SITE + "/"
    cases += [(p, home) for p in ("/no-such-page/", "/feed/", "/author/admin/", "/slide/volunteer/",
                                  "/?p=999999", "/?utm_source=north%20shore%20news", "/index.php",
                                  "/xmlrpc.php", "/wp-json/wp/v2/pages",
                                  "/wp-content/uploads/2017/07/Facebook-icon.jpg",  # still on the server
                                  "/wp-content/uploads/2017/07/gone.jpg", "/wp-content/uploads/")]
    return cases


def ask(url, host=None, resolve=None):
    """(status, where it sends you) for one address, without following the redirect."""
    cmd = ["curl", "-sS", "-m", "30", "-o", "/dev/null", "-w", "%{http_code} %{redirect_url}",
           "-A", "Mozilla/5.0 (foundation-redirects check)"]
    if host:
        cmd += ["-H", f"Host: {host}"]
    if resolve:
        cmd += ["--resolve", resolve]
    got = subprocess.run(cmd + [url], capture_output=True, text=True)
    if got.returncode:
        return 0, got.stderr.strip()
    status, _, where = got.stdout.partition(" ")
    return int(status), where


def report(failures, count, what):
    for line in failures:
        print("  FAIL", line)
    print(f"{count - len(failures)} of {count} {what}")
    return 1 if failures else 0


def test():
    if OUT.read_text() != build():
        sys.exit(f"{OUT.name} is behind redirects.csv. Run: redirects.py write")
    httpd = shutil.which("httpd") or shutil.which("apache2")
    if not (httpd and shutil.which("curl")):
        sys.exit("This check needs httpd (Apache) and curl.")
    modules = next(p for p in (pathlib.Path("/usr/libexec/apache2"), pathlib.Path("/usr/lib/apache2/modules"),
                               pathlib.Path("/usr/lib64/httpd/modules")) if p.exists())
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        root = tmp / "public_html"
        # What is on the old server: a picture and a document in the media library, WordPress.
        for kept in ("wp-content/uploads/2017/07/Facebook-icon.jpg", "wp-login.php", "index.php",
                     "wp-content/uploads/2023/07/EndlessSummer_ExhibitionBooklet.pdf",
                     "wp-admin/index.php", "wp-content/themes/Avada/style.css", "other-site/index.html"):
            (root / kept).parent.mkdir(parents=True, exist_ok=True)
            (root / kept).write_text("kept")
        # As on the server: the file's rules first, then what WordPress keeps in .htaccess.
        (root / ".htaccess").write_text(OUT.read_text() + WORDPRESS)
        load = "\n".join(f"LoadModule {name}_module {modules}/mod_{name}.so"
                         for name in ("mpm_prefork", "authz_core", "unixd", "dir", "rewrite"))
        (tmp / "httpd.conf").write_text(f"""{load}
ServerName localhost
Listen 127.0.0.1:{PORT}
PidFile {tmp}/httpd.pid
ErrorLog {tmp}/error.log
DocumentRoot "{root}"
DirectoryIndex index.php index.html
<Directory "{root}">
  AllowOverride All
  Require all granted
  Options FollowSymLinks
</Directory>
""")
        server = subprocess.Popen([httpd, "-X", "-f", str(tmp / "httpd.conf")],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        try:
            base = f"http://127.0.0.1:{PORT}"
            for _ in range(50):
                if ask(base + "/robots.txt", OLD_HOST)[0]:
                    break
                if server.poll() is not None:
                    sys.exit("Apache didn't start:\n" + server.stdout.read() + (tmp / "error.log").read_text())
                time.sleep(0.1)
            failures, cases = [], expected()
            for path, new in cases:
                for host in (OLD_HOST, "www." + OLD_HOST):
                    got = ask(base + path, host)
                    if got != (301, new):
                        failures.append(f"{host}{path}: {got[0]} {got[1]}, not 301 {new}")
            kept = [("/wp-login.php", OLD_HOST, 200), ("/wp-admin/", OLD_HOST, 200),
                    ("/wp-content/themes/Avada/style.css", OLD_HOST, 200),
                    ("/robots.txt", OLD_HOST, 404), ("/.well-known/acme-challenge/abc", OLD_HOST, 404),
                    ("/other-site/", "another-site.example", 200),  # another site in the account
                    ("/about/", "another-site.example", 404)]
            for path, host, status in kept:
                got = ask(base + path, host)
                if got[0] != status or got[1]:
                    failures.append(f"{host}{path}: {got[0]} {got[1]}, not {status} with no redirect")
            return report(failures, 2 * len(cases) + len(kept), "requests answered as they should")
        finally:
            server.terminate()
            server.wait()


def targets(address, theme):
    """Every new page answers 200 at this address. With --theme, as that unpublished theme shows it."""
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (foundation-redirects check)")]
    address = address.rstrip("/")
    if theme:
        opener.open(f"{address}/?preview_theme_id={theme}", timeout=60).read()
    news, failures = sorted({r["new"] for r in rows()}), []
    for new in news:
        try:
            with opener.open(address + new, timeout=60) as got:
                status, landed = got.status, got.geturl()
        except urllib.error.HTTPError as error:
            status, landed = error.code, error.geturl()
        path = re.sub(r"^https?://[^/]+", "", landed).split("?")[0] or "/"
        if status != 200 or path != new:
            olds = [r["old"] for r in rows() if r["new"] == new]
            failures.append(f"{new}: {status} at {path} (from {', '.join(olds[:3])}{' ...' if len(olds) > 3 else ''})")
        time.sleep(0.3)
    return report(failures, len(news), f"new pages answer at {address}")


def live(ip):
    failures, cases = [], [(r["old"], NEW_SITE + r["new"]) for r in rows()] + [("/no-such-page/", NEW_SITE + "/")]
    for path, new in cases:
        got = ask(f"https://{OLD_HOST}{path}", resolve=f"{OLD_HOST}:443:{ip}" if ip else None)
        if got != (301, new):
            failures.append(f"{path}: {got[0]} {got[1]}, not 301 {new}")
        time.sleep(0.2)
    return report(failures, len(cases), f"old addresses redirect at {OLD_HOST}" + (f" ({ip})" if ip else ""))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    steps = parser.add_subparsers(dest="step", required=True)
    steps.add_parser("write")
    steps.add_parser("test")
    step = steps.add_parser("targets")
    step.add_argument("address")
    step.add_argument("--theme")
    steps.add_parser("live").add_argument("--ip")
    args = parser.parse_args(argv)
    if args.step == "write":
        OUT.write_text(build())
        print(f"{OUT.relative_to(HERE.parent.parent)}: {len(rows())} old addresses")
        return 0
    if args.step == "test":
        return test()
    if args.step == "targets":
        return targets(args.address, args.theme)
    return live(args.ip)


if __name__ == "__main__":
    sys.exit(main())
