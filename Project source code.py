import prettytable as prettytable
import random as rnd
POPULATION_SIZE = 9
NUM_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1
class Data:
    ROOMS = [["R1",45],["R3",35]]
    LECTURE_TIMES =[["CSC1","MWF 09:00 - 10:00"],
                   ["CSC2","MWF 10:00 - 11:00"],
                   ["CSC3","TTH 09:00 - 10:30"],
                   ["CSC4","TTH 10:30 - 12:00"]]
    LECTURERS = [["I1", "Dr James Web"],
                ["I2", "Mr JMike Brown"],
                ["I3", "Dr Steve Dav"],
                ["I4", "Mrs Jane Doe"]]
    def __init__(self):
        #self._rooms = [];
        self._rooms = [[101, 50], [102, 100], [103, 30], [104, 80], [105, 45], [106, 25], [107, 120], [108, 35], [109, 60], [110, 75]]
        self._lectureTimes = []; self._lecturers = []
        if self._rooms:
            #for i in range(0, len(self._rooms)):
                #self._rooms[i] = Room(self._rooms[i][0], self._rooms[i][1])
            for i in range(len(self._rooms)):
                room_name, room_capacity = self._rooms[i]
                self._rooms.append(Room(room_name, room_capacity))


        for i in range(0, len(self.ROOMS)):
            #self._rooms.append(Room(self.ROOMS[i][0], self.Rooms[i][1]))
            self._rooms.append(Room(self._rooms[i][0], self._rooms[i][1]))

        #for i in range(0, len(self.LECTURE_TIMES)):
            #self.lectureTime.append(LECTURETIME(self.LECTURE_TIMES[i][0], self.LECTURE_TIMES[i][1]))
        #for i in range(len(self.LECTURE_TIMES)):
            #start_time, end_time = self.LECTURE_TIMES[i]
            #self._lectureTimes.append(LECTURETIME(start_time, end_time))
        for i in range(len(self.LECTURE_TIMES)):
            start_time = self.LECTURE_TIMES[i][0]
            end_time = self.LECTURE_TIMES[i][1]
            self._lectureTimes.append(LECTURETIME(start_time, end_time))

        for i in range(0, len(self.LECTURERS)):
            self._lecturers.append(Lecturer(self.LECTURERS[i][0], self.LECTURERS[i][1]))
        course1 = Course("C1", "325K", [self._lecturers[0],self._lecturers[1]],25)                
        course2 = Course("C2", "319K", [self._lecturers[0],self._lecturers[1], self._lecturers[2]],35)
        course3 = Course("C3", "462K", [self._lecturers[0],self._lecturers[1]],25)
        course4 = Course("C4", "464K", [self._lecturers[2],self._lecturers[3]],30)  
        course5 = Course("C5", "368C", [self._lecturers[3]],35)
        course6 = Course("C6", "303K", [self._lecturers[0],self._lecturers[2]],45)
        course7 = Course("C7", "303L", [self._lecturers[1],self._lecturers[3]],45)
        self._courses = [course1, course2, course3, course4, course5, course6, course7]
        dept1 = Department("CSC",[course1,course3])
        dept2 = Department("MATH", [course2, course4, course5])
        dept3 = Department("STAT", [course6, course7])
        self._depts = [dept1,dept2, dept3]
        self.numberOfClasses = 0
        for i in range(0, len(self._depts)):
            self.numberOfClasses += len(self._depts[i].get_courses())
    def get_rooms(self): return self._rooms
    def get_lecturers(self): return self._lecturers
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_lectureTimes(self): return self._lectureTimes
    def get_numberOfClasses(self): return self._numberOfclasses        
class Schedule:
        def __init__(self):
            self._data = data
            self._classes = []
            self._numbOfConflicts = 0
            self._fitness = -1
            self._classNumb = 0
            self._isFitnessChanged = True
        def get_classes(self):
            self._isFitnessChanged = True
            return self._classes
        def get_numbOfConflicts(self):
            return self._numbOfConflicts
        def get_fitness(self):
            if (self._isFitnessChanged == True):
                self._fitness = self.calculate_fitness()
                self._isFitnessChanged = False
            return self._fitness
        def initialize(self):
            depts = self._data.get_depts()
            for i in range(0, len(depts)):
                courses = depts[i].get_courses()
                for j in range(0, len(courses)):
                    newClass = Class(self._classNumb, depts[i], courses[j])
                    self._classNumb += 1
                    newClass.set_lectureTime(data.get_lectureTimes()[rnd.randrange(0, len(data.get_lectureTimes()))])
                    newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                    newClass.set_lecturer(courses[j].get_lecturers()[rnd.randrange(0, len(courses[j].get_lecturers()))])
                    self._classes.append(newClass)
            return self
        def calculate_fitness(self):
            self._numbOfConflicts = 0
            classes = self.get_classes()
            for i in range(0, len(classes)):
                if (classes[i].get_room().get_seatingCapacity() < classes[i].get_course().get_maxNumOfStudents()): 
                    self._numbOfConflicts += 1
            for j in range(0, len(classes)):
                if (j >= 1):
                    if (classes[i].get_lectureTime()== classes[j].get_lectureTime() and 
                        classes[i].get_id() != classes[j].get_id()):
                        if (classes[i].get_room() == classes[j].get_room()): self._numbOfConflicts += 1
                        if (classes[i].get_lecturer() == classes[j].get_lecturers()): self._numbOfConflicts += 1 
            return 1 / ((1.0*self._numbOfConflicts + 1)) 
        def __str__(self):
            returnValue = ""
            for i in range(0, len(self._classes)-1):
                returnValue += str(self._classes[i]) + ","
            returnValue += str(self._classes[len(self._classes)-1])
            return returnValue
class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(0, size): self._schedules.append(Schedule().initialize())
    def get_schedules(self):
        return self._schedules
class GeneticAlgorithm:
    def evolve(self, population): return self._mutate_population(self._crossover_population(population))
    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUM_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUM_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self.crossover_schedule(schedule1,schedule2))
            i += 1
        return crossover_pop
    def _mutate_population(self, population):
        for i in range(NUM_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population
    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if (rnd.random() > 0.5): crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else: crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule
    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(0, len(mutateSchedule.get_classes())):
            if (MUTATION_RATE > rnd.random()): mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule
    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop     
class Course:
    def __init__(self, number, name, lecturers, maxNumOfStudents):
        self._number = number
        self._name = name
        self._lecturers = lecturers
        self._maxNumOfStudents = maxNumOfStudents
    def get_number(self): return self._number
    def get_name(self): return self._name
    def get_lecturers(self): return self._lecturers
    def get_maxNumOfStudents(self): return self._maxNumOfStudents
    def __str__(self): return self._name                 
#class Lecturer:
    #def _init_(self, id, name):
        #self._id = id
        #self._name = name
        #def get_id(self): return self._id
        #def get_name(self): return self._name
        #def __str__(self): return self._name
class Lecturer:
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses
        def get_name(self): return self.name
        def get_courses(self): return self.courses
        def __str__(self): return self.courses
###########################################
class LECTURETIME:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
    
    def __str__(self):
        return '{}-{}'.format(self.start_time, self.end_time)

class Room:
    def __init__(self, number, seatingCapacity):
        self.number = number
        self.seatingCapacity = seatingCapacity
        def get_number(self): return self._number
        def get_seatingCapacity(self): return self._seatingCapacity
class LectureTime:
    def __init__(self, id, time):
        self._id = id
        self._time = time
        def get_id(self): return self._id
        def get_time(self): return self._time
class Department:
    def __init__(self, name, courses):
        self.name = name
        def get_name(self): return self._name
        def get_courses(self): return self._courses
    
    def get_courses(self):
        return self.get_courses
class Class:
    def __init__(self, id, dept, course):
        self._id = id
        self._dept = dept
        self._course = course
        self._lecturer = None
        self._lectureTime = None
        self._room = None
        def get_id(self): return self._id
        def get_dept(self): return self._dept
        def get_course(self): return self._course
        def get_lecturer(self): return self._lecturer
        def get_lectureTime(self): return self._lectureTime
        def get_room(self): return self._room
        def set_lecturer(self, lecturer): self._lecturer = lecturer
        def set_lectureTime(self, lectureTime): self._lectureTime = lectureTime
        def set_room(self, room): self._room = room
        def __str__(self):
            return str(self._dept.get_name()) + "," + str(self._course.get_number()) + "," + \
                str(self.room.get_number()) + "," + str(self._lecturer.get_id()) + "," + str(self._lectureTime.get_id())
class DisplayMgr:
    def print_available_data(self):
        print("> All Available Data")
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_lecturer()
        self.print_lecture_times()
    def print_dept(self):
        depts = data.get_depts()
        availableDeptsTable = prettytable.PrettyTable(['dept', 'courses'])
        for i in range(0, len(depts)):
            courses = depts._getitem_(i).get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row([depts.__getitem__(i).get_name(), tempStr])
        print(availableDeptsTable)
    def print_course(self):
        availableCoursesTable = prettytable.PrettyTable(['id', 'course #', 'max # of students', 'lecturers'])
        courses = data.get_courses()
        for i in range(0, len(courses)):
            lecturers = courses[i].get_lecturers()
            tempStr = ""
            for j in range(0, len(lecturers) - 1):
                tempStr += lecturer[j].__str__() + ", "
            tempStr += lecturers[len(lecturers) - 1].__str__()
            availableCoursesTable.add_row([courses[i].get_name(), str(courses[i].get_maxNumOfStudents()), tempStr])
        print(availableCoursesTable)
    def print_lecturer(self):
        availableLecturersTable = prettytable.PrettyTable(['id', 'Lecturer'])
        lecturers = data.get_lecturers()
        for i in range(0, len(lectures)):
            availableLecturesTable.add_row([lecturers[i].get_id(), lecturers[i].get_name()])
        print(availableLecturersTable)
    def print_room(self):
        availableRoomsTable = prettytable.PrettyTable(['room #', 'max seating capacity'])
        rooms = data.get_rooms()
        for i in range(0, len(rooms)):
            availableRoomsTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        print(availableRoomsTable)
    def print_lecture_times(self):
        availableLectureTimeTable = prettytable.PrettyTable(['id', 'Lecture Time'])
        lectureTimes = data.get_lectureTimes()
        for i in range(0, len(lectureTimes)):
            availableLectureTimeTable.add_row([lectureTimes[i].get_id(), lectureTimes[i].get_time()])
        print(availableLectureTimeTable)
    def print_generation(self, population):
        table1 = prettytable.PrettyTable(['schedule #', 'fitness', '# of conflicts', 'classes [dept,class,room,lecturer...]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i), round(schedules[i].get_fitness(),3), schedules[i].get_numbOfConflicts(), schedules[i].get_classes()])
        print(table1)
    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(['Class #','Dept','Course (number, max # of students)', 'Room (Capacity)', 'Lecturer', 'Lecture Time'])
        for i in range(0, len(classes)):
            table.add_row([str(i),classes[i].get_dept().get_name(), classes[i].get_course().get_name() + "(" +
                            classes[i].get_course().get_number() + ", " +
                            str(classes[i].get_course().get_maxNumOfStudents()) + ")",
                            classes[i].get_room().get_number() + " (" + str(classes[i].get_room().get_seatingCapacity()) + ")",
                            classes[i].get_lecturer().get_name() + " (" + str(classes[i].get_lecturer().get_id()) + ")",
                            classes[i].get_lectureTime().get_time() + " (" + str(classes[i].get_lectureTime().get_id()) + ")" ])
        print(table)


data = Data()
displayMgr = DisplayMgr()
displayMgr.print_available_data()
generationNumber = 0
print("\n> Generation # " + str(generationNumber))
population = Population(POPULATION_SIZE)
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
displayMgr.print_generation(population)
displayMgr.print_schedule_as_table(population.get_schedules()[0])
geneticAlgorithm = GeneticAlgorithm()
while (population.get_schedules()[0].get_fitness()!= 1.0):
    generationNumber += 1
    print("\n> Generation # " + str(generationNumber))
    population = geneticAlgorithm.evolve(population)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    displayMgr.print_generation(population)
    displayMgr.print_schedule_as_table(population.get_schedules()[0])
print("\n\n")
