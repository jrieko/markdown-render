import unittest
import md.dom
import io

class TestHeadingElement(unittest.TestCase):
    def test_parse_1(self):
        subject = md.dom.HeadingElement.parse(["# Test"])[0]
        self.assertEqual(subject.level, 1)
        self.assertEqual(subject.values, [md.dom.Text(["Test"])])

    def test_parse_2(self):
        subject = md.dom.HeadingElement.parse(["## Test"])[0]
        self.assertEqual(subject.level, 2)
        self.assertEqual(subject.values, [md.dom.Text(["Test"])])

    def test_parse_3(self):
        subject = md.dom.HeadingElement.parse(["### Test"])[0]
        self.assertEqual(subject.level, 3)
        self.assertEqual(subject.values, [md.dom.Text(["Test"])])

    def test_parse_4(self):
        subject = md.dom.HeadingElement.parse(["#### Test"])[0]
        self.assertEqual(subject.level, 4)
        self.assertEqual(subject.values, [md.dom.Text(["Test"])])

    def test_parse_5(self):
        subject = md.dom.HeadingElement.parse(["##### Test"])[0]
        self.assertEqual(subject.level, 5)
        self.assertEqual(subject.values, [md.dom.Text(["Test"])])

    def test_parse_6(self):
        subject = md.dom.HeadingElement.parse(["###### Test"])[0]
        self.assertEqual(subject.level, 6)
        self.assertEqual(subject.values, [md.dom.Text(["Test"])])

    def test_parse_7(self):
        """test compliance with HTML spec max heading level of 6"""

        subject = md.dom.HeadingElement.parse(["####### Test"])[0]
        self.assertEqual(subject.level, 6)
        self.assertEqual(subject.values, [md.dom.Text(["# Test"])])

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

class TestLink(unittest.TestCase):
    def test_parse_empty(self):
        input = ["[]()"]
        output = md.dom.Link.parse(input.copy())
        self.assertEqual(output, input)

    def test_parse(self):
        subject = md.dom.Link.parse(["[text](target)"])[0]
        self.assertEqual(subject.text, "text")
        self.assertEqual(subject.target, "target")

class TestDOM(unittest.TestCase):
    def test_parse_empty(self):
        subject = md.dom.DOM()
        subject.parse("")
        self.assertEqual(len(subject.content),0)

    def test_parse(self):
        input = [ 
            "# Test",
            "", 
            "## Test2"]
        subject = md.dom.DOM()
        subject.parse("\n".join(input))
        self.assertEqual(len(subject.content), 2)
        self.assertEqual(subject.content, md.dom.ParagraphElement.parse(input))
