import ast
import importlib.metadata
import re
from typing import Any
import sys
from typing import Generator
from typing import Type

from flake8.options.manager import OptionManager
from flake8.options.manager import argparse
from classify_imports import classify_base

PROBLEM_MESSAGE = "FAI001 {name} is not on the allowlist for imports"
DEFAULT_ALLOWLIST = [".*"]


class Visitor(ast.NodeVisitor):
    def __init__(self, allowlist: list[str]) -> None:
        self.problems: list[tuple[int, int, str]] = []
        self.patterns = [re.compile(p) for p in allowlist]

    def is_allowed(self, name: str) -> bool:
        return (
            any((p.match(name) for p in self.patterns))
            or classify_base(name) != "THIRD_PARTY"
        )

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if not self.is_allowed(alias.name):
                if sys.version_info.minor > 9:
                    self.problems.append((alias.lineno, alias.col_offset, alias.name))
                else:
                    self.problems.append((node.lineno, node.col_offset, alias.name))
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib.metadata.version(__name__)
    allowlist: list[str] = DEFAULT_ALLOWLIST

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    @classmethod
    def add_options(cls, manager: OptionManager):
        manager.add_option(
            long_option_name="--import-allowlist",
            default=cls.allowlist,
            comma_separated_list=True,
            parse_from_config=True,
            help="Comma-separated list of allowed third party modules",
        )

    @classmethod
    def parse_options(cls, options: argparse.Namespace):
        cls.allowlist = options.import_allowlist

    def run(self) -> Generator[tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor(allowlist=self.allowlist)
        visitor.visit(self._tree)
        for line, col, name in visitor.problems:
            yield line, col, PROBLEM_MESSAGE.format(name=name), type(self)
