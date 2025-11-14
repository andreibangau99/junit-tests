from itertools import product
import math

def optimized_count_invertible_2x2_matrices(N):
    invertible_count = 0

    # Generam toate 4-tuplele (a, b, c, d) posibile, pentru a, b, c, d <= N
    # Pentru a verifica daca o matrice este inversabila, verificam daca gcd(det, N) == 1
    for a, b, c, d in product(range(N), repeat=4):
        determinant = (a * d - b * c) % N
        if math.gcd(determinant, N) == 1:
            invertible_count += 1

    return invertible_count

invertible_keys_N13 = optimized_count_invertible_2x2_matrices(13)
invertible_keys_N26 = optimized_count_invertible_2x2_matrices(26)
invertible_keys_N256 = optimized_count_invertible_2x2_matrices(256)

print(f'N=13: {invertible_keys_N13}\nN=26: {invertible_keys_N26}\nN=256: {invertible_keys_N256}')
