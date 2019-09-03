import os
import git

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_version(git_path=CURRENT_DIR):
    """
    Gets version from git tags
    :return: version with the following format MAJOR.MINOR.PATCH
    """

    try:
        repo = git.Repo(git_path)
        tags = repo.tags
        tags = sorted(tags, key=lambda t: t.commit.committed_datetime)
    except git.exc.InvalidGitRepositoryError:
        return "v0.0.0"
    except TypeError:
        return "v0.0.0"

    if len(tags) == 0:
        return "v0.0.0"
    else:
        latest_tag = tags[-1]
        return latest_tag.name


def update_version(version, package_name):
    template_file = "{}/__init__.py.in".format(package_name)
    target_file = "{}/__init__.py".format(package_name)

    with open(template_file, mode="r") as f:
        text = f.read()
        f.close()

    index_of_the_occurrence = 3

    text = text.replace("{VERSION_PLACEHOLDER}", version, index_of_the_occurrence)

    if os.path.isfile(target_file):
        os.remove(target_file)
    with open(target_file, mode="w") as f:
        f.write(text)
        f.close()


def main():
    version = get_version(CURRENT_DIR)[1:]
    package_name = "typedresult"
    update_version(version, package_name)
    print('New version ({}) added to  "{}/__init__.py"'.format(version, package_name))


if __name__ == "__main__":
    main()
