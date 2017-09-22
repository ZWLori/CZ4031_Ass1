import xml.sax
import csv

class OurContentHandler(xml.sax.ContentHandler):

    def __init__(self, csv_writer):
        xml.sax.ContentHandler.__init__(self)
        self.writer = csv_writer

    def startElement(self, name, attrs):
        self.tag = name
        self.subclasses = ["incollection", "proceedings", "inproceedings", "article", "book", "www", "phdthesis", "mastersthesis"]
        if name in self.subclasses :
            self.field = {"key": "", "title": "", "year": "", "authors": []}
            if attrs:
                self.field["key"] = attrs.getValue("key")

    def characters(self, content):
        if content.strip():
            attr_list = ["year", "title"]
            if self.tag == "author":
                self.field["authors"].append(content)
            if self.tag in attr_list:
                self.field[self.tag] = content

    def endElement(self, name):
        # write to csv file
        if name in self.subclasses :
            row = [name, self.field["key"], self.field["title"],
                   self.field["year"], ','.join(self.field["authors"])]
            self.writer.writerow(row)


def main(sourceFileName):
    csv_file = open('./field.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["class", "key", "title", "year", "authors"])
    source = open(sourceFileName)
    xml.sax.parse(source, OurContentHandler(csv_writer))

if __name__ == "__main__":
    main("/Users/ZWLori/Downloads/dblp.xml")
