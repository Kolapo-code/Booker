import hashlib


def set_dict(initial_list, result_dict):
    """A function that sets a dictionary from a given list of objects."""
    result_dict.update(
        dict(
            zip(
                map(
                    lambda item: f"{item.__class__.__name__}.{item.id}",
                    initial_list,
                ),
                initial_list,
            )
        )
    )


def hash_to_sha256(string):
    """A function that hashes a given string to sha1."""
    hashed_string = hashlib.sha256(string.encode()).hexdigest().lower()
    return hashed_string
