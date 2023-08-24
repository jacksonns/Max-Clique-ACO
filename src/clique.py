import random

class Candidate:
    def __init__(self, edge) :
        self.edge = edge
        self.p_factor = edge.get_pheromone()
    
    def __repr__(self) -> str:
        return f'Vértice {self.edge.get_vertex()}'
    
    def items(self):
        return self.edge, self.p_factor
    
    def get_edge(self):
        return self.edge
    
    def get_p_factor(self):
        return self.p_factor


class Clique:
    # Constrói Clique.
    def __init__(self, graph, alpha):
        self.graph = graph
        self.alpha = alpha
        self.vertices = []
        self.size = 0
    
    def get_repr(self) -> str:
        repr = f'\nClique: k={self.get_size()}\nVertices: '
        for v in self.vertices:
            repr += f'{v} '
        return repr
    
    def get_size(self):
        return self.size

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        size = self.get_size()
        edges = []
        for i in range(size):
            for j in range (i+1, size):
                edges.append( (self.vertices[i], self.vertices[j]) )
        return edges
    
    def get_random_vertex(self):
        return random.choice(self.graph.get_vertices())

    def get_factors_sum(self, candidates):
        sum = 0
        for candidate in candidates:
            sum += candidate.get_p_factor()
        return sum
    
    # Choose edge with probability p(i)
    def choose_candidate(self, candidates):
        p_factors_sum = self.get_factors_sum(candidates) ** self.alpha
        p = []
        for candidate in candidates:
            pi = candidate.get_p_factor() ** self.alpha / p_factors_sum
            p.append(pi)
            #print(f'Candidato {candidate}, Probabilidade: {pi}')
        return random.choices(candidates, weights=p, k=1)[0]
    
    def update_candidates(self, candidates, v1):
        candidates_copy = list(candidates)
        for candidate in candidates_copy:
            edge = candidate.get_edge()
            v2 = edge.get_vertex()
            if not self.graph.has_edge(v1, v2): 
                candidates.remove(candidate)
    
    def print_candidates(self, candidates):
        string = 'Candidatos: '
        for c in candidates:
            string += f'{str(c.get_edge().get_vertex())} '
        print(string)

    def construct_maximal_clique(self):
        u = self.get_random_vertex()
        self.vertices.append(u)
        self.size += 1

        neighbors = self.graph.get_neighbor_edges(u)

        candidates = [Candidate(edge) for edge in neighbors]

        while candidates:
            chosen = self.choose_candidate(candidates)

            # Add chosen vertex to Clique
            edge = chosen.get_edge()
            v = edge.get_vertex()
            self.vertices.append(v)
            self.size += 1

            # Update candidates
            candidates.remove(chosen)
            self.update_candidates(candidates, v)