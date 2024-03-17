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
