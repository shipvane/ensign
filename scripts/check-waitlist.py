#!/usr/bin/env python3
"""Smoke-check the waitlist form: the site's only conversion path.

The form posts to Formspree, and Formspree only accepts the submission when the
Cloudflare Turnstile token verifies against the secret key held in its dashboard.
That makes the signup path quietly fragile: a wrong site key, a dropped script
tag or a mangled form action all leave a page that looks perfect and silently
accepts nobody. Nothing about it fails loudly, and the funnel is one page deep.

Run against the source file as a pre-merge gate, or against the deployed URL to
confirm what visitors are actually served:

    python3 scripts/check-waitlist.py --file site/index.html
    python3 scripts/check-waitlist.py --url https://shipvane.com/

Stdlib only, by design: the site has no toolchain and this check should not be
the thing that gives it one.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser

FORMSPREE_ACTION = re.compile(r"^https://formspree\.io/f/[A-Za-z0-9]+$")
TURNSTILE_SCRIPT = "challenges.cloudflare.com/turnstile/v0/api.js"

# Cloudflare's documented dummy site keys, e.g. 1x00000000000000000000AA. They
# always pass (or always block) and mint tokens no real secret key can verify,
# so one reaching production means a silently dead form.
TEST_SITEKEY = re.compile(r"^[123]x0{20}[A-Z]{2}$")


class WaitlistParser(HTMLParser):
    """Pull out just the bits of the waitlist form the signup path depends on."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.form_attrs: dict[str, str] | None = None
        self.turnstile_attrs: dict[str, str] | None = None
        self.email_input = False
        self.turnstile_script = False
        self._depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}

        if tag == "script" and TURNSTILE_SCRIPT in a.get("src", ""):
            self.turnstile_script = True

        if tag == "form" and a.get("id") == "waitlist-form":
            self.form_attrs = a
            self._depth = 1
            return

        if not self._depth:
            return

        # Turnstile injects its hidden token input into the enclosing form, which
        # is what makes `new FormData(form)` carry the token. Nesting matters.
        if tag == "div" and "cf-turnstile" in a.get("class", "").split():
            self.turnstile_attrs = a
        if tag == "input" and a.get("type") == "email" and a.get("name") == "email":
            self.email_input = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "form" and self._depth:
            self._depth = 0


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "shipvane-waitlist-check"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status != 200:
            raise OSError("HTTP %s" % resp.status)
        return resp.read().decode("utf-8", "replace")


def load(args: argparse.Namespace) -> tuple[str, str]:
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            return fh.read(), args.file

    # Pages' CDN can lag a few seconds behind a deploy, and a scheduled monitor
    # should not page anyone over one dropped connection.
    last = ""
    for attempt in range(1, args.retries + 1):
        try:
            return fetch(args.url), args.url
        except urllib.error.HTTPError as e:
            last = "HTTP %s" % e.code
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = str(e)
        if attempt < args.retries:
            print("      fetch attempt %d/%d failed (%s), retrying in %ds…"
                  % (attempt, args.retries, last, args.retry_delay))
            time.sleep(args.retry_delay)

    # Being unable to reach the site is a different failure from the form being
    # broken; say so, rather than implying the waitlist is misconfigured.
    raise SystemExit(
        "ERROR could not fetch %s after %d attempt(s): %s"
        % (args.url, args.retries, last)
    )


def check(html: str) -> list[str]:
    """Return a list of failure messages; empty means healthy."""
    p = WaitlistParser()
    p.feed(html)
    bad: list[str] = []

    if p.form_attrs is None:
        # Everything else is scoped to the form, so there is nothing left to say.
        return ['no <form id="waitlist-form"> on the page']

    action = p.form_attrs.get("action", "")
    if not FORMSPREE_ACTION.match(action):
        bad.append("form action is not a Formspree endpoint: %r" % action)

    if not p.email_input:
        bad.append('no <input type="email" name="email"> inside the form')

    if not p.turnstile_script:
        bad.append("the Turnstile api.js script tag is missing")

    if p.turnstile_attrs is None:
        bad.append("no .cf-turnstile widget inside the form")
    else:
        key = p.turnstile_attrs.get("data-sitekey", "")
        if not key:
            bad.append("the .cf-turnstile widget has no data-sitekey")
        elif TEST_SITEKEY.match(key):
            bad.append(
                "data-sitekey %s is a Cloudflare TEST key — Formspree will reject "
                "every submission against the real secret key" % key
            )
        elif not key.startswith("0x"):
            bad.append("data-sitekey %r is not a real Turnstile key (expected 0x…)" % key)

    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="path to the HTML file to check")
    src.add_argument("--url", help="deployed URL to fetch and check")
    ap.add_argument("--retries", type=int, default=3,
                    help="fetch attempts before giving up (--url only, default 3)")
    ap.add_argument("--retry-delay", type=int, default=10,
                    help="seconds between fetch attempts (default 10)")
    args = ap.parse_args()

    html, origin = load(args)
    failures = check(html)

    if failures:
        print("FAIL  waitlist smoke check — %s" % origin)
        for f in failures:
            print("  - %s" % f)
        print("\nThe signup form is the site's only conversion path; treat this as broken.")
        return 1

    print("OK    waitlist smoke check — %s" % origin)
    print("      form posts to Formspree, email field present,")
    print("      Turnstile script loaded and a real site key is wired in.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
