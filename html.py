class Tag:
    def __init__(self, tag, klass = "", is_single=False, **kwargs):
        self.tag = tag
        self.text = ""
        self.klass = klass
        self.is_single = is_single

        self.arguments = [""]
        self.childrens = []

        self.inside = []

        if klass != "":
            self.klass = " %s=\"%s\"" % ("class", " ".join(klass))

        for argument, value in kwargs.items():
            self.arguments.append("%s=\"%s\"" % (argument, value))
    
    def __iadd__(self, other):
        self.childrens.append(str(other))
        return self
    
    def __str__(self):
        if len(self.arguments) < 2:
            self.arguments = []
        if self.childrens == [] and self.is_single is not True:
            return "  " + "<{tag}{klass}{arg}>{text}</{tag}>\n".format(tag = self.tag, klass = self.klass, arg = " ".join(self.arguments), text = self.text)
        elif self.is_single is True:
            return "  " + "<{tag}{klass}{arg}>\n".format(tag = self.tag, klass = self.klass, arg = " ".join(self.arguments))
        else:
            start = "<{tag}{klass}{arg}>{text}\n{inside}{childrens}".format(tag = self.tag, klass = self.klass, arg = " ".join(self.arguments), inside = "  ", text = self.text, childrens = "  ".join(self.childrens))
            ending = "</{tag}>\n".format(tag = self.tag)
            return start + "  " + ending
    
    def __enter__(self):
        return self
    
    def __exit__(self, *arg):
        pass

# paragraph = Tag(
#     "p",
#     klass=("text-align-right", "text-nice"),
#     id="heading-text",
#     data_bind="not-above"
# )
# paragraph.text = "Some text inside tag"
# oh = Tag("div", klass="img")
# paragraph+=oh

# print(paragraph)
class HTML:
    def __init__(self, output=None):
        self.str1ng = []
        self.wr1te = output
    
    def __iadd__(self, other):
        self.str1ng.append(str(other))
        return self
    
    def __enter__(self):
        return self
    
    def __exit__(self, *arg):
        if self.wr1te != None:
            with open("%s" % (self.wr1te), "w") as f:
                f.write("".join(self.str1ng))
        else:
            print("".join(self.str1ng))

class TopLevelTag(Tag):
    def __str__(self):
        if len(self.arguments) < 2:
            self.arguments = []
        if self.childrens is False:
            return "<{tag}{klass}{arg}>{text}</{tag}>".format(tag = self.tag, klass = self.klass, arg = " ".join(self.arguments), text = self.text)
        else:
            start = "<{tag}{klass}{arg}>{text}\n{childrens}".format(tag = self.tag, klass = self.klass, arg = " ".join(self.arguments), text = self.text, childrens = "  ".join(self.childrens))
            ending = "</{tag}>\n".format(tag = self.tag)
            return start + ending



with HTML(output="test.html") as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div += img

            body += div

        doc += body