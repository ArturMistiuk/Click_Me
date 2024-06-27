class Character:
    def __init__(self):
        self.stages = [
            {"image": "resources/images/character1_stage1.png", "threshold": 0, "multiplier": 1},
            {"image": "resources/images/character1_stage2.png", "threshold": 100, "multiplier": 3},
            # Добавьте остальные стадии здесь
        ]
        self.current_stage = 0

    def get_current_stage(self):
        return self.stages[self.current_stage]

    def advance_stage(self):
        if self.current_stage < len(self.stages) - 1:
            self.current_stage += 1
