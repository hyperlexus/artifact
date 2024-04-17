# def factorial(n):
#     if n == 0:
#         return 1
#     else:
#         result = 1
#         for i in range(1, n+1):
#             result *= i
#         return result
#
# def binomial_coefficient(n, k):
#     return factorial(n) // (factorial(k) * factorial(n-k))
#
# def binomial_percentile(tries, probability):
#     """Calculates luckiness percentile without libraries"""
#     expected_tries = 1 / probability
#
#     if tries <= expected_tries:
#         percentile = 0.5
#     else:
#         # Calculate CDF manually
#         cdf = 0.0
#         for k in range(tries):
#             success_prob = probability**k * (1 - probability)**(tries - k)
#             combination = binomial_coefficient(tries, k)
#             cdf += combination * success_prob
#
#         # Adjust the CDF to reflect a 'luckier' percentile
#         percentile = 1 - cdf
#
#     return percentile
#
# percentile = binomial_percentile(25,0.5)
# print(f"Percentile of luckiness: {percentile:.2f}")

p = 0.98
n = 2
print(1-p**n)