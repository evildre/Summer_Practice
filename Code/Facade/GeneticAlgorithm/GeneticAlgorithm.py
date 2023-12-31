import math

from imports import *


class GeneticAlgorithm:

    # В конструкторе происходит распаковка данных,
    # которые задал пользователь (не хватает функционала для управления модификациями).
    def __init__(self, input_data):
        self.__number_of_items = len(input_data.weights)
        self.__weights = input_data.weights
        self.__costs = input_data.costs
        self.__probability_of_mutation = input_data.probability_of_mutation
        self.__probability_of_crossover = input_data.probability_of_crossover
        self.__number_of_individuals = input_data.number_of_individuals
        self.__backpack_capacity = input_data.backpack_capacity
        self.__parents_selector, self.__pair_matcher, self.__recombinator, \
        self.__mutator, self.__population_selector = input_data.modifications
        self.__population_data_list = []

    '''
    Данный метод предназначен для отбора родителей в популяции в зависимисомти
    от модификации, которую выбрал пользователь.
    Входные данные: популяция (список особей)
    Выходные данные: родители (список особей)
    '''

    def __get_parents(self, population: list) -> list:
        match self.__parents_selector:
            case Modifications.tournament_selection.value:
                parents_selector = TournamentSelector(population,
                                                      [self.__cost_of_individual(individual) for individual in
                                                       population],
                                                      [self.__weight_of_individual(individual) for individual in
                                                       population], self.__backpack_capacity)
            case Modifications.roulette_selection.value:
                parents_selector = RouletteSelector(population,
                                                    [self.__cost_of_individual(individual) for individual in
                                                     population],
                                                    [self.__weight_of_individual(individual) for individual in
                                                     population], self.__backpack_capacity)
        parents = parents_selector.make_parents()
        return parents

    '''
    Данный метод предназначен для составления пар родителей по принципу, который задал пользователь.
    Входные данные: список родителей
    Выходные данные: список пар родителей
    '''

    def __get_parents_pairs(self, parents: list, clarify: bool) -> list:
        match self.__pair_matcher:
            case Modifications.panmixia.value:
                pair_matcher = Panmixia(parents)
            case Modifications.in_and_outbreeding.value:
                if clarify:
                    pair_matcher = Inbreeding(parents)
                else:
                    pair_matcher = Outbreeding(parents)
        parents_pairs = pair_matcher.make_parents_pairs()
        return parents_pairs

    '''
    Данный метод предназначен для формирвания семей (потомок 1, потомок 2, родитель 1, родитель 2) 
    в зависимости от того рекомбинатора, который задал пользователь. 
    Входные данные: список пар родителей
    Выходные данные: список семей, где каждая семья - кортеж размерностью 4
    '''

    def __get_families(self, parents_pairs: list) -> list:
        match self.__recombinator:
            case Modifications.homogeneous_recombination.value:
                recombination = HomogeneousRecombinator(
                    parents_pairs, 0.5, self.__probability_of_crossover)
            case Modifications.single_point_recombination.value:
                recombination = SinglePointRecombinator(
                    parents_pairs, 0.5, self.__probability_of_crossover)
        families = recombination.make_children()
        return families

    '''
    Данный метод предназначен для получения списка отправленных на мутацию детей (не гарантирует, что все дети мутируют)
    в зависимости от установленного пользователем мутатора.
    Входные данные: список семей
    Выходные данные: список детей
    '''

    def __get_children(self, families: list) -> list:
        match self.__mutator:
            case Modifications.binary_mutator.value:
                mutator = ChangingMutator(
                    families, self.__probability_of_mutation)
            case Modifications.adaptive_mutator.value:
                mutator = ChangingMutator(
                    families, self.__probability_of_mutation)
        children = mutator.make_mutation()
        return children

    '''
    Данный метод формирует новую популяцию из списка родителей и списка детей по тому принципу, 
    который задал пользователь.
    Входные данные: список детей и список родителей
    Выходные данные: новая популяция
    '''

    def __get_new_population(self, children: list, population: list) -> list:
        match self.__population_selector:
            case Modifications.selection_by_displacement.value:
                population_selector = SelectionByDisplacement(self.__init_info_about_individuals(population + children),
                                                              self.__backpack_capacity)
                new_population = population_selector.make_new_population() + self.__generate_population(
                    int(0.9 * self.__number_of_individuals))
            case Modifications.elite_selection.value:
                population_selector = EliteSelection(self.__init_info_about_individuals(population + children),
                                                     self.__backpack_capacity)
                new_population = population_selector.make_new_population() + self.__generate_population(
                    int(self.__number_of_individuals))
        return new_population

    '''
    Данный метод запускает и останавливает генетический алгоритм, 
    является посредником в обмене данными между модулями ГА.
    Выходные данные: список структур, в каждой из которых хранится самая важная 
    информация о каждой популяции (понадобится для отображения в GUI)
    '''

    def run(self):
        population = self.__generate_population(self.__number_of_individuals)
        self.__init_population_info(population)
        print(
            f"Стоимость ранца (динамический метод): {knapsack(self.__weights, self.__costs, self.__backpack_capacity)}")
        i = 0
        while i < 100:
            parents = self.__get_parents(population)
            parents_pairs = self.__get_parents_pairs(parents, i > 50)
            families = self.__get_families(parents_pairs)
            children = self.__get_children(families)
            population = self.__get_new_population(children, population)
            self.__init_population_info(population)
            if self.__population_data_list[-1].price_of_best_chromosome - \
                    self.__population_data_list[-2].price_of_best_chromosome == 0:
                i += 1
            else:
                i = 0
        return self.__population_data_list

    '''
    Данные метод инициализирует самые важные данные о каждой популяции, который нужно для отобржения графика в GUI.
    Входные данные: популяция
    '''

    def __init_population_info(self, population: list) -> None:
        sum_cost_of_population = 0
        max_cost_of_individual = 0
        best_chromosome = population[0]
        bad_population = True
        for individual in population:
            cost_of_individual = self.__cost_of_individual(individual)
            sum_cost_of_population += cost_of_individual
            if cost_of_individual > max_cost_of_individual and self.__weight_of_individual(
                    individual) <= self.__backpack_capacity:
                bad_population = False
                max_cost_of_individual = cost_of_individual
                best_chromosome = individual
        population_data = PopulationData(best_chromosome, max_cost_of_individual,
                                         self.__weight_of_individual(
                                             best_chromosome),
                                         sum_cost_of_population / len(population), bad_population)
        self.__population_data_list.append(population_data)

    '''
    Данный метод генерирует начальную популяцию.
    Выходные данные: сгенерированная начальная популяция
    '''

    def __generate_population(self, number_of_individuals) -> list:
        population = []
        i = 0
        while i < number_of_individuals:
            weight_of_individual = 0
            chromosome = ['0'] * self.__number_of_items
            numbers_of_items_not_taken = [
                i for i in range(self.__number_of_items)]
            numbers_of_taken_items = []
            while True:
                if len(numbers_of_items_not_taken) == 0:
                    population.append(chromosome)
                    i += 1
                    break
                index_of_item_not_taken = random.randint(
                    0, len(numbers_of_items_not_taken) - 1)
                number_of_taken_item = numbers_of_items_not_taken.pop(
                    index_of_item_not_taken)
                numbers_of_taken_items.append(number_of_taken_item)
                chromosome[number_of_taken_item] = '1'
                weight_of_individual += self.__weights[number_of_taken_item]
                if weight_of_individual > self.__backpack_capacity:
                    index_of_returned_item = self.__get_index_of_returned_item(
                        numbers_of_taken_items)
                    number_of_returned_item = numbers_of_taken_items.pop(
                        index_of_returned_item)
                    chromosome[number_of_returned_item] = '0'
                    population.append(chromosome)
                    i += 1
                    break
        return population

    '''
    Данный метод находит индекс предмета, 
    который лучше всего выкинуть из хромосомы,
    чтобы её можно было положить в рюкзак (выкидываем самый жирный по весу предмет).
    Входные данные: номера уже взятых предметов в набор.
    Выходные данные: индекс предмета, который лучше всего выкинуть.
    '''

    def __get_index_of_returned_item(self, numbers_of_taken_items: list) -> int:
        weights_of_gens = [self.__weights[number_of_taken_item]
                           for number_of_taken_item in numbers_of_taken_items]
        max_weight = max(weights_of_gens)
        return weights_of_gens.index(max_weight)

    '''
    Данный метод считает вес особи
    Входные данные: особь(хромосома)
    Выходные данные: вес особи
    '''

    def __weight_of_individual(self, individual: list) -> int:
        weight = 0
        for i in range(len(individual)):
            weight += int(individual[i]) * self.__weights[i]
        return weight

    '''
    Данный метод считает цену особи
    Входные данные: особь(хромосома)
    Выходные данные: цена особи
    '''

    def __cost_of_individual(self, individual: list) -> int:
        cost = 0
        for i in range(len(individual)):
            cost += int(individual[i]) * self.__costs[i]
        return cost

    '''
    Данный метод инициализирует данные о каждой особи популяции в виде кортежа (цена особи, вес, хромосома)
    Входные данные: список особей
    Выходные данные: список кортежей вида (цена особи, вес, хромосома)
    '''

    def __init_info_about_individuals(self, population: list) -> list:
        info_about_individuals = []
        for individual in population:
            info_about_individual = (
                self.__cost_of_individual(individual), self.__weight_of_individual(individual), individual)
            info_about_individuals.append(info_about_individual)
        return info_about_individuals
