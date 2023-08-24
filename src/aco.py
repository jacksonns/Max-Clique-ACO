from src.graph import Graph
from src.clique import Clique
from src.results import Results
from src.util import TAU_MAX, TAU_MIN

class Ant:
    def __init__(self, graph, alpha):
        self.clique = Clique(graph, alpha)
    
    def construct_maximal_clique(self):
        self.clique.construct_maximal_clique()
    
    def get_clique_size(self):
        return self.clique.get_size()

    def get_clique(self):
        return self.clique

class AntColonyOptimizer:
    def __init__(self, config_args):
        self.graph = Graph(config_args['file_path'])
        self.ants_num = config_args['ants_num']
        self.iterations = config_args['iterations']
        self.evaporation = config_args['evaporation']
        self.alpha = config_args['alpha']
        self.results = Results(config_args)
    
    def evaporate_trails(self):
        self.graph.evaporate_trails(self.evaporation)

    def update_edge(self, edge, ant_pheromone):
        new_pheromone = edge.get_pheromone() + ant_pheromone

        if new_pheromone < TAU_MIN:
            edge.set_pheromone(TAU_MIN)
        elif new_pheromone > TAU_MAX:
            edge.set_pheromone(TAU_MAX)
        else:
            edge.set_pheromone(new_pheromone)
    
    def update_trails(self, clique, ant_pheromone):
        edges = clique.get_edges()
        for u, v in edges:
            edge1 = self.graph.get_edge(u, v)
            edge2 = self.graph.get_edge(v, u)
            self.update_edge(edge1, ant_pheromone)
            self.update_edge(edge2, ant_pheromone)
        
    def run(self):
        self.graph.initialize_trails(TAU_MAX)

        it = 0
        best_clique_size = 0
        best_clique = None

        while it < self.iterations:
            best_cycle_clique_size = 0

            ants = [Ant(self.graph, self.alpha) for _ in range(self.ants_num)]

            for ant in ants:
                ant.construct_maximal_clique()

                size = ant.get_clique_size()
                if size > best_cycle_clique_size: 
                    best_cycle_clique = ant.get_clique()
                    best_cycle_clique_size = size

            if best_cycle_clique_size > best_clique_size:
                best_clique = best_cycle_clique
                best_clique_size = best_cycle_clique_size
            
            print(f'Iteration {it}: Best Clique k = {best_cycle_clique_size}')

            ant_pheromone = 1 / (1 + best_clique_size - best_cycle_clique_size)
            self.evaporate_trails()
            self.update_trails(best_cycle_clique, ant_pheromone)

            self.results.update_results(it, best_clique_size)

            it += 1
    
        self.results.update_best_clique(best_clique)

        
        print(f'\nBest Clique Found: k = {best_clique_size}')