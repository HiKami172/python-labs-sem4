class JsonDecoder:
    int_const = tuple("1 2 3 4 5 6 7 8 9 0 -".split(" "))

    def __init__(self):
        self.json_to_true = self.json_to_custom("true", True)
        self.json_to_false = self.json_to_custom("false", False)
        self.json_to_none = self.json_to_custom("null", None)

        self.json_types = [
            ("{", self.json_to_dict),
            ("[", self.json_to_list),
            ('"', self.json_to_string),
            (self.int_const, self.json_to_numeric),
            ("false", self.json_to_false),
            ("true", self.json_to_true),
            ("null", self.json_to_none)
        ]

    def json_to_custom(self, word, value=None):
        def result(obj):
            if obj.startswith(word):
                return value, obj[len(word):]

        result.__name__ = "parse_%s" % word
        return result

    def json_to_dict(self, objs):
        res = {}
        objs = remove_prefix(objs, "{").lstrip()
        while not objs.startswith("}"):
            (key, objs) = self.json_to_obj(objs)
            objs = remove_prefix(objs, ":")
            (value, objs) = self.json_to_obj(objs)
            res[key] = value
            objs = remove_prefix(objs, ",").lstrip()
        return res, remove_prefix(objs, "}")

    def json_to_list(self, objs):
        res = []
        objs = remove_prefix(objs, "[").lstrip()
        while not objs.startswith("]"):
            (value, objs) = self.json_to_obj(objs)
            res.append(value)
            objs = remove_prefix(objs, ",").lstrip()
        return res, remove_prefix(objs, "]")

    def json_to_numeric(self, obj):
        for i in range(len(obj)):
            if obj[i] not in self.int_const and obj[i] != ".":
                try:
                    return int(obj[:i]), obj[i:]
                except ValueError:
                    return float(obj[:i]), obj[i:]
        if '.' in obj[:i+1]:
            return float(obj[:i+1]), obj[i+1:]
        return int(obj[:i+1]), obj[i+1:]

    def json_to_string(self, obj):
        obj = remove_prefix(obj, '"')
        tmp = obj.find('"')
        return obj[:tmp], obj[tmp + 1:]

    def json_to_obj(self, obj):
        obj = obj.lstrip()
        for (char, func) in self.json_types:
            if not obj:
                pass
            elif obj.startswith(char):
                return func(obj)

        raise ValueError(obj.split(",") + " is not supported!")

    def json_decode(self, obj):
        (item, obj) = self.json_to_obj(obj)
        obj = obj.lstrip()
        if obj != "":
            raise ValueError("Wrong format!")
        else:
            return item


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
