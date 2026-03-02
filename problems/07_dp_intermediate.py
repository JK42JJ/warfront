# MISSION: 07 | DP | officer
# TITLE: Logistics Optimization — Longest Common Subsequence
# DESC: Identify strategic commonalities using LCS dynamic programming
# ALGO: DP (LCS)
# MODULE: mission_07_dp
# TIME_COMPLEXITY: O(m·n)
# SPACE_COMPLEXITY: O(m·n)
# DIFFICULTY: 4
"""
┌─ LCS ───────────────────────────────────────────────────────────────────────┐
│  1. dp[i][j] = LCS length of seq1[:i] and seq2[:j]                         │
│  2. If chars match: dp[i][j] = dp[i-1][j-1] + 1                            │
│  3. Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])  ← skip one char         │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['seq1'] : list/str — first sequence
# data['seq2'] : list/str — second sequence
# Return: {'length': int, 'lcs': list}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """LCS — find the longest common subsequence of two sequences."""
    s1 = data['seq1']
    s2 = data['seq2']
    m, n = len(s1), len(s2)
    dp   = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                # TODO: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                pass

    # Backtrack to reconstruct LCS
    lcs, i, j = [], m, n
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            lcs.append(s1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1

    return {'length': dp[m][n], 'lcs': lcs[::-1]}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ length == len(lcs)
#   ✅ lcs is a valid subsequence of both seq1 and seq2
# ─────────────────────────────────────────────────────────────────────────────
