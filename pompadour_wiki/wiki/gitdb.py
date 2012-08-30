from git import *
from git.exc import InvalidGitRepositoryError

class Repository(object):
    """ Repository object """

    def __init__(self, gitdir):
        try:
            self.repo = Repo(gitdir)
        except InvalidGitRepositoryError:
            pass

        self.repo_tree = self.repo.heads.master.commit.tree
        self.blobs = []
        self.trees = [self.repo_tree]

        for e in self.repo_tree.traverse():
            if type(e) is Tree:
                self.trees.append(e)
            else:
                self.blobs.append(e)

    def is_dir(self, path):
        if path == self.repo_tree.path:
            return True

        for e in self.repo_tree.traverse():
            if e.path == path and type(e) is Tree:
                return True

        return False

    def get_content(self, path):
        for blob in self.blobs:
            if blob.path == path:
                return blob.data_stream.read()

    def get_tree(self, path):
        for tree in self.trees:
            if tree.path == path:
                ret = []

                ret = ret + [b.path for b in tree.blobs]
                ret = ret + [t.path + '/' for t in tree.trees]

                return ret
