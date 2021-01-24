# How to make changes using branches:

1. Start with the branch you want to make changes in (usually master or main)	
`git switch master`
1. Create a new branch, based on the previous branch: 
`git switch/checkout -b myname/what-the-branch-is-for`
 At this point you should be on your new “feature” branch.

1. Make your changes, edit some files, add some files, etc. in your editor. When you’re at a good stopping point, STAGE your changes (set your changes up to go into the repository in one commit). For each file you’ve added, removed or edited, stage by running add :
`git add file1 file2 file3 file4`
`git add file5`
1. Check the status to ensure all the files you want to commit together are listed:
`git status`
1. COMMIT the changes that have been staged to the LOCAL repository
`git commit `
1. Ensure that there are no files that somehow got missed
`git status`
1. Push to github (the remote)
`git push`
Note: if you have never pushed remotely before, you will need to add `--set-upstream` as the error message will explain
At this point your branch should be updated on github
1. Do you have to make more edits? If yes, go to (3)
1. If you need to make a pull request:
   1. Go to github.com, navigate to the repository and create a pull request
   1. Wait until you get approval to merge the request,
   1. If you need to make further changes, go to (3). Pull requests will automatically update.
   1. When ready, merge using the github.com interface.
   1. If there is a merge conflict, then see RESOLVE CONFLICTS sheet.
1. If you do not need to make a pull request:
   1. You can merge branch using the interface on github.com OR:
   1. Switch to the master (or branch you want to merge into):
   `git switch master`
   1. Merge in the changes
   `git merge myname/what-the-branch-is-for`
   1. If there are conflicts, see the RESOLVE CONFLICTS sheet




