from z3 import *

solver = Solver()
Person = DeclareSort("Person")
Room = DeclareSort("Room")
Time = DeclareSort("Time")

PersonLocation = Function("person_location", Person, Time, Room)

laura = Const('Laura', Person)
beeke = Const('Beeke', Person)

_3_pm = Const('3pm', Time)
_2_pm = Const('2pm', Time)

pianoRoom = Const('PianoRoom', Room)
mainStage = Const('MainStage', Room)

solver.add(pianoRoom != mainStage)

solver.add(PersonLocation(laura, _2_pm) == mainStage)
solver.add(PersonLocation(laura, _3_pm) == pianoRoom)

assert solver.check() == sat

model = solver.model()

print(solver.model())

solver.add(PersonLocation(laura, _3_pm) == mainStage)

assert solver.check() == unsat
