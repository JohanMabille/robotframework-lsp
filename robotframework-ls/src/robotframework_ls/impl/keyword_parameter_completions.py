from typing import List

from robotframework_ls.impl.protocols import ICompletionContext


def _create_completion_item(arg, selection, col_start, col_end):
    """
    :param IKeywordFound keyword_found:
    :param selection:
    :param token:
    """
    from robocorp_ls_core.lsp import (
        CompletionItem,
        InsertTextFormat,
        Position,
        Range,
        TextEdit,
    )
    from robocorp_ls_core.lsp import MarkupKind
    from robocorp_ls_core.lsp import CompletionItemKind

    label = arg
    text = arg

    text_edit = TextEdit(
        Range(
            start=Position(selection.line, col_start),
            end=Position(selection.line, col_end),
        ),
        text,
    )

    return CompletionItem(
        label,
        kind=CompletionItemKind.Field,
        text_edit=text_edit,
        documentation="",
        insertTextFormat=InsertTextFormat.PlainText,
        documentationFormat=MarkupKind.PlainText,
    ).to_dict()


def complete(completion_context: ICompletionContext) -> List[dict]:
    from robotframework_ls.impl.protocols import IKeywordFound

    ret = []

    current_keyword_definition = completion_context.get_current_keyword_definition()
    if current_keyword_definition is not None:
        keyword_found: IKeywordFound = current_keyword_definition.keyword_found
        keyword_args = keyword_found.keyword_args
        if keyword_args:
            sel = completion_context.sel
            line_to_column = sel.line_to_column

            for arg in keyword_args:
                if arg.startswith("${") and arg.endswith("}"):
                    arg = arg[2:-1]

                if arg.startswith("**"):
                    continue

                elif arg.startswith("*"):
                    continue

                eq_i = arg.rfind("=")
                if eq_i != -1:
                    arg = arg[:eq_i]

                colon_i = arg.rfind(":")
                if colon_i != -1:
                    arg = arg[:colon_i]

                arg = arg.strip()
                if arg:
                    arg += "="

                ret.append(_create_completion_item(arg, sel, sel.col, sel.col))

    return ret
