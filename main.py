#!/usr/bin/python
# -*-coding: utf-8-*-

import sys
from collections import defaultdict


def read_graph_file(file_name):
    graph_struct = defaultdict(dict)
    with open(file_name, 'r') as f:
        for s in f:
            v, w,   l = (int(x) for x in s.strip().split())
            graph_struct[v][w] = l
            graph_struct[w][v] = l
    return graph_struct


def distances_from_one(graph, v):
    distance_from_one = {w: l for w, l in graph[v].items()}
    distance_from_one[v] = 0
    not_rated = set(graph.keys()) - {v}
    while not_rated:
        min_not_rated_w, _ = min(
            {k: distance_from_one[k] for k in not_rated if k in distance_from_one}.items(),
            key=lambda x: x[1]
        )
        not_rated = not_rated - {min_not_rated_w, }
        for k in not_rated:
            if k in graph[min_not_rated_w]:
                if k in distance_from_one:
                    distance_from_one[k] = min(
                        distance_from_one[k],
                        distance_from_one[min_not_rated_w] + graph[min_not_rated_w][k]
                    )
                else:
                    distance_from_one[k] = distance_from_one[min_not_rated_w] + graph[min_not_rated_w][k]
    return distance_from_one


def opt_path_by_distance(graph, start, finish, distances):
    if finish == start:
        return [start, ]

    result = [finish, ]
    for k in distances:
        if k in graph[finish]:
            if distances[finish] == graph[finish][k] + distances[k]:
                result = result + opt_path_by_distance(graph, start, k, distances)
                return result
    assert(0)


def opt_path(graph, start, finish):
    distances_from_start = distances_from_one(graph, start)
    return opt_path_by_distance(graph, start, finish, distances_from_start), distances_from_start[finish]


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('format: python main.py file start end')

    graph = read_graph_file(sys.argv[1])
    print('Path: {}, distance: {}'.format(*opt_path(graph, int(sys.argv[2]), int(sys.argv[3]))))

    exit(0)
