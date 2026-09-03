#!/usr/bin/env python3
"""Tests for the waitlist smoke check.

The point of these is that the checker FAILS when it should. A smoke check that
only ever passes is worse than none — it reports health it never verified.

    python3 -m unittest discover -s scripts -p 'test_*.py'
"""

from __future__ import annotations

import unittest

import importlib.util
from pathlib import Path

# The script is hyphenated (it is a CLI, not a module), so it needs loading by
# path rather than a plain import.
_mod_path = Path(__file__).resolve().parent / "check-waitlist.py"
_spec = importlib.util.spec_from_file_location("check_waitlist", _mod_path)
check_waitlist = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_waitlist)
check = check_waitlist.check


HEALTHY = """
<!doctype html><html><head>
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
</head><body>
  <form id="waitlist-form" action="https://formspree.io/f/mbdvrvke" method="POST">
    <input type="email" name="email" required />
    <button type="submit">Join the waitlist</button>
    <div class="cf-turnstile" data-sitekey="0x4AAAAAAElVOZSIfpUwMhx9" data-theme="light"></div>
  </form>
</body></html>
"""


class TestHealthy(unittest.TestCase):
    def test_healthy_page_passes(self):
        self.assertEqual(check(HEALTHY), [])


class TestCatchesBreakage(unittest.TestCase):
    """Each case is a real way this page can silently stop accepting signups."""

    def assert_fails_with(self, html: str, needle: str):
        failures = check(html)
        self.assertTrue(failures, "expected a failure, got a clean pass")
        joined = " ".join(failures).lower()
        self.assertIn(needle.lower(), joined)

    def test_cloudflare_test_sitekey_is_rejected(self):
        # The exact regression this check exists for: the placeholder shipping.
        for key in (
            "1x00000000000000000000AA",
            "2x00000000000000000000AB",
            "3x00000000000000000000FF",
        ):
            with self.subTest(key=key):
                self.assert_fails_with(
                    HEALTHY.replace("0x4AAAAAAElVOZSIfpUwMhx9", key), "test key"
                )

    def test_missing_sitekey(self):
        self.assert_fails_with(
            HEALTHY.replace(' data-sitekey="0x4AAAAAAElVOZSIfpUwMhx9"', ""),
            "no data-sitekey",
        )

    def test_missing_turnstile_script(self):
        self.assert_fails_with(
            HEALTHY.replace("https://challenges.cloudflare.com/turnstile/v0/api.js", ""),
            "api.js script tag is missing",
        )

    def test_missing_widget(self):
        self.assert_fails_with(
            HEALTHY.replace('class="cf-turnstile"', 'class="something-else"'),
            "no .cf-turnstile widget",
        )

    def test_widget_outside_the_form_is_not_counted(self):
        # Turnstile injects its token input into the enclosing form. A widget
        # sitting outside it renders fine and submits nothing.
        html = HEALTHY.replace(
            '<div class="cf-turnstile" data-sitekey="0x4AAAAAAElVOZSIfpUwMhx9" data-theme="light"></div>',
            "",
        ).replace(
            "</form>",
            '</form><div class="cf-turnstile" data-sitekey="0x4AAAAAAElVOZSIfpUwMhx9"></div>',
        )
        self.assert_fails_with(html, "no .cf-turnstile widget")

    def test_broken_form_action(self):
        self.assert_fails_with(
            HEALTHY.replace("https://formspree.io/f/mbdvrvke", "/submit"),
            "not a formspree endpoint",
        )

    def test_missing_email_input(self):
        self.assert_fails_with(
            HEALTHY.replace('<input type="email" name="email" required />', ""),
            "no <input",
        )

    def test_missing_form_entirely(self):
        self.assert_fails_with("<html><body>nothing here</body></html>", "no <form")

    def test_renamed_form_id_is_caught(self):
        # app.js looks the form up by id; renaming it breaks submission silently.
        self.assert_fails_with(
            HEALTHY.replace('id="waitlist-form"', 'id="signup-form"'), "no <form"
        )


if __name__ == "__main__":
    unittest.main()
