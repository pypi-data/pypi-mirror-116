import sys
import os
import re
import argparse
from math import log10


def has_ext(filename, ext):
    """
    >>> has_ext('test.mp3',['opus','mp3','aac'])
    True
    >>> has_ext('test.mp4',['opus','mp3','aac'])
    False
    >>> has_ext('test.opus.gz',['opus','mp3','aac'])
    False
    >>> has_ext('test.1.OPUS',['opus','mp3','aac'])
    True
    """

    return filename.split(".")[-1].lower() in ext


def is_audio(f):
    return has_ext(f, ["opus", "mp3", "aac", "m4a", "ogg"])


def is_video(f):
    return has_ext(f, ["mp4", "avi", "mov", "mkv", "webm"])


def is_image(f):
    return has_ext(f, ["png", "jpeg", "jpg"])


def is_media(f):
    return is_audio(f) or is_video(f) or is_image()


def normalize_date(name):
    """
    >>> normalize_date("2010-10-20 04.05.06.jpg")
    '2010-10-20T040506.jpg'

    >>> normalize_date("1999-05-01 11.22.33 name.jpg")
    '1999-05-01T112233 name.jpg'
    """

    m = re.search(
        "^"
        "(?P<year>\d{4})[\-\.]?"
        "(?P<month>\d{2})[\-\.]?"
        "(?P<day>\d{2})[Tt \-\.]?"
        "(?P<hour>\d{2})[\.\:\- ]?"
        "(?P<minute>\d{2})[\.\:\- ]?"
        "(?P<second>\d{2})",
        name,
    )

    if m:
        name = name.replace(
            m.group(0),
            f"{m['year']}-{m['month']}-{m['day']}T{m['hour']}{m['minute']}{m['second']}",
        )

    return name


def normalize(filename):
    """
    Normalize to lowercase separated by dashes

    Convert embedded dates to ISO 8601 format

    >>> normalize('Test 1.txt')
    'test-1.txt'
    >>> normalize('another-TEst_file.mp4')
    'another-test-file.mp4'
    >>> normalize('Linkin Park - In the End -.opus')
    'linkin-park-in-the-end.opus'
    >>> normalize('calvin&hobbes.pdf')
    'calvin-hobbes.pdf'
    >>> normalize('2019-10-11 07.08.09[family photo].jpg')
    '2019-10-11T070809-family-photo.jpg'
    >>> normalize('2010-01-12 03.04.05 some nature.jpg')
    '2010-01-12T030405-some-nature.jpg'
    >>> normalize('2010-01-12T030405-some-nature.jpg')
    '2010-01-12T030405-some-nature.jpg'
    >>> normalize('2010-01-12 03.04.05.jpg')
    '2010-01-12T030405.jpg'
    """

    path = filename.split("/")[:-1]
    filename = filename.split("/")[-1]

    filename = filename.lower().replace("_", "-").replace(" ", "-").replace("–", "-")

    filename = normalize_date(filename)

    if is_audio(filename):
        filename = re.sub(r"[\(\[].*?[\)\]]", "", filename)  # Remove parentheticals

    filename = re.sub("[\[\(\)\]\-\&]+", "-", filename)
    words = filename.split("-")

    filename = "-".join(words)

    filename = re.sub(r"[\'\!\:\,]", "", filename)

    filename = re.sub(r"-+\.+", ".", filename)

    filename = re.sub(r"\-+", "-", filename)

    return "/".join(path + [filename])


def normalize_scene(filename):
    """
    Normalize a file name roughly following scene rules

    >>> normalize_scene('Test 1.txt')
    'Test.1.txt'
    >>> normalize_scene('another-TEst_file.mp4')
    'Another.Test.File.mp4'
    >>> normalize_scene('Linkin Park - In the End -.opus')
    'Linkin.Park.In.the.End.opus'
    >>> normalize_scene('Linkin Park - IN THE END -.opus')
    'Linkin.Park.in.the.End.opus'
    >>> normalize_scene('2019-10-11 07.08.09[family photo].jpg')
    '2019.10.11T070809.Family.Photo.jpg'
    >>> normalize_scene('2010-01-12 03.04.05 trees and nature.jpg')
    '2010.01.12T030405.Trees.and.Nature.jpg'
    >>> normalize_scene('2010-01-12T030405-trees-in-forest.jpg')
    '2010.01.12T030405.Trees.in.Forest.jpg'
    >>> normalize_scene('2010-01-12 03.04.05.jpg')
    '2010.01.12T030405.jpg'
    >>> normalize_scene('calvin&hobbes.pdf')
    'Calvin.and.Hobbes.pdf'
    >>> normalize_scene('THE_MATRIX.mkv')
    'The.Matrix.mkv'
    >>> normalize_scene('makefile')
    'makefile'
    >>> normalize_scene('my-project.c')
    'my-project.c'
    """

    path = filename.split("/")[:-1]
    filename = filename.split("/")[-1]

    if re.match(
        "(makefile|readme.md|license.md|requirements.txt|.*.py|.*.c)$", filename
    ):
        return filename

    filename = normalize_date(filename)

    if is_audio(filename):
        filename = re.sub(r"[\(\[].*?[\)\]]", "", filename)  # Remove parentheticals

    filename = filename.replace("&", ".and.")

    filename = re.sub(r"[\'\!\:\,\[\(\)\]\-\+\.\_\- ]+", ".", filename)

    parts = filename.split(".")
    keep_lower = {
        "this",
        "upon",
        "altogether",
        "whereunto",
        "across",
        "between",
        "and",
        "if",
        "as",
        "over",
        "above",
        "afore",
        "inside",
        "like",
        "besides",
        "on",
        "atop",
        "about",
        "toward",
        "by",
        "these",
        "for",
        "into",
        "beforehand",
        "unlike",
        "until",
        "in",
        "aft",
        "onto",
        "to",
        "vs",
        "amid",
        "towards",
        "afterwards",
        "notwithstanding",
        "unto",
        "next",
        "while",
        "including",
        "thru",
        "a",
        "down",
        "after",
        "with",
        "afterward",
        "or",
        "those",
        "but",
        "whereas",
        "versus",
        "without",
        "off",
        "among",
        "because",
        "some",
        "against",
        "before",
        "around",
        "of",
        "under",
        "that",
        "except",
        "at",
        "beneath",
        "out",
        "amongst",
        "the",
        "from",
        "per",
        "mid",
        "behind",
        "along",
        "outside",
        "beyond",
        "up",
        "past",
        "through",
        "beside",
        "below",
        "during",
    }

    parts = [
        p.lower() if p.lower() in keep_lower and p.title() != p else p.title()
        for p in parts
    ]
    parts[-1] = parts[-1].lower()
    parts[0] = parts[0].title()
    filename = ".".join(parts)

    return "/".join(path + [filename])


def zfill(i, maxval):
    """
    Zero fills a number with enough zeroes to ensure all items are the same
    length

    >>> zfill(1, 299)
    '001'

    >>> zfill(0, 999)
    '000'

    >>> zfill(3, 10)
    '03'

    >>> zfill(101, 48591)
    '00101'
    """

    return str(i).zfill(int(log10(maxval) + 1))


def get_numeric_name(filename, i, maxval):
    """
    Returns numeric name for a file

    >>> get_numeric_name("test/img.jpg", 13, 356)
    'test/013.jpg'

    >>> get_numeric_name("test/next/photo.jpg", 4, 7)
    'test/next/4.jpg'

    >>> get_numeric_name("test/dir/readme", 113, 9987)
    'test/dir/0113'

    >>> get_numeric_name("test/doc.md", 2, 14)
    'test/02.md'

    >>> get_numeric_name("doc.md", 6, 101)
    '006.md'
    """

    path = filename.split("/")[:-1]
    filename = filename.split("/")[-1]
    extension = filename.split(".")[-1]

    new_name = zfill(i, maxval)

    if extension != filename:
        new_name += "." + extension

    return "/".join(path + [new_name])


def main():
    ap = argparse.ArgumentParser(description="Rename files to a standard format")
    ap.add_argument("files", nargs="+", help="List of files")
    ap.add_argument(
        "--numeric",
        "-n",
        action="store_true",
        help="Rename file numerically after sorting alphabetically",
    )
    ap.add_argument(
        "--reverse",
        "-r",
        action="store_true",
        help="Reverse sort order prior to renaming",
    )
    ap.add_argument(
        "--scene",
        "-s",
        action="store_true",
        help="Rename using scene rules",
    )
    args = ap.parse_args()

    files = sorted(args.files, reverse=args.reverse)

    for i, filename in enumerate(files):
        if args.numeric:
            os.rename(filename, get_numeric_name(filename, i, len(files)))
        else:
            os.rename(filename, normalize_scene(filename) if args.scene else normalize(filename))

if __name__ == '__main__':
    main()
