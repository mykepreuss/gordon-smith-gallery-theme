#!/usr/bin/env python3
"""Tests for check_answers.py against small synthetic pages.

  python3 design-system/scripts/tests/test_check_answers.py
"""
import json
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import check_answers as check  # noqa: E402

GALLERY = {"@context": "https://schema.org", "@graph": [{
    "@type": "ArtGallery", "name": "Gordon Smith Gallery",
    "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                  "dayOfWeek": ["https://schema.org/Thursday", "https://schema.org/Friday",
                                                "https://schema.org/Saturday"],
                                  "opens": "12:00", "closes": "16:00"}}]}


def page(body, data=None, description="The gallery is open Thursday to Saturday."):
    script = f'<script type="application/ld+json">{json.dumps(data)}</script>' if data else ""
    return (f'<html><head><title>T</title><meta name="description" content="{description}">{script}</head>'
            f"<body><main>{body}</main></body></html>")


class CheckAnswers(unittest.TestCase):
    def test_evidence_found_in_the_words_a_visitor_sees(self):
        question = {"evidence": ["Thursday to Saturday", r"12 to 4 PM"], "data": ["ArtGallery"]}
        html = page("<p>Open Thursday to&nbsp;Saturday,<br>12 to 4 PM</p>", GALLERY)
        self.assertEqual(check.check_question(question, html), [])

    def test_evidence_in_a_script_does_not_count(self):
        question = {"evidence": ["by donation"]}
        html = page("<p>Welcome</p><script>var a = 'by donation'</script>", description="")
        self.assertEqual(check.check_question(question, html), ["by donation"])

    def test_the_description_counts(self):
        question = {"evidence": ["public art gallery"]}
        html = page("<p>Welcome</p>", description="A public art gallery in North Vancouver.")
        self.assertEqual(check.check_question(question, html), [])

    def test_missing_structured_data(self):
        question = {"evidence": ["Welcome"], "data": ["FAQPage"]}
        self.assertEqual(check.check_question(question, page("<p>Welcome</p>", GALLERY)),
                         ["structured data: FAQPage"])

    def test_nested_types_are_found(self):
        self.assertIn("OpeningHoursSpecification", check.data_types(page("", GALLERY)))

    def test_hours_agree(self):
        self.assertEqual(check.check_hours(page("<p>Open Thursday to Saturday</p>", GALLERY)), [])

    def test_hours_disagree(self):
        errors = check.check_hours(page("<p>Open Wednesday to Sunday</p>", GALLERY, description=""))
        self.assertEqual(errors, ["the data says Thursday to Saturday; the page doesn't"])

    def test_the_question_list_is_sound(self):
        spec = json.loads(check.QUESTIONS.read_text())
        numbers = [q["n"] for q in spec["questions"]]
        self.assertEqual(numbers, sorted(set(numbers)))
        for question in spec["questions"]:
            self.assertTrue(question["page"].startswith("/"))
            self.assertTrue(question.get("evidence"), question["n"])
            for pattern in question["evidence"]:
                re.compile(pattern)


if __name__ == "__main__":
    unittest.main()
