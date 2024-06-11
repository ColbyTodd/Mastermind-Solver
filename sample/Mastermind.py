class Mastermind:
    
    def __init__(self, ans: tuple[int]):
        self.ans = ans
    
    def hint(self, guess: tuple[int]) -> tuple[int]:
        hints = []
        guess = list(guess)
        ans =  list(self.ans)
        n = len(guess)
        if guess == ans:
            # This means the answer has been found
            return ((2,) * n)
        
        for i in range(n):
            if guess[i] == ans[i]:
                hints.append(2)
                guess[i] = -1
                ans[i] = -1
        
        for i in range(n):
            if guess[i] != -1 and guess[i] in ans:
                ans.remove(guess[i])
                hints.append(1)
        
        hints.extend([0] * (n - len(hints)))
        
        return tuple(hints)