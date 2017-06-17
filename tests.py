from random import randint, random
from operator import add

def individual(min, max):
    'Create a member of the population.'
    return [ randint(min,max) for x in xrange(2) ]

def population(count, min, max):
    """
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the minimum possible value in an individual's list of values
    max: the maximum possible value in an individual's list of values

    """
    return [ individual(min, max) for x in xrange(count) ]

def fitness(individual):
    """
    Determine the fitness of an individual. Higher is better.

    individual: the individual to evaluate
    target: the target number individuals are aiming for
    """
    x=individual[0]
    z=individual[1]
    return  x**2-2*x*z+6*x+z**2-6*z

def grade(pop):
    'Find average fitness for a population.'
    summed = reduce(add, (fitness(x) for x in pop))
    return summed / (len(pop) * 1.0)


def selection_roullete(contesters):
    '''
    receives a list of contesters with [fitness,[x,y]]
    :param contesters: 
    :return: 
    '''
    lista = []
    mating_pool=[]
    bestfit=contesters[0][0]
    worstfit=contesters[len(contesters)-1][0]
    selected=[]
    for i,el in enumerate(contesters):
        lista.append([translate(el[0],worstfit,bestfit),el[1]])
        rand = randint(0,100)
        if lista[i][0] >= rand:
            selected.append(lista[i][1][1])
    for individual in lista:
        for i in range(individual[0]):
            mating_pool.append(individual[1])
    return mating_pool

def translate(value, leftMin, leftMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    if leftSpan ==0:
        return 50

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(valueScaled * 100)

def evolve(pop, elitism=0.25, breed_rate=0.70, mutate=0.01):
    graded = [ (fitness(x), x) for x in pop]
    pop_by_fitness = [ x for x in sorted(graded)]
    pop_without_fitness=[ x[1] for x in sorted(graded)]
    retain_length = int(len(pop_by_fitness)*elitism)

    #the x% best fit will survive to the next generation!
    next_pop = pop_without_fitness[:retain_length]

    # crossover parents to create children
    mating_pool = selection_roullete(pop_by_fitness)
    n_breedings = int(len(pop)*breed_rate)
    for i in range(0,n_breedings):
        male = randint(0, len(mating_pool)-1)
        female = randint(0, len(mating_pool)-1)
        if male != female:
            male = mating_pool[male]
            female = mating_pool[female]
            half = len(male) / 2
            child = male[:half] + female[half:]
            next_pop.append(child)

    # randomly add other individuals to
    # promote genetic diversity
    while len(next_pop) < len(pop):
       next_pop.append(pop_without_fitness[randint(0, len(pop_without_fitness) - 1)])

    # mutate some individuals
    for individual in next_pop:
        if mutate > random():
            #print individual,"mutated to "
            pos_to_mutate = randint(0, len(individual)-1)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            individual[pos_to_mutate] = randint(
                min(individual), max(individual))
            #print individual
    #print "end of pop"


    return next_pop


p_count = 100
i_min = -100
i_max = 100
p = population(p_count, i_min, i_max)
fitness_history = [grade(p),]
count=0
while grade(p) > -8.9:
    p = evolve(p)
    fitness_history.append(grade(p))
    count+=1
for datum in fitness_history:
   print datum
print count
