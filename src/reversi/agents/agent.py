class ReversiAgent:
    def __init__(self, policy, width=8, height=8):
        self.width = width
        self.height = height
        self.policy = policy