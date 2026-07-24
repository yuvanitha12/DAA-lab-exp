"""
Experiment No. 6
Optimal Cost Computation in Matrix Chain Multiplication using DP Technique
CS5303 - Design and Analysis of Algorithms

Extended version: multiple sample inputs + runtime measurement +
theoretical time/space complexity analysis.
"""

import time
import sys


def matrix_chain_order(dims):
    
    n = len(dims) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    for l in range(2, n + 1):          # chain length
        for i in range(1, n - l + 2):  # start index
            j = i + l - 1              # end index
            m[i][j] = float('inf')
            for k in range(i, j):      # split point
                cost = m[i][k] + m[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    return m, s


def print_optimal_parens(s, i, j):
    if i == j:
        return f'A{i}'
    k = s[i][j]
    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)
    return f'({left} x {right})'


def print_dp_table(m, n):
    print('\nDP Cost Table m[i][j]:')
    print(f'{"":>6}', end='')
    for j in range(1, n + 1):
        print(f'A{j:>8}', end='')
    print()
    for i in range(1, n + 1):
        print(f'A{i:<5}', end='')
        for j in range(1, n + 1):
            if j < i:
                print(f'{"---":>9}', end='')
            else:
                print(f'{m[i][j]:>9}', end='')
        print()


def approx_space_bytes(n):
    """Rough estimate of space used by the two (n+1)x(n+1) int tables."""
    entries = 2 * (n + 1) * (n + 1)
    return entries * sys.getsizeof(0)


def run_case(label, dims):
    n = len(dims) - 1
    print('=' * 60)
    print(label)
    print('=' * 60)
    print('Matrix Dimensions:')
    for i in range(n):
        print(f'  A{i + 1}: {dims[i]} x {dims[i + 1]}')

    start = time.perf_counter()
    m, s = matrix_chain_order(dims)
    elapsed = time.perf_counter() - start

    print(f'\nMinimum scalar multiplications: {m[1][n]}')
    print(f'Optimal parenthesization: {print_optimal_parens(s, 1, n)}')
    print_dp_table(m, n)

    print(f'\nMatrices in chain (n): {n}')
    print(f'Time complexity   : O(n^3)  [theoretical]')
    print(f'Space complexity  : O(n^2)  [theoretical]')
    print(f'Measured runtime  : {elapsed * 1000:.4f} ms')
    print(f'Estimated table memory : {approx_space_bytes(n)} bytes '
          f'(~{approx_space_bytes(n) / 1024:.2f} KB)')
    print()
    return n, elapsed


if __name__ == '__main__':
    # Different sample sets (not the manual's original 4-matrix example)
    sample_sets = {
        'Sample 1: 3 matrices': [5, 10, 3, 12],
        'Sample 2: 5 matrices': [40, 20, 30, 10, 30, 15],
        'Sample 3: 6 matrices (larger)': [30, 35, 15, 5, 10, 20, 25],
    }

    results = []
    for label, dims in sample_sets.items():
        n, elapsed = run_case(label, dims)
        results.append((n, elapsed))

    print('=' * 60)
    print('Summary: chain length (n) vs measured runtime')
    print('=' * 60)
    print(f'{"n (matrices)":>15} {"Runtime (ms)":>15}')
    for n, elapsed in results:
        print(f'{n:>15} {elapsed * 1000:>15.4f}')

    print('\nINFERENCE')
    print('As the number of matrices n grows, runtime grows roughly as n^3 '
          '(cubic), matching the theoretical O(n^3) time complexity, since '
          'the algorithm has three nested loops over chain length, start '
          'index, and split point. Memory usage grows as O(n^2) because of '
          'the two n x n tables (m and s) used to store subproblem costs '
          'and split points.')
