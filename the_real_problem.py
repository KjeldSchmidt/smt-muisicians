from enum import Enum, auto

from z3 import *

person_count = 20
rooms_count = 10
timeslots_count = 10
number_of_rehearsals = 3


class Attribute(Enum):
    Piano = auto()
    Accessible = auto()
    Drumkit = auto()
    ConcertHall = auto()


rooms = [
    (20, [Attribute.ConcertHall, Attribute.Drumkit, Attribute.Piano, Attribute.Accessible]),
    (3, [Attribute.Piano]),
    (5, [Attribute.Piano]),
    (5, [Attribute.Drumkit]),
    (3, [Attribute.Accessible]),
    (3, []),
    (3, []),
    (3, []),
    (5, []),
    (3, []),
]

musicians_groups = [
    ((0, 1, 2), [Attribute.Accessible]),
    ((1, 2, 3), [Attribute.Accessible]),
    ((2, 3, 4), [Attribute.Piano, Attribute.Accessible]),
    ((3, 4, 5), [Attribute.Piano]),
    ((4, 5, 6), [Attribute.Piano]),
    ((5, 6, 7), [Attribute.Piano]),
    ((6, 7, 8), [Attribute.Piano]),
    ((7, 8, 9), [Attribute.Piano]),
    ((8, 9, 10), []),
    ((9, 10, 11), []),
    ((0, 1, 2, 3, 4), [Attribute.Piano, Attribute.Accessible]),
    ((5, 6, 7, 8, 9), [Attribute.Piano]),
    ((10, 11, 12, 13, 14, 15), []),
    ((15, 16, 17, 18, 19), []),
]

# Begin modelling

solver = Solver()

# Declare sorts and constants for:
# Timeslots (simple)

AttributeSort = DeclareSort("Attribute")
AttributeSetSort = SetSort(AttributeSort)

attributes = {}
for attribute in Attribute:
    new_attribute = Const(attribute.name, AttributeSort)
    for prev_attribute in attributes.values():
        solver.add(new_attribute != prev_attribute)
    attributes[attribute] = new_attribute


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
        room_attributes = SetAdd(room_attributes, attributes[attribute])
    solver.add(RoomAttributes(new_room) == room_attributes)


GroupSort = DeclareSort("Group")
GroupSize = Function("group_size", GroupSort, IntSort())
GroupMembers = Function("group_members", GroupSort, SetSort(PersonSort))
GroupAttributes = Function("group_attributes", GroupSort, AttributeSetSort)

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
        group_attributes = SetAdd(group_attributes, attributes[attribute])
    solver.add(GroupAttributes(new_group) == group_attributes)

    # Add group members
    group_members = EmptySet(PersonSort)
    for member in group[0]:
        group_members = SetAdd(group_members, people[member])
    solver.add(GroupMembers(new_group) == group_members)


# Declare Timeslot
TimeslotSort = DeclareSort("Timeslot")
timeslots = []
for timeslot_index in range(timeslots_count):
    new_timeslot = Const(f"Timeslot {timeslot_index}", TimeslotSort)

    # Define timeslot to be distinct from every other previously defined timeslot
    for prev_timeslot in timeslots:
        solver.add(new_timeslot != prev_timeslot)

    timeslots.append(new_timeslot)



# group_1 = Const("Group 1", Group)
# group_2 = Const("Group 2", Group)
#
#
# solver.add(group_1 == SetAdd(SetAdd(EmptySet(PersonSort), people[0]), people[2]))
# solver.add(group_2 == SetAdd(SetAdd(EmptySet(PersonSort), people[1]), people[1]))
# solver.add(SetIntersect(group_1, group_2) == EmptySet(PersonSort))
solver.add()


assert solver.check() == sat

print(solver.model())



# Declare Sort for room-group-pair
# Declare Sort for set of room-group-pair

# define mapping function from time slot to {room, group}

# Start defining constraints:
# All persons, rooms, groups and time slots are distinct

# for time slot t, the set can only contain each room at most once
# for time slot t, every group size is smaller than it's room size
# for time slot t, every room has at least all attributes of the assigned group
# for time slot t, each group should be pairwise distinct
# (alternative: the set of the union of all groups is equal in size to the sum of all group sizes)

# over all time slots, each group is assigned to the concert hall at least once
