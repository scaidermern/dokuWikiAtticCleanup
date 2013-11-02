#!/usr/bin/python
#
# Copyright 2013 Alexander Heinlein <alexander.heinlein@web.de>
# License: GPLv3
#

from datetime import datetime
import os

class DokuWikiAtticCleanup:
    """Cleanup DokuWiki's attic directory by removing old page revisions
    
    DokuWiki stores its wiki page histories inside the data/attic/ directory
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
    
    Note: Even after deleting the old revisions they still get listed when
    clicking the 'Old Revisions' button. This is due to the fact that
    DokuWiki additionally records the history in separate files located at
    data/meta/<namespace>.changes which won't get modified by this script.
    
    Warning: Don't use this script if you want to keep your history!
    """

    @staticmethod
    def cleanup(dir, max_days, dry_run=False, verbose=False):
        """Cleanup DokuWiki's attic directory by removing old page revisions
        
        Args:
            dir:      DokuWiki root directory (must contain a 'data/attic' dir).
            max_days: Maximum age in days.
            verbose:  Print detailed information about each file.
            dry_run:  Dry-run, just show which files would have been deleted.
        
        Raises:
            ValueError: If the specified directory doesn't contain a 'data/attic' dir
        """
        
        attic = dir + "/data/attic"
        if not os.path.isdir(attic):
            raise ValueError("'%s' does not look like the dokuwiki root directory, cannot find directory '%s'" % (dir, attic))
            
        now = datetime.now()

        for root, dirs, files in os.walk(attic):
            if verbose:
                print "processing directory %s" % root
            for filename in files:
                if not filename.endswith(".txt.gz"):
                    continue
                parts = filename.split(".")
                if len(parts) < 4:
                    print "error: file with unexpected name: '%s/%s'" % (root, filename)
                
                time_epoch = int(parts[-3])
                time = datetime.fromtimestamp(time_epoch)
                
                age_days = (now - time).days
                if age_days <= max_days:
                    if verbose:
                        print "skipping file %s/%s with an age of %s days" % (root, filename, age_days)
                    continue
                else:
                    if verbose or dry_run:
                        print "deleting file %s/%s with an age of %s days" % (root, filename, age_days)
                    if not dry_run:
                        os.remove("%s/%s" % (root, filename))

if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Cleanup DokuWiki's attic directory by removing old page revisions")
    parser.add_argument("age",             help="maximum age in days", type=int)
    parser.add_argument("-d", "--dir",     help="DdokuWiki root directory (must contain a 'data/attic' dir), uses the current working directory if omitted")
    parser.add_argument("-n", "--no-act",  help="dry-run, just show which files would have been deleted", action="store_true")
    parser.add_argument("-v", "--verbose", help="print detailed information about each file", action="store_true")
    args = parser.parse_args()
    
    if args.dir == None:
        args.dir = os.getcwd()
    
    DokuWikiAtticCleanup.cleanup(dir=args.dir,
                                 max_days=args.age,
                                 dry_run=args.no_act,
                                 verbose=args.verbose)
