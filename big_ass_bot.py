import random
import numpy as np
from ..bot_control import Move

class BigAssBot:

    def __init__(self):
        self.target = None
        self.distance = 0

    def get_name(self):
        return "Big Ass Bot"

    def get_contributor(self):
        return "Mahmoud"

    def build_scores(self, enemies):
        scores = dict({})
        for enemy in enemies:
            scores[enemy["id"]] = (enemy["id"] - self.id) % 3
        scores[self.id] = 0
        scores[0] = 2
        return scores

    def evaluate(self, grid, point, scores):
        print(scores)
        
        p1 = [np.max([point[0] - 2, 0]), np.max([point[1] - 2, 0])]
        p2 = [np.min([point[0] + 2, grid.shape[0] - 1]), np.min([point[1] + 2, grid.shape[0] - 1])]

        score = 0
        for y in range(p1[0], p2[0] + 1):
            for x in range(p1[1], p2[1] + 1):
                score += scores[grid[y][x]]
        
        return score
    
    def left_point(self, grid):
        return [self.position[0], np.max([self.position[1] - 1, 0])]

    def right_point(self, grid):
        return [self.position[0], np.min([self.position[1] + 1, grid.shape[1]])]

    def up_point(self, grid):
        return [np.min([self.position[0] + 1, grid.shape[0]]), self.position[1]]

    def down_point(self, grid):
        return [np.max([self.position[0] - 1, 0]), self.position[1]]

    def eval_single(self, grid, point, scores):
        return scores[grid[point[1]][point[0]]]

    def determine_next_move(self, grid, enemies, game_info):
        # Chooses a random target location, and moves there.
        # Once it's there, choose a new location.

        # Create a target in storage if doesn't exist
        if  self.target is None:
            self.target = np.zeros_like(self.position)

        scores = self.build_scores(enemies)

        ############### Make global decision ################
        # If reached the target find a new target
        if np.array_equal(self.position, self.target):
            ##### Generate 4 random targets in 4 quarters
            ## 0 - Pi/2
            q1 = (random.randint((grid.shape[1] - 1) // 2, grid.shape[1] - 1), 
                  random.randint((grid.shape[1] - 1) // 2, grid.shape[1] - 1))
            score = self.evaluate(grid, q1, scores)
            self.target = q1
            ## P/2 - P
            q2 = (random.randint((grid.shape[1] - 1) // 2, grid.shape[1] - 1), 
                  random.randint(0, (grid.shape[1] - 1) // 2))
            score2 = self.evaluate(grid, q2, scores)
            if(score2 > score):
                score = score2
                self.target = q2
            ## P - 3P/2
            q3 = (random.randint(0, (grid.shape[1] - 1) // 2), 
                  random.randint(0, (grid.shape[1] - 1) // 2))
            score3 = self.evaluate(grid, q3, scores)
            if(score3 > score):
                score = score3
                self.target = q3
            ## 3P/2 - 2P
            q4 = (random.randint(0, (grid.shape[1] - 1) // 2), 
                  random.randint((grid.shape[1] - 1) // 2, grid.shape[1] - 1))
            score4 = self.evaluate(grid, q4, scores)
            if(score4 > score):
                score = score4
                self.target = q4

        # Move in direction of target:
        move = Move.DOWN
        if self.target[0] > self.position[0]:
            move = Move.RIGHT
        elif self.target[0] < self.position[0]:
            move = Move.LEFT
        elif self.target[1] > self.position[1]:
            move = Move.UP
   
        # ############### Make local decision ################
        # up_score = self.eval_single(grid, self.up_point(grid), scores)
        # right_score = self.eval_single(grid, self.right_point(grid), scores)
        # left_score = self.eval_single(grid, self.left_point(grid), scores)
        # down_score = self.eval_single(grid, self.down_point(grid), scores)
        # match move:
        #     case Move.DOWN:
        #         if right_score >= down_score + 1:
        #             move = Move.RIGHT
        #         elif left_score >= down_score + 1:
        #             move = Move.LEFT
        #     case Move.UP:
        #         if right_score >= up_score + 1:
        #             move = Move.RIGHT
        #         elif left_score >= up_score + 1:
        #             move = Move.LEFT
        #     case Move.RIGHT:
        #         if down_score >= right_score + 1:
        #             move = Move.DOWN
        #         elif up_score >= right_score + 1:
        #             move = Move.UP
        #     case Move.LEFT:
        #         if down_score >= left_score + 1:
        #             move = Move.DOWN
        #         elif up_score > left_score + 1:
        #             move = Move.UP                
        
        return move

