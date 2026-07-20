"""Custom Pylint checker plugin for project-specific rules."""
from pylint.checkers import BaseChecker
from astroid import nodes

class CustomPrintChecker(BaseChecker):
    """Checker that flags any usage of print() instead of standard logging."""
    name = "custom-print-checker"
    msgs = {
        "W9901": (
            "Use of print() is forbidden. Use logging instead.",
            "avoid-print",
            "Used when print() function is called instead of logging.",
        ),
    }

    def visit_call(self, node):
        """Called for every function call in the AST."""
        if isinstance(node.func, nodes.Name) and node.func.name == "print":
            self.add_message("avoid-print", node=node)

def register(linter):
    """Required function to register the checker with pylint."""
    linter.register_checker(CustomPrintChecker(linter))
