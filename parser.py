import xml.sax
import csv

class OurContentHandler(xml.sax.ContentHandler):
    def __init__(self, csv_writer):
        xml.sax.ContentHandler.__init__(self)
        self.writer = csv_writer
        # keeps track of our traversal
        self.tag_stack = []
        # the classes of records we are interested in
        self.subclasses = ["incollection", "proceedings", "inproceedings", "article", "book", "phdthesis", "mastersthesis", "www"]
        # the XML tags we are interested in
        self.needed_tags = ["key", "year", "title", "author", "crossref", "journal"] + self.subclasses

    def startElement(self, name, attrs):
        if name in self.needed_tags:
            self.tag_stack.append(name)
        if name in self.subclasses:
            self.field = {"key": "", "title": "", "year": "", "authors": [], "journal": "", "crossref": ""}
            if attrs:
                self.field["key"] = attrs.getValue("key")
        if name == "author":
            self.author_name = ""

    def characters(self, content):
        if content.strip():
            last = self.tag_stack[-1]
            attr_list = ["year", "title", "crossref", "journal"]
            if last == "author":
                #self.field["authors"].append(content)
                self.author_name += content
            if last in attr_list:
                self.field[last] += content

    def endElement(self, name):
        if name in self.needed_tags:
            self.tag_stack.pop()
        # only append to authors (list) when we have the complete author name
        if name == "author":
            self.field["authors"].append(self.author_name)
        if name in self.subclasses and name != "www":
            row = [name, self.field["key"], self.field["title"],
                   self.field["year"], ','.join(self.field["authors"]),
                   self.field["journal"], self.field["crossref"]]
            self.writer.writerow(row)

def main(sourceFileName):
    csv_file = open('./field.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["class", "key", "title", "year", "authors", "journal", "crossref"])
    source = open(sourceFileName)
    xml.sax.parse(source, OurContentHandler(csv_writer))

if __name__ == "__main__":
    main("/Users/koallen/Downloads/dblp.xml")
