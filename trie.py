

class Trie(object):
    def __init__(self):
        self.path = {}
        self.value = None
        self.value_valid = False

    def __setitem__(self, key, value):
        if len(key) == 0:
            self.value = value
            self.value_valid = True
            return
        head = key[0]
        if head in self.path:
            node = self.path[head]
        else:
            node = Trie()
            self.path[head] = node

        if len(key) > 1:
            remains = key[1:]
            node.__setitem__(remains, value)
        else:
            node.value = value
            node.value_valid = True

    def __delitem__(self, key):
        if len(key) == 0:
            self.value_valid = False
            self.value = None
            return
        head = key[0]
        if head in self.path:
            node = self.path[head]
            if len(key) > 1:
                remains = key[1:]
                node.__delitem__(remains)
            else:
                node.value_valid = False
                node.value = None
            if len(node) == 0:
                del self.path[head]

    def __getitem__(self, key):
        if len(key) == 0:
            if self.value_valid:
                return self.value
            raise KeyError(key)
        head = key[0]
        if head in self.path:
            node = self.path[head]
        else:
            raise KeyError(key)
        if len(key) > 1:
            remains = key[1:]
            try:
                return node.__getitem__(remains)
            except KeyError:
                raise KeyError(key)
        elif node.value_valid:
            return node.value
        else:
            raise KeyError(key)

    def __contains__(self, key):
        try:
            self.__getitem__(key)
        except KeyError:
            return False
        return True

    def __len__(self):
        n = 1 if self.value_valid else 0
        for k in self.path.keys():
            n = n + len(self.path[k])
        return n

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def nodeCount(self):
        n = 0
        for k in self.path.keys():
            n = n + 1 + self.path[k].nodeCount()
        return n

    def keys(self, prefix=()):
        return self.__keys__(prefix)

    def __keys__(self, prefix=(), seen=()):
        result = []
        if self.value_valid:
            result.append(self._reconstruct(seen))
        if len(prefix) > 0:
            head = prefix[0]
            remaining = prefix[1:]
            children = [(head, self.path[head])] if head in self.path else []
        else:
            remaining = ()
            children = list(self.path.items())
        for k, child in children:
            result.extend(child.__keys__(remaining, seen + (k,)))
        return result

    @staticmethod
    def _reconstruct(seen):
        # Rebuild the original key from the elements collected along the path.
        # The trie indexes *the sequence of elements*, not the container, so
        # "Foo", ["F","o","o"], and ("F","o","o") all collapse to "Foo".
        # Following Bill's historical len(k) <= 2 clue (commit be5e3e4): a key
        # reconstructs as a string only when every element is a string of
        # length at most two; anything else (multi-char chunks, ints, lists or
        # tuples) is returned as a list rather than the old prefix-arg bug.
        if seen and all(isinstance(x, str) and len(x) <= 2 for x in seen):
            return "".join(seen)
        return list(seen)

    def __iter__(self):
        for k in self.keys():
            yield k

    def __add__(self, other):
        result = Trie()
        result += self
        result += other
        return result

    def __sub__(self, other):
        result = Trie()
        result += self
        result -= other
        return result

    def __iadd__(self, other):
        for k in other:
            self[k] = other[k]
        return self

    def __isub__(self, other):
        for k in other:
            del self[k]
        return self
