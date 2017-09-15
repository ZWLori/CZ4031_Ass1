import xml.sax
import csv

class OurContentHandler(xml.sax.ContentHandler):

    # month??????

    def __init__(self, csv_writer):
        xml.sax.ContentHandler.__init__(self)
        self.pub_table = {}
        self.authors = []
        self.field = {}
        self.tag = ""
        self.key = ""
        self.writer = csv_writer

    def startElement(self, name, attrs):
        self.tag = name
        subclasses = ["incollection", "proceedings", "inproceedings", "article", "book"]
        if name in subclasses :
            if attrs:
                self.key = attrs.getValue("key")
                self.pub_table["type"] = name
                self.pub_table["key"] = self.key
                self.field["key"] = self.key

    def characters(self, content):
        if content.strip():
            attr_list = ["year", "title"]
            if self.tag == "author":
                self.authors.append(content)
            if self.tag in attr_list:
                self.field[self.tag] = content

    def endElement(self, name):
        # write to csv file
        subclasses = ["incollection", "proceedings", "inproceedings", "article", "book"]
        if name in subclasses :
            self.field["author"] = self.authors
            row = [self.field["key"], self.field["title"],
                   self.field["year"], ','.join(self.field["author"])]
            print(row)
            self.writer.writerow(row)


def main(sourceFileName):
    csv_file = open('./field.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["key", "title", "year", "author"])
    source = open(sourceFileName)
    xml.sax.parse(source, OurContentHandler(csv_writer))

if __name__ == "__main__":
    main("./dblp.xml")
