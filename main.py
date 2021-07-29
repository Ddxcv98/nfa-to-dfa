import json
import tabulate

from argparse import ArgumentParser
from collections import deque
from name_mapper import NameMapper
from tabulate import tabulate as table


def nfa_to_dfa(sigma, delta, q0):
    initial_state = {symbol: frozenset(states) for symbol, states in delta[q0].items()}
    dfa = {frozenset([q0]): initial_state}
    queue = deque(initial_state.values())

    while len(queue) != 0:
        q_set = queue.popleft()

        if not q_set or q_set in dfa:
            continue

        edges = {s: set() for s in sigma}

        for q in q_set:
            for s, p_set in delta[q].items():
                edges[s].update(p_set)

        frozen_edges = {s: frozenset(edge) for s, edge in edges.items()}
        dfa[q_set] = frozen_edges
        queue.extend(frozen_edges.values())

    return dfa


def hopcroft(sigma, delta, f):
    p = {f, frozenset(filter(lambda q: q not in f, delta))}
    w = {f}

    while len(w) != 0:
        a = w.pop()

        for c in sigma:
            x = frozenset(filter(lambda q: delta[q][c] in a, delta))

            for y in p.copy():
                intersection = x.intersection(y)
                difference = y.difference(x)

                if not intersection or not difference:
                    continue

                p.remove(y)
                p.add(intersection)
                p.add(difference)

                if y in w:
                    w.remove(y)
                    w.add(intersection)
                    w.add(difference)
                elif len(intersection) <= len(difference):
                    w.add(intersection)
                else:
                    w.add(difference)

    return p


def minimize(sigma, delta, f):
    merged_states = hopcroft(sigma, delta, f)
    minimized = {}

    for q_set in merged_states:
        q = next(iter(q_set))
        edges = {}

        for symbol in sigma:
            p = delta[q][symbol]

            if p:
                edges[symbol] = next(filter(lambda m: p in m, merged_states))
            else:
                edges[symbol] = frozenset()

        minimized[q_set] = edges

    return minimized


def get_name(mapper, q, convert):
    if not q:
        return None

    if convert:
        return mapper.get_name(q)

    return f"{{{', '.join(sorted(q))}}}"


def convert_dfa_names(delta, q0, f, convert):
    mapper = NameMapper()
    delta2 = {}
    q02 = None
    f2 = set()

    for q_set, edges in delta.items():
        q2 = get_name(mapper, q_set, convert)
        delta2[q2] = {s: get_name(mapper, p_set, convert) for s, p_set in edges.items()}

        if q0 in q_set:
            q02 = q2

        if any(q in f for q in q_set):
            f2.add(q2)

    return delta2, q02, frozenset(f2)


def get_row(q, q0, f):
    prefix = ''

    if q == q0:
        prefix += '->'

    if q in f:
        prefix += '*'

    if prefix:
        prefix += ' '

    return [prefix + q + ' ' * len(prefix)]


def print_dfa(sigma, delta, q0, f):
    headers = [''] + sigma
    body = []

    for q, edges in delta.items():
        row = get_row(q, q0, f)

        for p in edges.values():
            row.append(p if p else '-')

        body.append(row)

    print(table(body, headers, 'pretty'))


def main():
    parser = ArgumentParser()
    parser.add_argument('input', help='File to parse')
    parser.add_argument('--nfa', action='store_true', help='flag used when the input is a NFA')
    parser.add_argument('--dfa', action='store_true', help='flag used when the input is a DFA')
    parser.add_argument('--preserve-nfa-sets', action='store_true', help='keep the original sets when converting to a DFA')
    parser.add_argument('--preserve-dfa-sets', action='store_true', help='keep the original sets when minimizing the DFA')
    parser.add_argument('--minimize', action='store_true', help='get the minimized dfa; not needed when the input is a DFA')
    args = parser.parse_args()

    if args.nfa == args.dfa:
        print('exactly one of the following arguments should be present: --nfa, --dfa')
        exit(-1)

    with open(args.input) as file:
        fa = json.load(file)

    sigma = fa['Σ']
    q0 = fa['q0']
    delta = fa['Δ']
    f = frozenset(fa['F'])

    if args.nfa:
        dfa = nfa_to_dfa(sigma, delta, q0)
        dfa2, q02, f2 = convert_dfa_names(dfa, q0, f, not args.preserve_nfa_sets)

        if args.minimize:
            minimized = minimize(sigma, dfa2, f2)
            dfa3, q03, f3 = convert_dfa_names(minimized, q02, f2, not args.preserve_dfa_sets)
            print_dfa(sigma, dfa3, q03, f3)
        else:
            print_dfa(sigma, dfa2, q02, f2)
    else:
        minimized = minimize(sigma, delta, f)
        dfa2, q02, f2 = convert_dfa_names(minimized, q0, f, not args.preserve_dfa_sets)
        print_dfa(sigma, dfa2, q02, f2)


if __name__ == '__main__':
    tabulate.PRESERVE_WHITESPACE = True
    main()
