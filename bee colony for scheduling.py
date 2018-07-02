from math import *
from random import uniform, randrange
import random
import copy
import pygame


class course:
    def __init__(self, name, num, hours, stress):
        self.name = name
        self.num = num
        self.hours = hours
        self.stress = stress

    def __repr__(self):
        return ("%s" % (self.name))


class candidate:
    def __init__(self, cours, day_hours, blocks, course_per_day):
        self.total_hours = 0
        self.schedule = []
        self.blocks = blocks
        self.cours = copy.deepcopy(cours)
        self.day_hours = day_hours
        self.slots = []
        self.fitness = 0
        self.course_per_day = course_per_day
        self.e = 0
        self.fill_cand()
        self.set_fitness()

    def fill_cand(self):
        # total of hours
        for x in range(len(self.cours)):
            self.total_hours = self.total_hours + self.cours[x].hours
        # fill slots
        for x in range(self.total_hours):
            self.slots.append(x)

        temp_cours = copy.deepcopy(self.cours)

        # fill candidates
        temp_cand = []
        for x in range(len(self.slots)):
            if temp_cours:
                temp_cour = random.choice(temp_cours)
                idx_h = temp_cours.index(temp_cour)
                temp_cours[idx_h].hours = temp_cours[idx_h].hours - 1
                if temp_cours[temp_cours.index(temp_cour)].hours == 0:
                    temp_cours.remove(temp_cour)
                self.schedule.append(temp_cour)

        print(self.schedule)

    # set fitness
    def set_fitness(self):
        self.fitness = 0
        temp_num = []
        temp_stress = []
        prom_temp_stress = []
        prom_day_cour = []
        prom_week_cour = []
        only_one_course_per_day = []
        prom_only_one_course_per_day = []
        for x in range(len(self.schedule)):
            temp_num.append(self.schedule[x].num)
            temp_stress.append(self.schedule[x].stress)
            if (x + 1) % self.day_hours == 0:
                # Promedio bloques de curso al dia
                count = 1
                for y in range(len(temp_num) - 1):
                    if temp_num[y] == temp_num[y + 1]:
                        count = count + 1
                    else:
                        prom_day_cour.append(count)
                        count = 1

                # maximo del curso diario a la semana
                prom_week_cour.append(max(prom_day_cour))

                # prom Stress diario
                stres = 0
                for y in range(len(temp_stress)):
                    stres = stres + temp_stress[y]

                # prom Stress Semanal
                prom_temp_stress.append(stres)

                # Curso por dia
                count = 0
                for y in range(0, len(temp_num) - 1):
                    if temp_num[y] != temp_num[y + 1]:
                        for z in range(y, len(temp_num)):
                            if temp_num[y] == temp_num[z]:
                                count = count + 1
                        only_one_course_per_day.append(count)

                # maximo del prom curso por dia
                prom_only_one_course_per_day.append(max(only_one_course_per_day))

                only_one_course_per_day = []
                temp_num = []
                temp_stress = []
                prom_day_cour = []

        # Fitness for weekly block course
        b_c = self.blocks - abs(self.blocks - max(prom_week_cour))
        self.fitness += b_c

        # Fitness for weekly stress
        st = max(prom_temp_stress)
        self.fitness = self.fitness + (1 / st)

        # Fitness for weekly course per day
        c_d = self.course_per_day - abs(self.course_per_day - max(prom_only_one_course_per_day))
        # print(prom)
        self.fitness += c_d

    def recall(self):
        self.schedule = []
        self.fitness = 0
        self.e = 0
        self.fill_cand()
        self.set_fitness()


class beeColony():
    # it needs the colony size, dimension of space, num of iter and domain, courses
    def __init__(self, CS, dim, it, candidate):
        self.CS = CS
        self.dim = dim
        self.it = it
        self.LE = (CS * dim) / 2
        self.best = 0
        self.candidate = copy.deepcopy(candidate)
        self.candidates = []

    def fitness(self, candidat):
        return canditat.fitness

    def init(self):
        for x in range(int(self.CS / 2)):
            rows = []
            for y in range(self.dim):
                temp = copy.deepcopy(self.candidate)
                temp.recall()
                rows.append(temp)
            self.candidates.append(rows)

    def employeeBee(self):
        for i in range(int(self.CS / 2)):
            j = randrange(self.dim)
            fi_1 = randrange(self.candidate.total_hours)
            fi_2 = randrange(self.candidate.total_hours)
            v_i = copy.deepcopy(self.candidates[i][j])
            v_i.schedule[fi_1], v_i.schedule[fi_2] = v_i.schedule[fi_2], v_i.schedule[fi_1]
            v_i.set_fitness()
            if v_i.fitness < self.candidates[i][j].fitness:
                self.candidates[i][j].e += 1
            else:
                v_i.e = 0
                self.candidates[i][j] = copy.deepcopy(v_i)


    def probability(self):
        temp = []
        suma = 0
        for x in range(len(self.candidates)):
            suma = suma + self.candidates[x][self.dim - 1].fitness

        for x in range(len(self.candidates)):
            temp.append(self.candidates[x][self.dim - 1].fitness / suma)

        temp_sum = []
        suma = 0
        temp_sum.append(0)
        for x in range(len(temp) - 1):
            suma += temp[x]
            temp_sum.append(suma)

        ram = uniform(0, 1)
        res = 0
        for x in range(len(temp_sum)):
            if ram > temp_sum[x]:
                res = x
        return res

    def spectatorBee(self):
        for x in range(int(self.CS / 2)):
            i = self.probability()
            j = randrange(self.dim)
            fi_1 = randrange(self.candidate.total_hours)
            fi_2 = randrange(self.candidate.total_hours)
            v_i = copy.deepcopy(self.candidates[i][j])
            v_i.schedule[fi_1], v_i.schedule[fi_2] = v_i.schedule[fi_2], v_i.schedule[fi_1]
            v_i.set_fitness()
            if v_i.fitness < self.candidates[i][j].fitness:
                self.candidates[i][j].e += 1
            else:
                v_i.e = 0
                self.candidates[i][j] = copy.deepcopy(v_i)

    def searchBee(self):
        for x in range(len(self.candidates)):
            if self.candidates[x][self.dim - 1].fitness > self.candidates[self.best][self.dim - 1].fitness:
                self.best = x
            if self.candidates[x][self.dim - 1].e >= self.LE:
                self.candidates[x][self.dim - 1].recall()

    def run(self):
        self.init()
        self.display_width = 800
        self.display_height = 800

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.linesize = 800
        temp_best = self.best
        pygame.init()
        for x in range(self.it):
            self.employeeBee()
            self.spectatorBee()
            self.searchBee()
            for y in range(len(self.candidates)):
                print(self.candidates[y][self.dim - 1].fitness)
            print("---- %i -----" % x)
            if x == 0:
                self.draw(99, self.candidates[self.best][self.dim - 1])

            if temp_best != self.best:
                print("entre")
                self.draw(99, self.candidates[self.best][self.dim - 1])
            temp_best = self.best
        input()
        pygame.quit()
        quit()

    def draw(self, vel, cd):
        
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        self.clock = pygame.time.Clock()

        self.gameDisplay.fill(self.black)
        for x in range(cd.day_hours + 2):
            self.line(1, (self.display_height / (cd.day_hours + 1)) * (x + 1), 0)

        days = ["lunes", "martes", "miercoles", "jueves", "viernes"]
        for x in range(len(days)):
            self.line((self.display_width / (len(days))) * (x + 1), self.display_height, 90)

        for x in range(len(days)):
            self.message_display(days[x], [((self.display_width / (len(days))) * (x + 1)) - 80, 40], 30)
            for y in range(cd.day_hours):
                self.message_display(str(cd.schedule[x + (cd.day_hours - 1 * y)]),
                                     [(self.display_height / len(days)) * (x + 1) - 80,
                                      (self.display_height / (cd.day_hours + 1)) * (y + 1) + 40],
                                      8)

        pygame.display.update()
        # self.clock.tick(vel)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.white)
        return textSurface, textSurface.get_rect()

    def message_display(self, text, pos, size):
        largeText = pygame.font.Font('freesansbold.ttf', size)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = (pos[0], pos[1])
        self.gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()

    def line(self, thingx, thingy, angle):
        pygame.draw.line(self.gameDisplay, self.white, [thingx, thingy], [thingx + cos(radians(angle)) * self.linesize, thingy - sin(radians(angle)) * self.linesize], 5)



curs1 = course("Matemáticas", 1, 6, 7)
curs2 = course("Razonamiento Matemàtico", 2, 2, 5)
curs3 = course("Comunicación ", 3, 7, 6)
curs4 = course("Inglés", 4, 2, 8)
curs5 = course("Arte", 5, 2, 1)
curs6 = course("Historia, Geografia y Economia", 6, 4, 7)
curs7 = course("Formación Cívica y Cuidadana", 7, 2, 3)
curs8 = course("Person, Familia y Relaciones Humanas", 8, 2, 3)
curs9 = course("Formación Física", 9, 2, 2)
curs10 = course("Formación Religiosa", 10, 1, 1)
curs11 = course("Ciencia, Tecnología y Ambiente", 11, 6, 7)
curs12 = course("Educacion para el Trabajo", 12, 2, 3)
curs13 = course("Tutoría", 13, 1, 1)
curs14 = course("Ecología y Medio Ambiente", 14, 1, 5)
cursos = [curs1, curs2, curs3, curs4, curs5, curs6, curs7, curs8, curs9, curs10, curs11, curs12, curs13, curs14]

# Candidate recibe cursos, horas al dia, bloques de curso al dia, cantidad del mismo curso por dia
cd = candidate(cursos, 8, 2, 1)

# colony size, dimension of space, num of iter and courses
b_c = beeColony(50, 1, 301, cd)

b_c.run()

print(b_c.candidates[b_c.best][b_c.dim - 1].fitness)
dias = ["lunes", "martes", "miercoles", "jueves", "viernes"]
for x in range(len(b_c.candidates[b_c.best][b_c.dim - 1].schedule)):
    if x % 8 == 0:
        print(dias[int(x / 8)])
    print(" ", b_c.candidates[b_c.best][b_c.dim - 1].schedule[x])
