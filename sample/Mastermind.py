class mastermind:
    
    def __init__(self, ans: tuple[int]):
        self.ans = ans
    
    def hint(self, guess: tuple[int]) -> tuple[int]:
        hints = []
        n = len(guess)
        if guess == self.ans:
            return (3)
        
        for i in range(n):
            if guess[i] == self.ans[i]:
                hints.append(2)
                guess[i] = -1
                self.ans[i] = -1
        
        for i in range(n):
            if guess[i] != -1 and guess[i] in self.ans:
                self.ans.remove(guess[i])
                hints.append(1)
        
        return hints