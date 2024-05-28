import os
import sys
import zlib

# At its heart, git is a key value store.
# Git stores compressed data in blob and puts metadata in header.
# The blobs are stored in objects directory.
# The first two characters of the blob becomes the directory name and the rest is the file.

"""
.git
├── HEAD
├── config
├── description
├── hooks
│   ├── applypatch-msg.sample
│   ├── commit-msg.sample
│   ├── fsmonitor-watchman.sample
│   ├── post-update.sample
│   ├── pre-applypatch.sample
│   ├── pre-commit.sample
│   ├── pre-merge-commit.sample
│   ├── pre-push.sample
│   ├── pre-rebase.sample
│   ├── pre-receive.sample
│   ├── prepare-commit-msg.sample
│   ├── push-to-checkout.sample
│   ├── sendemail-validate.sample
│   └── update.sample
├── info
│   └── exclude
├── objects
│   ├── info
│   └── pack
└── refs
    ├── heads
    └── tags
"""


def main():

    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        # All part versions of files compressed using SHA1 hash
        os.mkdir(".git/objects")
        # stores references(pointers). refs/heads contains pointers to branches and refs/tags contains pointers to tags.
        os.mkdir(".git/refs")
        # HEAD -> This file contains a reference to the currently checked out branch.
        # this is pointing to refs/heads folder.
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file":
        # NOTE: Blobs only store the contents of a file, not its name or permissions.
        # All Git objects are identifiable by a 40-character SHA-1 hash, also known as the "object hash".
        # Git objects are stored in the .git/objects directory. The path to an object is derived from its hash.
        # Each Git Blob is stored as a separate file in the .git/objects directory. The file contains a header and the contents of the blob object, compressed using Zlib.
        blob_hash = sys.argv[3]
        folder_name = blob_hash[0:2]
        file_name = blob_hash[2:]
        with open(f"./.git/objects/{folder_name}/{file_name}", "rb") as blob_file:
            content = zlib.decompress(blob_file.read())
            # blob <size>\0<content>
            required_content = (content.split(b"\0"))[1]
            print(required_content.decode(), end="")
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
