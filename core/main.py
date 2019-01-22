import argparse
import sys
import core.verify
import os


def parse_args(args):

    p = argparse.ArgumentParser(
        prog="looker-checker: A tool for validating your lookml project",
        formatter_class=argparse.RawTextHelpFormatter,
        description="Additional tools for administering and validating your LookML",
        epilog="Select one of these sub-commands and you can find more help from there.",
    )

    subs = p.add_subparsers(title="Available sub-commands", dest="command")

    verify_sub = subs.add_parser(
        "verify",
        help="Ensure that every field in your loomkl can be selected without error.",
    )
    verify_sub.add_argument(
        '--models',
        nargs='+',
        help="Include a list of models you'd like to verify. If not set, looker-checker will verify all models."
    )

    if len(args) == 0:
        p.print_help()
        sys.exit(1)
        return

    return p.parse_args()

def check_env_var(name):
    if name in os.environ:
        return 0
    else:
        print("You're missing an environment variable! Make sure the %s variable is set appropriately" % name)
        return 1


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parsed = parse_args(args)

    required_envs = ["LOOKER_BASE_URL", "LOOKER_API_ID", "LOOKER_API_SECRET"]
    is_missing = sum([check_env_var(x) for x in required_envs])
    if is_missing > 0:
        print("Can't proceed without all required environment variables. Bailing out.")
        sys.exit(1)

    # Check for required environment variables
    if parsed.command == "verify":
        task = core.verify.Verify()
        task.run(parsed.models)

if __name__ == "__main__":
    main()
