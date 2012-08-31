from git import *
from git.exc import InvalidGitRepositoryError
import simplejson

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

    def exists(self, path):
        if path == self.repo_tree.path:
            return True

        for e in self.repo_tree.traverse():
            if e.path == path:
                return True

        return False

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
                return blob.data_stream.read(), blob.name

    def get_tree(self, path):
        for tree in self.trees:
            if tree.path == path:
                ret = []

                ret = ret + [b.path for b in tree.blobs]
                ret = ret + [t.path + '/' for t in tree.trees]

                return ret, tree.name

    def get_json_tree(self):

        json = {'node': {
            'name': '/',
            'path': '/',
            'type': 'tree',
            'children': []
        }}

        # Get all paths from the repository
        for e in self.repo_tree.traverse():
            spath = e.path.split('/')

            node = json['node']

            # Build tree before inserting node
            for d in spath[:-1]:
                new_node = {'node': {
                    'name': d,
                    'path': e.path,
                    'type': 'tree',
                    'children': []
                }}

                # Search if the node is already in the tree
                for n in node['children']:
                    if d == n['node']['name']:
                        new_node = n
                        break
                else: # if not, just add it
                    node['children'].append(new_node)

                # Up level
                node = new_node['node']

            if type(e) is Tree:
                new_node = {'node': {
                    'name': e.name,
                    'path': e.path,
                    'type': 'tree',
                    'children': []
                }}

                node['children'].append(new_node)
            else:
                new_node = {'node': {
                    'name': e.name,
                    'path': e.path,
                    'type': 'file'
                }}

                node['children'].append(new_node)

        return simplejson.dumps(json)
