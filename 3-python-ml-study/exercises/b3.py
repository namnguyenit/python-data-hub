def sieve_primes_in_range(a, b):
    if a > b:
        temp = a
        a = b
        b = temp

    if b < 2:
        return []

    limit = b

    is_prime = []
    for i in range(0, limit + 1):
        is_prime.append(True)

    is_prime[0] = False
    is_prime[1] = False

    for p in range(2, b + 1):
        if p * p > b:
            break
        if is_prime[p] == True:
            for multiple in range(p * p, b + 1, p):
                is_prime[multiple] = False

    result = []
    start = a
    if start < 2:
        start = 2

    for number in range(start, b + 1):
        if is_prime[number] == True:
            result.append(number)

    return result


if __name__ == "__main__":
    a = int(input("Nhap A: "))
    b = int(input("Nhap B: "))

    primes = sieve_primes_in_range(a, b)
    if primes:
        print("Cac so nguyen to trong khoang [A, B]:")
        for index in range(0, len(primes)):
            print(primes[index], end=" ")
        print()
    else:
        print("Khong co so nguyen to trong khoang [A, B].")