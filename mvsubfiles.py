#!/usr/bin/env python3

import argparse
import os
import shutil


class Mover:
    """
    Moves matching files from subdirectories of provided directory to new destination.

    Useful e.g. for moving videos of an YT playlist that were earlier batch-downloaded with JDownloader.
    """
    @staticmethod
    def validate_args(src, dst, matches):
        if not os.path.exists(src):
            raise ValueError("Invalid source directory")
        if not os.path.exists(dst):
            raise ValueError("Invalid destination directory")
        if len(matches) < 0:
            raise ValueError("No pattern to match")

    def __init__(self, src, dst, *matches):
        self.validate_args(src, dst, matches)
        self.src_dir = src
        self.dst_dir = dst
        self.matches = list(matches) if len(matches) > 1 else None
        self.match = matches[0] if len(matches) == 1 else None
        self.counter = 0

    def start(self):
        home_list = os.listdir(self.src_dir)
        for directory in home_list:
            src = self.src_dir + "/" + directory
            if os.path.samefile(src, self.dst_dir):  # filter out the destination from the source
                continue
            print("****src:", src)
            src_list = os.listdir(src)

            if self.match is not None:
                for filename in src_list:
                    if self.match in filename:
                        self.move_subfile(src, self.dst_dir, filename)
            else:
                for match in self.matches:
                    src_list = os.listdir(src)
                    for filename in src_list:
                        if match in filename:
                            self.move_subfile(src, self.dst_dir, filename)

        if self.counter == 1:
            print("*****\nMoved {} file".format(self.counter))
        else:
            print("*****\nMoved {} files".format(self.counter))

    def move_subfile(self, src, dst, subfile):
        src_path = src + "/" + subfile
        print("dst:", dst)
        print("src_path:", src_path)
        if os.path.isfile(dst + "/" + subfile):  # circumvent shutil 'already exists' error
            shutil.copy2(src_path, dst)
            os.remove(src_path)
        else:
            shutil.move(src_path, dst)
        self.counter += 1
        print("Moving a file: '{}' to new destination: '{}'".format(src_path, dst))


def get_argsparser():
    """Creates and returns an argsparser."""
    parser = argparse.ArgumentParser(description="Move matching files from subdirs of src_dir to dst_dir")
    parser.add_argument("src_dir", help="full path to directory containing subdirs with files to be moved")
    parser.add_argument("dst_dir", help="full path to required destination")
    parser.add_argument("matches", nargs=argparse.REMAINDER, help="each file containing any of provided matches in its name will be moved")
    return parser


def main():
    """Runs the script."""
    parser = get_argsparser()
    args = parser.parse_args()

    m = Mover(args.src_dir, args.dst_dir, *args.matches)
    m.start()


if __name__ == "__main__":
    main()
