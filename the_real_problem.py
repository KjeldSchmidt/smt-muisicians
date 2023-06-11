import json
import itertools

from z3 import *

person_count = 20
timeslots_count = 10
number_of_rehearsals = 3

rooms = [
    (20, ["ConcertHall", "Drumkit", "Piano", "Accessible"]),
    (5, ["Piano"]),
    (5, ["Drumkit"]),
    (3, ["Accessible"]),
    (3, ["Piano"]),
    (5, []),
    (3, []),
    (3, []),
    (3, []),
    (3, []),
    (3, []),
    (3, []),
    (3, []),
    (3, []),
    (3, []),
    (3, []),
    (3, []),
    (3, []),
]


musicians_groups = [
    ((0, 1, 2), ["Accessible"]),
    ((1, 2, 3), ["Accessible"]),
    ((2, 3, 4), ["Piano", "Accessible"]),
    ((3, 4, 5), ["Piano"]),
    ((4, 5, 6), ["Piano"]),
    ((5, 6, 7), ["Piano"]),
    ((6, 7, 8), ["Piano"]),
    ((7, 8, 9), ["Piano"]),
    ((8, 9, 10), []),
    ((9, 10, 11), []),
    ((0, 1, 2, 3, 4), ["Piano", "Accessible"]),
    ((5, 6, 7, 8, 9), ["Piano"]),
    ((10, 11, 12, 13, 14, 15), []),
    ((15, 16, 17, 18, 19), []),
]

raw_attributes: set[str] = set()
for room in rooms:
    raw_attributes.update(room[1])

# Begin modelling

solver = Solver()

# Declare sorts and constants for:
# Timeslots (simple)

AttributeSort = DeclareSort("Attribute")
AttributeSetSort = SetSort(AttributeSort)

attribute_consts = {}
for attribute in raw_attributes:
    new_attribute = Const(attribute, AttributeSort)
    for prev_attribute in attribute_consts.values():
        solver.add(new_attribute != prev_attribute)
    attribute_consts[attribute] = new_attribute


# Declare people
PersonSort = DeclareSort("Person")
people = []
for person_index in range(person_count):
    new_person = Const(f"Person {person_index}", PersonSort)

    # Define person to be distinct from every other previously defined person
    for prev_person in people:
        solver.add(new_person != prev_person)

    people.append(new_person)

# Declare rooms
RoomSort = DeclareSort("Room")
rooms_consts = []

RoomSize = Function("room_size", RoomSort, IntSort())
RoomAttributes = Function("room_attributes", RoomSort, AttributeSetSort)
for idx, room in enumerate(rooms):
    new_room = Const(f"Room {idx}", RoomSort)
    rooms_consts.append(new_room)

    # Add room size
    solver.add(RoomSize(new_room) == room[0])

    # Add room attributes
    room_attributes = EmptySet(AttributeSort)
    for attribute in room[1]:
        room_attributes = SetAdd(room_attributes, attribute_consts[attribute])
    solver.add(RoomAttributes(new_room) == room_attributes)


GroupSort = DeclareSort("Group")
GroupSize = Function("group_size", GroupSort, IntSort())
GroupMembers = Function("group_members", GroupSort, SetSort(PersonSort))
GroupAttributes = Function("group_attributes", GroupSort, AttributeSetSort)
no_group_const = Const("No group", GroupSort)
solver.add(GroupSize(no_group_const) == 0)
solver.add(GroupAttributes(no_group_const) == EmptySet(AttributeSort))
solver.add(GroupMembers(no_group_const) == EmptySet(PersonSort))

groups_consts = []
for idx, group in enumerate(musicians_groups):
    new_group = Const(f"Group {idx}", GroupSort)

    # Distinct groups
    for prev_group in groups_consts:
        solver.add(new_group != prev_group)

    groups_consts.append(new_group)

    # Group Size
    solver.add(GroupSize(new_group) == len(group[0]))

    # Add group attributes
    group_attributes = EmptySet(AttributeSort)
    for attribute in group[1]:
        group_attributes = SetAdd(group_attributes, attribute_consts[attribute])
    solver.add(GroupAttributes(new_group) == group_attributes)

    # Add group members
    group_members = EmptySet(PersonSort)
    for member in group[0]:
        group_members = SetAdd(group_members, people[member])
    solver.add(GroupMembers(new_group) == group_members)

GroupSetSort = SetSort(GroupSort)
setOfGroups = EmptySet(GroupSort)
for group in groups_consts:
    setOfGroups = SetAdd(setOfGroups, group)


# Declare Timeslot
TimeslotSort = DeclareSort("Timeslot")
timeslots_consts = []
for timeslot_index in range(timeslots_count):
    new_timeslot = Const(f"Timeslot {timeslot_index}", TimeslotSort)

    # Define timeslot to be distinct from every other previously defined timeslot
    for prev_timeslot in timeslots_consts:
        solver.add(new_timeslot != prev_timeslot)

    timeslots_consts.append(new_timeslot)


# solver.add(group_1 == SetAdd(SetAdd(EmptySet(PersonSort), people[0]), people[2]))
# solver.add(group_2 == SetAdd(SetAdd(EmptySet(PersonSort), people[1]), people[1]))
# solver.add(SetIntersect(group_1, group_2) == EmptySet(PersonSort))


Timeslot_room_to_group = Function("Timeslot and Room to Group", TimeslotSort, RoomSort, GroupSort)
Timeslot_group_to_room = Function("Timeslot and Group to Room", TimeslotSort, GroupSort, RoomSort)


# No group can play in two rooms at the same time
for room_a, room_b in itertools.combinations(rooms_consts, 2):
    for timeslots_const in timeslots_consts:
        # A group does not play twice at the same time
        """solver.add(
            (Timeslot_room_to_group(timeslots_const, room_a) != Timeslot_room_to_group(timeslots_const, room_b))
        )"""
        solver.add(Implies(
            Timeslot_room_to_group(timeslots_const, room_a) == Timeslot_room_to_group(timeslots_const, room_b),
            Timeslot_room_to_group(timeslots_const, room_a) == no_group_const
        ))

# Any assigned group must exist or be the NoGroup
for timeslots_const in timeslots_consts:
    allowed_results_set = SetAdd(setOfGroups, no_group_const)
    for room_const in rooms_consts:
        result = Timeslot_room_to_group(timeslots_const, room_const)
        result_set = SetAdd(EmptySet(GroupSort), result)
        solver.add(SetIntersect(allowed_results_set, result_set) != EmptySet(GroupSort))


# for time slot t, every group size is smaller than it's room size
for timeslots_const in timeslots_consts:
    for room_const in rooms_consts:
        result = Timeslot_room_to_group(timeslots_const, room_const)
        solver.add(GroupSize(result) <= RoomSize(room_const))


# for time slot t, every room has at least all attributes of the assigned group
# for time slot t, each group should be pairwise distinct
# (alternative: the set of the union of all groups is equal in size to the sum of all group sizes)

# over all time slots, each group is assigned to the concert hall at least once


assert solver.check() == sat

model = solver.model()
for thing in model:
    if thing.name() != "Timeslot and Room to Group":
        print(f"{thing} = {model.get_interp(thing)}")
    else:
        print(f"{thing} =")
        for line in model.get_interp(thing).as_list():
            print(f"{line}")
