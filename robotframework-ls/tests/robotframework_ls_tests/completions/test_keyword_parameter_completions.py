def test_keyword_completions_params_basic(workspace, libspec_manager, data_regression):
    from robotframework_ls.impl.completion_context import CompletionContext
    from robotframework_ls.impl import keyword_parameter_completions

    workspace.set_root("case2", libspec_manager=libspec_manager)
    doc = workspace.get_doc("case2.robot")
    doc.source = """
*** Keywords ***
My Equal Redefined
    [Arguments]         ${arg1}     ${arg2}
    Should Be Equal     ${arg1}     ${arg2}

*** Task ***
Some task
    My Equal Redefined    """

    completions = keyword_parameter_completions.complete(
        CompletionContext(doc, workspace=workspace.ws)
    )

    data_regression.check(completions)


def test_keyword_completions_params_complete_existing(
    workspace, libspec_manager, data_regression
):
    from robotframework_ls.impl.completion_context import CompletionContext
    from robotframework_ls.impl import keyword_parameter_completions

    workspace.set_root("case2", libspec_manager=libspec_manager)
    doc = workspace.get_doc("case2.robot")
    doc.source = """
*** Keywords ***
My Equal Redefined
    [Arguments]         ${arg1}     ${arg2}    ${another3}
    Should Be Equal     ${arg1}     ${arg2}    ${another3}

*** Task ***
Some task
    My Equal Redefined    ar"""

    completions = keyword_parameter_completions.complete(
        CompletionContext(doc, workspace=workspace.ws)
    )

    data_regression.check(completions)


def test_keyword_completions_params_dont_complete_1(workspace, libspec_manager):
    from robotframework_ls.impl.completion_context import CompletionContext
    from robotframework_ls.impl import keyword_parameter_completions

    workspace.set_root("case2", libspec_manager=libspec_manager)
    doc = workspace.get_doc("case2.robot")
    doc.source = """
*** Keywords ***
My Equal Redefined
    [Arguments]         ${arg1}     ${arg2}    ${another3}
    Should Be Equal     ${arg1}     ${arg2}    ${another3}

*** Task ***
Some task
    My Equal Redefined    ar"""

    line, col = doc.get_last_line_col()
    col -= 1

    completions = keyword_parameter_completions.complete(
        CompletionContext(doc, workspace=workspace.ws, line=line, col=col)
    )

    assert not completions

    col -= 1

    completions = keyword_parameter_completions.complete(
        CompletionContext(doc, workspace=workspace.ws, line=line, col=col)
    )

    assert not completions


def _todo_test_keyword_completions_params_dont_complete_2(workspace, libspec_manager):
    from robotframework_ls.impl.completion_context import CompletionContext
    from robotframework_ls.impl import keyword_parameter_completions

    workspace.set_root("case2", libspec_manager=libspec_manager)
    doc = workspace.get_doc("case2.robot")
    doc.source = """
*** Keywords ***
My Equal Redefined
    [Arguments]         ${arg1}     ${arg2}    ${another3}
    Should Be Equal     ${arg1}     ${arg2}    ${another3}

*** Task ***
Some task
    My Equal Redefined    ar="""

    completions = keyword_parameter_completions.complete(
        CompletionContext(doc, workspace=workspace.ws)
    )

    assert not completions
