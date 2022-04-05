Git Script
==========

Script allows you to automatically merge
all commits in your's git branch.

For example, you've got 5 commmits in
your branch.  
![alt-Block-Scheme](./images/commits-before.png "Block-Scheme")  
And you want to merge them
so there will be less commits then it was.  
![alt-Block-Scheme](./images/commits-after.png "Block-Scheme")  
Script recognize that some commits
are approached to be merged.
So with 5 commits you'll got 3
commits as a result.  

-----

Conditions
----------

To realise what commits to merge, your
git history should follow next conditions:

* You've got ONLY one branch (master)
* Time difference between 2 commits
should be less than 1 hour
* Author of commits should be the same
* In commits should be mentioned that
only one file was changed

Example:  
commit_1: branch: master, time: 9:00 am, author: Alex, changes: script.py  
commit_2: branch: master, time: 9:20 am, author: Alex, changes: script.py  
So, this to commits could be merged.

-----

Installation
------------

Download repository from GitHub, NOT clone.
Press button to download. You can find
this button to the right of the field
with HTTP/SSH address of this repository.  

Then put downloaded template with script
files to your work repository with .git file:  
project/--  
        |-file1  
        |-file2  
        |-.git  
        |-**git-script/**  

-----

Run script
----------

Move to script directory:

```text
$cd ./project/git-script
```  

Run script file:

```text
$source script.sh
```  
