def test_library_completions_basic(
    data_regression, workspace, cases, libspec_manager, workspace_dir
):
    from robotframework_ls.impl import filesystem_section_completions
    from robotframework_ls.impl.completion_context import CompletionContext

    cases.copy_to("case1", workspace_dir)

    workspace.set_root(workspace_dir, libspec_manager=libspec_manager)
    doc = workspace.get_doc("case1.robot")
    doc.source = """*** Settings ***
Library           collec"""

    completions = filesystem_section_completions.complete(
        CompletionContext(doc, workspace=workspace.ws)
    )

    data_regression.check(completions)


def test_library_completions_middle(
    data_regression, workspace, cases, libspec_manager, workspace_dir
):
    from robotframework_ls.impl import filesystem_section_completions
    from robotframework_ls.impl.completion_context import CompletionContext

    cases.copy_to("case1", workspace_dir)

    workspace.set_root(workspace_dir, libspec_manager=libspec_manager)
    doc = workspace.get_doc("case1.robot")
    doc.source = """*** Settings ***
Library           collecXXX"""

    line, col = doc.get_last_line_col()
    completions = filesystem_section_completions.complete(
        CompletionContext(doc, workspace=workspace.ws, line=line, col=col - len("XXX"))
    )

    data_regression.check(completions)


def test_library_completions_local(
    data_regression, workspace, cases, libspec_manager, workspace_dir
):
    from robotframework_ls.impl import filesystem_section_completions
    from robotframework_ls.impl.completion_context import CompletionContext

    cases.copy_to("case1", workspace_dir)

    workspace.set_root(workspace_dir, libspec_manager=libspec_manager)
    doc = workspace.get_doc("case1.robot")
    doc.source = """*** Settings ***
Library           caseXXX"""

    line, col = doc.get_last_line_col()
    completions = filesystem_section_completions.complete(
        CompletionContext(doc, workspace=workspace.ws, line=line, col=col - len("XXX"))
    )

    data_regression.check(completions)


def test_library_completions_in_dirs(
    data_regression, workspace, cases, libspec_manager, workspace_dir
):
    from robotframework_ls.impl import filesystem_section_completions
    from robotframework_ls.impl.completion_context import CompletionContext
    import os.path

    cases.copy_to("case1", workspace_dir)

    workspace.set_root(workspace_dir, libspec_manager=libspec_manager)
    doc = workspace.get_doc("case1.robot")
    doc.source = """*** Settings ***
Library           dir1/caseXXX"""

    dir1 = os.path.join(workspace_dir, "dir1")
    os.mkdir(dir1)

    mycase_py = os.path.join(dir1, "mycase.py")
    with open(mycase_py, "w") as stream:
        stream.write("""def my_method():\n    pass""")

    line, col = doc.get_last_line_col()
    completions = filesystem_section_completions.complete(
        CompletionContext(doc, workspace=workspace.ws, line=line, col=col - len("XXX"))
    )

    data_regression.check(completions)


def test_library_completions_absolute(
    data_regression, workspace, cases, libspec_manager, workspace_dir
):
    from robotframework_ls.impl import filesystem_section_completions
    from robotframework_ls.impl.completion_context import CompletionContext
    import os.path

    cases.copy_to("case1", workspace_dir)

    dir1 = os.path.join(workspace_dir, "dir1")
    os.mkdir(dir1)

    workspace.set_root(workspace_dir, libspec_manager=libspec_manager)

    directory = workspace_dir
    directory = directory.replace(u"\\", u"/")

    doc = workspace.get_doc("case1.robot")
    doc.source = u"""*** Settings ***
Library           %s/""" % (
        directory,
    )

    completions = filesystem_section_completions.complete(
        CompletionContext(doc, workspace=workspace.ws)
    )
    _line, col = doc.get_last_line_col()
    for completion in completions:
        # The range will change based on the workspace_dir contents, so,
        # check it here and not in the data regression.
        found_range = completion["textEdit"].pop("range")
        assert found_range == {
            "start": {"line": 1, "character": col},
            "end": {"line": 1, "character": col},
        }

    data_regression.check(completions)


def test_resource_completions_relative(
    data_regression, workspace, cases, libspec_manager, workspace_dir
):
    from robotframework_ls.impl import filesystem_section_completions
    from robotframework_ls.impl.completion_context import CompletionContext

    cases.copy_to("case4", workspace_dir)

    workspace.set_root(workspace_dir, libspec_manager=libspec_manager)
    doc = workspace.get_doc("case4.robot")
    doc.source = """*** Settings ***
Resource           case"""

    completions = filesystem_section_completions.complete(
        CompletionContext(doc, workspace=workspace.ws)
    )

    data_regression.check(completions)


def test_resource_completions_resolve_var(
    data_regression, workspace, cases, libspec_manager, workspace_dir
):
    from robotframework_ls.impl import filesystem_section_completions
    from robotframework_ls.impl.completion_context import CompletionContext
    from robotframework_ls.impl.robot_lsp_constants import OPTION_ROBOT_VARIABLES
    from robotframework_ls.robot_config import RobotConfig

    cases.copy_to("case4", workspace_dir)

    config = RobotConfig()
    config.update({"robot": {"variables": {"ext_folder": cases.get_path("ext")}}})
    assert config.get_setting(OPTION_ROBOT_VARIABLES, dict, {}) == {
        "ext_folder": cases.get_path("ext")
    }

    workspace.set_root(workspace_dir, libspec_manager=libspec_manager)
    doc = workspace.get_doc("case4.robot")
    doc.source = """*** Settings ***
Resource           ${ext_folder}/"""

    completions = filesystem_section_completions.complete(
        CompletionContext(doc, workspace=workspace.ws, config=config)
    )

    data_regression.check(completions)
