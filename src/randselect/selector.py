import random


def available_items(items, used=None):
    """Items not yet in `used`, preserving order."""
    used = used or set()
    return [item for item in items if item not in used]


def random_selection(n_list, q_list, rng=random, used_names=None, used_questions=None):
    names_pool = available_items(n_list, used_names)
    questions_pool = available_items(q_list, used_questions)

    chosen_name = rng.choice(names_pool)
    chosen_question = rng.choice(questions_pool)

    return (chosen_name, chosen_question)