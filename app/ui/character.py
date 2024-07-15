import random
import json


class Character:
    def __init__(self, name, image_paths, thresholds, variant_images=None):
        self.name = name
        self.stages = [{"image": image_paths[0], "threshold": thresholds[0]}]
        for i in range(1, len(thresholds)):
            self.stages.append({"image": image_paths[i], "threshold": thresholds[i]})
        self.current_stage = 0
        self.variant_images = variant_images if variant_images else {}

    def advance_stage(self):
        if self.current_stage < len(self.stages) - 1:
            self.current_stage += 1
        print(f"Advanced to stage: {self.current_stage}")

    def get_image_path(self):
        print("Stage: ", self.current_stage)
        print("Variant_images: ", self.variant_images)
        if self.current_stage in self.variant_images:
            chosen_image = random.choice(self.variant_images[self.current_stage])
            print(f"Chosen variant image: {chosen_image}")
            return chosen_image
        return self.stages[self.current_stage]["image"]

    def get_current_threshold(self):
        return self.stages[self.current_stage]["threshold"]
