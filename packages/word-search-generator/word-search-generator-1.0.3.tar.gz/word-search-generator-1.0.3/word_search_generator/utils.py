import string

from . import config


def cleanup_input(words: str) -> set:
    """Cleanup provided input string. Removing spaces
    one-letter words, and words with punctuation.

    Args:
        words (str): String of words separated by commas, spaces, or new lines.

    Raises:
        TypeError: A string was not provided.
        ValueError: No proper words were provided.

    Returns:
        set: Words to be placed in the puzzle.
    """
    if not isinstance(words, str):
        raise TypeError(
            "Words must be a string separated by spaces, commas, or new lines"
        )
    # remove new lines
    words = words.replace("\n", ",")
    # remove excess spaces and commas
    words = ",".join(words.split(" ")).split(",")
    # iterate through all words and pick first set that match criteria
    word_list = set()
    for word in words:
        if len(word_list) > config.max_puzzle_words:
            break
        if len(word) > 1 and not contains_punctuation(word):
            word_list.add(word.upper())
    # if no words were left raise exception
    if not word_list:
        raise ValueError("Use words longer than one-character and without punctuation.")
    return word_list


def contains_punctuation(word):
    """Check to see if puncuation is present in the provided string."""
    return any([True if c in string.punctuation else False for c in word])


def stringify(puzzle: list, tabs: bool = False):
    """Convert a list of list into a string separated by either spaces or tabs.

    Args:
        puzzle (list): The current puzzle state.
        tabs (bool, optional): Use tabs between characters.

    Returns:
        [type]: A string with of the current puzzle.
    """
    string = ""
    spacer = "\t" if tabs else " "
    for line in puzzle:
        string += spacer.join(line) + "\n"
    return string.strip("\n")


def replace_right(s: str, target: str, replacement: str, replacements: int = 1) -> str:
    """Replace `target` with `replacement` from the right size of the string.

    Args:
        s (str): A string to do replacement on.
        target (str): String to be replaced.
        replacement (str): New string to insert.
        replacements (int, optional): Number of times replace. Defaults to 1.

    Returns:
        str: Updated string with replacement(s).
    """
    return replacement.join(s.rsplit(target, replacements))


def get_level_dirs_str(level: int) -> str:
    """Return all pozzible directions for specified level."""
    return replace_right(", ".join(config.level_dirs[level]), ", ", ", and ")


def get_word_list_str(key: dict) -> str:
    """Return all placed puzzle words as a list."""
    return ", ".join([k for k in sorted(key.keys())])


def get_answer_key_str(key: dict) -> str:
    """Return a easy to read answer key for display/export."""
    keys = []
    for k in sorted(key.keys()):
        direction = key[k]["direction"]
        coords = (key[k]["start"][0] + 1, key[k]["start"][1] + 1)
        keys.append(f"{k} {direction} @ {coords}")
    return ", ".join(keys)
