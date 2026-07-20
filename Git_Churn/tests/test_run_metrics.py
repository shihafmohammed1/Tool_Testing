from run_metrics import build_parser


def test_build_parser_has_repo_argument():
    parser = build_parser()
    actions = {action.dest for action in parser._actions}
    assert "repo" in actions
