from tabulate import tabulate


def create_row(edges):
    row = {}

    for edge in edges:
        row[edge] = []

    return row


def rec_convert(graph, converted, edges, nodes):
    b_row = create_row(edges)

    for node in nodes:
        a_row = graph[node]

        for edge in edges:
            a_hops = a_row[edge]
            b_hops = b_row[edge]

            for hop in a_hops:
                if hop not in b_hops:
                    b_hops.append(hop)

            b_hops.sort()

    converted[nodes] = b_row

    for b_hops in b_row.values():
        if len(b_hops) != 0:
            frozen_b_hops = tuple(b_hops)

            if frozen_b_hops not in converted:
                rec_convert(graph, converted, edges, frozen_b_hops)


def contains_at_lest_one(a, b):
    for i in a:
        if i in b:
            return True

    return False


def print_converted(converted, sigma, start, finals):
    header = [''] + sigma
    body = []

    for nodes, right in converted.items():
        row = []
        left = '->' if start in nodes else ''

        if contains_at_lest_one(finals, nodes):
            left += '*'

        left += str(nodes)
        row.append(left)

        for hops in right.values():
            row.append('[]' if len(hops) == 0 else str(hops))

        body.append(row)

    print(tabulate(body, header, 'pretty'))


def convert(sigma, start, finals, graph):
    converted = {}
    rec_convert(graph, converted, sigma, tuple([start]))
    print_converted(converted, sigma, start, finals)
