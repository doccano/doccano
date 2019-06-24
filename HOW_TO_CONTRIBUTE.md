# Contribution Workflow

In order to follow a good GitHub collaboration workflow, there are some tips might be helpful.

## Build a development environment

Please read this issue [#149](https://github.com/chakki-works/doccano/issues/149) first.

## Update to latest version

Run the following command to get the latest version.

```
# Add upstream
git remote add upstream https://github.com/gong-io/doccano

# Fetch all the branches of that remote into remote-tracking branches,
git fetch upstream

# Make sure that you're on your master branch:
git checkout master

# Rewrite your master branch so that any commits of yours that
# aren't already in upstream/master are replayed on top of that
# other branch:
git rebase upstream/master
```

If you already wrote code directly on the master branch. This will cause conflict when you want to rebase latest version to your forked repo.

In order to rebase your forked repo (master branch) to the latest version. You should make a copy of your code, where the code you already wrote. And then run the following command.

```
# Add upstream
git remote add upstream https://github.com/gong-io/doccano

# Fetch all the branches of that remote into remote-tracking branches,
git fetch upstream

# Make sure that you're on your master branch:
git checkout master

# Rewrite your master branch to make  your local doccano be the same with upstream/master 
git reset --hard upstream/master

# Make your forked repo same as the upstream
git push -f origin master
```

`git reset --hard upstream/master` will make your local version totally match the project's master branch and delete the work you have committed. So, please make a copy before running the `git reset --hard upstream/master`.

`git push -f origin master` will make your forked repo be same with the master branch.

## Development

Right now, your local master branch, origin master branch (forked repo in GitHub), and upstream master branch (original doccano repo) should be the same.

Usually, we use a new branch for feature development or bug fix, like 'feature/auto_label', 'bug/annotation. For example, we want to implement the JSON export feature, so we name a new branch as `feature/json_export`.

```
git checkout -b 'feature/json_export'
```

You should make all your commit in this branch. Remember I told you to make a copy? Here you can use the copied code in the development. 

As for the commit message, it would be great to add an issue prefix. For example, `git commit -m 'iss17: support for exporting JSON file'`. This is for an explicit statement.

## Pull Request (PR)

After you finish the development, you can make a PR.

First, push the branch to origin

```
git push origin feature/json_export
```

Then make a PR in the GitHub page you forked. Below is not command, just for demo.

```
BrambleXu wants to merge 5 commits into gong-io:master from BrambleXu:feature/json_export
```

You can write some descriptions in the comment for this PR. This [Git Commit Message Style Guide](http://udacity.github.io/git-styleguide/?utm_source=wanqu.co&utm_campaign=Wanqu+Daily&utm_medium=website) might be helpful.

If you have any questions feel free to ask us. 