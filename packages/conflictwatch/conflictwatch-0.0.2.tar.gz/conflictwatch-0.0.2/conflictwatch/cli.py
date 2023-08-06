from argparse import ArgumentParser
import subprocess


def has_conflict(branch_name):
    try:
        base_commit_sha = subprocess.check_output(['git', 'merge-base', 'HEAD', branch_name]).decode().strip()
        patch = subprocess.run(['git', 'format-patch', f'{base_commit_sha}..{branch_name}', '--stdout'], check=True, capture_output=True)
        apply_check = subprocess.run(['git', 'apply', '--3way', '--check', '-'],
                                    input=patch.stdout, capture_output=True)

        if "with conflicts" in apply_check.stderr.decode():
            return True
        else:
            return False
    
    except subprocess.CalledProcessError as e:
        raise Exception('Git command error', e)


def main():
    print('Running...')
    parser = ArgumentParser(prog='cli')
    parser.add_argument("-a","--all-branches",action="store_true",help="Check all remote branches against your current HEAD and staging")
    args = parser.parse_args()

    remote_branches = {'origin/master'}

    if args.all_branches:
        remote_branches = set(subprocess.check_output(["git", "branch", "-r"]).decode().split('\n'))
        remote_branches = {branch.strip() for branch in remote_branches if branch != ''}

    subprocess.check_output(["git", "fetch"])

    for branch_name in remote_branches:
        if has_conflict(branch_name):
            print(f"{branch_name} has a conflict with our branch!")


if __name__ == '__main__':
    main()
