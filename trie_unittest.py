#!/usr/bin/python -B

import unittest
from trie import Trie


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()

    def _square_brackets(self, key):
        return self.trie[key]

    def test_basicAssignment(self):
        self.trie["Foo"] = True
        self.assertTrue(self.trie["Foo"])
        self.assertRaises(KeyError, self._square_brackets, "Food")
        self.assertEqual(1, len(self.trie))
        self.assertEqual(3, self.trie.nodeCount())
        self.assertTrue("Foo" in self.trie)
        self.trie["Bar"] = None
        self.assertTrue("Bar" in self.trie)

    def test_basicRemoval(self):
        self.trie["Foo"] = True
        self.assertTrue(self.trie["Foo"])
        del self.trie["Foo"]
        self.assertRaises(KeyError, self._square_brackets, "Foo")
        self.assertEqual(0, len(self.trie))
        self.assertEqual(0, self.trie.nodeCount())
        self.assertFalse("Foo" in self.trie)

    def test_MixedTypes(self):
        self.trie["Foo"] = True
        self.trie[[1, 2, 3]] = True
        self.assertTrue(self.trie["Foo"])
        self.assertTrue(self.trie[[1, 2, 3]])
        self.assertTrue([1, 2, 3] in self.trie)
        self.assertTrue("Foo" in self.trie)
        del self.trie[[1, 2, 3]]
        self.assertFalse([1, 2, 3] in self.trie)

    def test_Iteration(self):
        self.trie["Foo"] = True
        self.trie["Bar"] = True
        self.trie["Grok"] = True
        for k in self.trie:
            self.assertTrue(k in self.trie)
            self.assertTrue(self.trie[k])

    def test_Addition(self):
        self.trie["Foo"] = True
        t2 = Trie()
        t2["Food"] = True
        t3 = t2 + self.trie
        self.assertTrue("Foo" in self.trie)
        self.assertFalse("Food" in self.trie)
        self.assertTrue("Food" in t2)
        self.assertFalse("Foo" in t2)
        self.assertTrue("Foo" in t3)
        self.assertTrue("Food" in t3)

    def test_Subtraction(self):
        self.trie["Food"] = True
        self.trie["Foo"] = True
        t2 = Trie()
        t2["Food"] = True
        t3 = self.trie - t2
        t4 = t2 - self.trie
        self.assertTrue("Food" in self.trie)
        self.assertTrue("Foo" in self.trie)
        self.assertTrue("Food" in t2)
        self.assertTrue("Foo" in t3)
        self.assertFalse("Food" in t3)
        self.assertFalse("Foo" in t4)
        self.assertFalse("Food" in t4)

    def test_SelfAdd(self):
        self.trie["Foo"] = True
        t2 = Trie()
        t2["Food"] = True
        self.assertTrue("Foo" in self.trie)
        self.assertFalse("Food" in self.trie)
        self.assertTrue("Food" in t2)
        self.assertFalse("Foo" in t2)
        self.trie += t2
        self.assertTrue("Foo" in self.trie)
        self.assertTrue("Food" in self.trie)

    def test_SelfSub(self):
        self.trie["Foo"] = True
        self.trie["Food"] = True
        t2 = Trie()
        t2["Food"] = True
        self.assertTrue("Food" in self.trie)
        self.assertTrue("Foo" in self.trie)
        self.assertTrue("Food" in t2)
        self.trie -= t2
        self.assertFalse("Food" in self.trie)
        self.assertTrue("Foo" in self.trie)
        self.assertTrue("Food" in t2)

    def test_SelfGet(self):
        self.trie["Foo"] = True
        self.assertTrue(self.trie["Foo"])
        self.assertRaises(KeyError, self._square_brackets, "Food")
        self.assertEqual("Bar", self.trie.get("Food", "Bar"))
        self.assertEqual("Bar", self.trie.get("Food", default="Bar"))
        self.assertTrue(self.trie.get("Foo"))
        self.assertTrue(self.trie.get("Food") is None)

    def test_KeysByPrefix(self):
        self.trie["Foo"] = True
        self.trie["Food"] = True
        self.trie["Eggs"] = True
        kset = self.trie.keys()
        self.assertTrue("Foo" in kset)
        self.assertTrue("Food" in kset)
        self.assertTrue("Eggs" in kset)
        kset = self.trie.keys("Foo")
        self.assertTrue("Foo" in kset)
        self.assertTrue("Food" in kset)
        kset = self.trie.keys("Ox")
        self.assertEqual(0, len(kset))

    def test_EmptyKey(self):
        # Both empty sequences terminate at the root; the trie indexes the
        # sequence of elements and does not distinguish "" from ().
        self.trie[""] = "empty-string"
        self.assertEqual("empty-string", self.trie[""])
        self.assertIn("", self.trie)

        self.trie[()] = "empty-tuple"
        self.assertEqual("empty-tuple", self.trie[()])
        self.assertIn((), self.trie)

        # Deleting the empty key removes it cleanly.
        del self.trie[""]
        self.assertNotIn("", self.trie)

    def test_SequenceCollapse(self):
        # A string and its list/tuple of characters are structurally identical.
        t = Trie()
        t["Foo"] = 1
        self.assertEqual(1, t[("F", "o", "o")])
        self.assertEqual(1, t[["F", "o", "o"]])
        # ...and they all appear once (as the string) in keys().
        keys = t.keys()
        self.assertIn("Foo", keys)
        self.assertNotIn(["F", "o", "o"], keys)

    def test_MultiCharChunkReturnsList(self):
        # With a len(k) <= 2 rule, elements longer than two chars do not
        # reconstruct as a single string; they come back as a list. This is the
        # historical behavior (commit be5e3e4) that my earlier "all strings"
        # guess had silently broken: ["foo","bar"] must NOT become "foobar".
        t = Trie()
        t["foo", "bar"] = 1
        keys = t.keys()
        self.assertIn(["foo", "bar"], keys)
        self.assertNotIn("foobar", keys)

    def test_TwoCharChunkStillString(self):
        # A two-char element counts as a str chunk (len <= 2), so the key
        # reconstructs as a string.
        t = Trie()
        t["Fo", "o"] = 1
        self.assertIn("Foo", t.keys())


if __name__ == '__main__':
    unittest.main()
