"""Simple calculator."""

import ast
import operator
from typing import Any

from shell.commands.base import BaseCommand, CommandResult


class CalcCommand(BaseCommand):
    name = "calc"
    category = "apps"
    description = "Evaluate a math expression"
    syntax = "calc EXPRESSION"
    examples = ("calc 2 + 2", "calc 10 * 5")

    _OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def execute(self, args: list[str], context: dict[str, Any]) -> CommandResult:
        if not args:
            return CommandResult(output="calc: usage: calc EXPRESSION", exit_code=1)

        expression = " ".join(args)
        try:
            result = self._evaluate(expression)
        except Exception as error:
            return CommandResult(output=f"calc: {error}", exit_code=1)

        return CommandResult(output=str(result))

    def _evaluate(self, expression: str) -> float | int:
        tree = ast.parse(expression, mode="eval")
        return self._eval_node(tree.body)

    def _eval_node(self, node: ast.AST) -> float | int:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._OPS:
            return self._OPS[type(node.op)](self._eval_node(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in self._OPS:
            return self._OPS[type(node.op)](self._eval_node(node.left), self._eval_node(node.right))
        raise ValueError("invalid expression")
