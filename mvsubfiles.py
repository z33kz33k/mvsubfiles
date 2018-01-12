#!/usr/bin/env python3

import argparse
import os
import shutil


class Mover:
    """
    Moves matching files from subdirectories of provided directory to new destination

    Useful e.g. for moving videos of an YT playlist that were earlier batch-downloaded with JDownloader
    """

    def __init__(self, src, dst, *matches):
        self.src_dir = src
        self.dst_dir = dst
        if len(matches) > 1:
            self.matches = matches
            self.match = None
        else:
            self.matches = None
            self.match = matches[0]
        self.counter = 0

    def start(self):
        home_list = os.listdir(self.src_dir)
        for folder in home_list:
            src = self.src_dir + "/" + folder
            src_list = os.listdir(src)
            if self.match is not None:
                for file in src_list:
                    if self.match in file:
                        self.move_subfile(src, self.dst_dir, file)
            else:
                matches = self.matches[:]
                for file in src_list:
                    for match in matches:
                        if match in file:
                            self.move_subfile(src, self.dst_dir, file)
                            matches.remove(match)
                            break

        print("*****\nMoved {} files".format(self.counter))

    def move_subfile(self, src, dst, subfile):
        src_path = src + "/" + subfile
        shutil.move(src_path, dst)
        self.counter += 1
        print("Moving a file: '{}' to new destination: '{}'".format(src_path, dst))


def get_argsparser():
    """Creates and returns an argsparser"""
    parser = argparse.ArgumentParser(description="Move matching files from subdirs of src_dir to dst_dir")
    parser.add_argument("src_dir", help="full path to directory containing subdirs with files to be moved")
    parser.add_argument("dst_dir", help="full path to required destination")
    parser.add_argument("matches", nargs=argparse.REMAINDER, help="each file containing any of provided matches in its name will be moved")
    return parser


def main():
    """Runs the script"""
    parser = get_argsparser()
    args = parser.parse_args()

    m = Mover(args.src_dir, args.dst_dir, *args.matches)
    m.start()


if __name__ == "__main__":
    main()
