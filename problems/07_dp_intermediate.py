# MISSION: 07 | DP | officer
# TITLE: Logistics Optimization — DP Longest Common Subsequence
# DESC: Identify strategic commonalities using Longest Common Subsequence (LCS)
# ALGO: DP (LCS)
# MODULE: mission_07_dp
def solve(data):
    s1 = data['seq1']
    s2 = data['seq2']
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                # TODO: dp[i][j] = max(Up, Left)
                pass
    # backtracking LCS Reconstruction
    lcs, i, j = [], m, n
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            lcs.append(s1[i-1]); i -= 1; j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    return {'length': dp[m][n], 'lcs': lcs[::-1]}

# --- Execution Block ---
