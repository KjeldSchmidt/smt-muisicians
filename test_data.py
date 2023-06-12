def group_index_issue():
    rooms = [
        [3, ['wheelchair']],
        [3, ['piano']]
    ]

    musicians_groups = [
        [[0, 1], ['wheelchair']],
        [[1, 3], ['piano']],
        [[2, 3], ['piano']],
        [[0, 2], ['wheelchair']]
    ]
    person_count = 4
    timeslots_count = 8
    number_of_rehearsals = 2

    return rooms, musicians_groups, person_count, timeslots_count, number_of_rehearsals


def base_data():
    person_count = 20
    timeslots_count = 10
    number_of_rehearsals = 3

    rooms = [
        (20, ["ConcertHall", "Drumkit", "Piano", "Accessible"]),
        (5, ["Piano"]),
        (5, ["Drumkit"]),
        (3, ["Accessible"]),
        (3, ["Piano"]),
        (1, []),
        (2, []),
        (3, []),
        (4, []),
        (5, []),
        (6, []),
        (7, []),
        (8, []),
        (9, []),
    ]

    musicians_groups = [
        ((0, 1, 2), ["Accessible"]),
        # ((1, 2, 3), ["Accessible"]),
        # ((2, 3, 4), ["Piano", "Accessible"]),
        ((3, 4, 5), ["Piano"]),
        # ((4, 5, 6), ["Piano"]),
        # ((5, 6, 7), ["Piano"]),
        # ((6, 7, 8), ["Piano"]),
        # ((7, 8, 9), ["Piano"]),
        # ((8, 9, 10), []),
        # ((9, 10, 11), []),
        ((0, 1, 2, 3, 4), ["Piano", "Accessible"]),
        # ((5, 6, 7, 8, 9), ["Piano"]),
        # ((10, 11, 12, 13, 14, 15), []),
        # ((15, 16, 17, 18, 19), []),
    ]

    return rooms, musicians_groups, person_count, timeslots_count, number_of_rehearsals
