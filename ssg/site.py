import sys

from pathlib import Path


class Site:

    def __init__(self, source, dest, parsers=None):
        self.source = Path(source)
        self.dest = Path(dest)
        self.parsers = parsers or []

    def create_dir(self, Path):
        directory = self.dest / Path.relative_to(self.source)
        directory.mkdir(parents=True, exist_ok=True)

    def load_parser(self, extension):
        for parser in self.parsers:
            if parser.valid_extension(extension):
                return parser

    def run_parser(self, Path):
        parser = self.load_parser(Path.suffix)
        if parser is not None:
            parser.parse(Path, self.source, self.dest)
        else:
            self.error(
                "No parser for the {} extension, file skipped!".format(Path.suffix))

    def build(self):
        self.dest.mkdir(parents=True, exist_ok=True)
        for Path in self.source.rglob("*"):
            if Path.is_dir():
                self.create_dir(Path)
            elif Path.is_file():
                self.run_parser(Path)

    @staticmethod
    def error(message):
        sys.stderr.write("\x1b[1;31m{}\n".format(message))
