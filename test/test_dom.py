import unittest
import md.dom
import io


class TestParagraphElement(unittest.TestCase):
    def test_parse(self):
        subject = md.dom.ParagraphElement.parse(["Test text"])[0]
        self.assertEqual(subject.values, [md.dom.Text(["Test text"])])

    def test_parse_newline_1(self):
        subject = md.dom.ParagraphElement.parse(["Test text\nLine 2"])[0]
        self.assertEqual(subject.values, [md.dom.Text(["Test text\nLine 2"])])

    def test_parse_newline_2(self):
        subjects = md.dom.ParagraphElement.parse(["Test text\n\nLine 2"])
        self.assertEqual(len(subjects), 2)
        self.assertEqual(subjects[0].values, [md.dom.Text(["Test text"])])
        self.assertEqual(subjects[1].values, [md.dom.Text(["Line 2"])])

