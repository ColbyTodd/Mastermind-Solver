class Mastermind:
    
    def __init__(self, ans: tuple[int]):
        self.ans = ans
    
    def hint(self, guess: tuple[int]) -> tuple[int]:
        hints = ()
        if guess == self.ans:
            return (3)
        
        for i in range(len(guess)):
            if guess[i] == self.ans[i]:
                hints += (2)
            
            