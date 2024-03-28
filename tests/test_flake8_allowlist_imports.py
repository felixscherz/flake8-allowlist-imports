import argparse
import ast

from flake8_allowlist_imports import Plugin


def _results(s: str, allowlist: list[str]) -> set[str]:
    tree = ast.parse(s)
    options = argparse.Namespace(import_allowlist=allowlist)
    Plugin.parse_options(options)
    plugin = Plugin(tree=tree)
    return {f"{line}:{col} {msg}" for line, col, msg, _ in plugin.run()}


def test_trivial_case():
    assert _results("", [".*"]) == set()

def test_classify():
    from classify_imports import classify_base
    assert classify_base("mypackage") == "THIRD_PARTY"

def test_forbid_env_variables_via_subscript():
    code = """import mypackage"""
    expected = {"1:7 FAI001 mypackage is not on the allowlist for imports"}
    assert _results(code, ["myotherpackage"]) == expected
