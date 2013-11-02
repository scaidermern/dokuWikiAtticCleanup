dokuWikiAtticCleanup
====================

Cleanup [DokuWiki](https://www.dokuwiki.org/dokuwiki)'s `attic` directory by removing old page revisions.

DokuWiki stores its wiki page histories inside the `data/attic/` directory
as compressed text files. Over time this directory will contain more and
more files because every single page edit creates a new revision file and
there is no automatic cleanup mechanism. While the total directory size
won't grow significantly due to compression the number of files can
become annoying and will lead to a significantly slowdown of backups and
similar processes.

This script will walk recursively through the attic directory and remove
every page revision older than the specified number of days.

For more information about the attic directory read the official
documentation at https://www.dokuwiki.org/attic

Note
----
Even after deleting the old revisions they still get listed when
clicking the `Old Revisions` button. This is due to the fact that
DokuWiki additionally records the history in separate files located at
`data/meta/<namespace>.changes` which won't get modified by this script.

Warning
-------
Don't use this script if you want to keep your history!

Usage
-----
Just call this script inside the DokuWiki root directory and pass the
maximum age in days. It might be a good idea to start a dry-run first by
passing option `-n`.

If you don't have direct access to the webserver directory then you can
use [curlftpfs](http://curlftpfs.sourceforge.net/) to mount it locally.

    positional arguments:
      age                maximum age in days

    optional arguments:
      -h, --help         show this help message and exit
      -d DIR, --dir DIR  DokuWiki root directory (must contain a 'data/attic'
                         dir), uses the current working directory if omitted
      -n, --no-act       dry-run, just show which files would have been deleted
      -v, --verbose      print detailed information about each file
