import random
from BaseAI import BaseAI
import time
import math
max_level=4
board_size=4
heuristic_weight=[0.3,0.3,0.005]
class IntelligentAgent(BaseAI):

    def getMove(self, grid):
        maxUtility=-math.inf
        alpha=-float('inf')
        beta=float('inf')
        moves=grid.getAvailableMoves()
        chosen_direction=moves[0][0] if moves else 0
        for move in moves:
            utility=self.Expectiminimax(move[1],1,1,alpha,beta)
            if utility>maxUtility:
                maxUtility=utility
                chosen_direction=move[0]
            if maxUtility>=beta:
                break
            if maxUtility>alpha:
                alpha=maxUtility
        return chosen_direction

    def Expectiminimax(self,grid,level,probability,alpha,beta):
        if level>=max_level-1:
            return self.heuristic(grid)
        minUtility=float('inf')
        for i in range(board_size):
            for j in range(board_size):
                if grid.map[i][j]==0:
                    utility=0
                    grid.map[i][j]=4
                    utility+=0.1*self.maximize(grid,level+1,probability*0.1,alpha,beta)
                    grid.map[i][j]=2
                    utility+=0.9*self.maximize(grid,level+1,probability*0.9,alpha,beta)
                    grid.map[i][j]=0
                    if utility<minUtility:
                        minUtility=utility
                    if minUtility<=alpha:
                        break
                    if minUtility<beta:
                        beta=minUtility
        return minUtility
    def maximize(self,grid,level,probability,alpha,beta):
        maxUtility=-float('inf')
        moves=grid.getAvailableMoves()
        for move in moves:
            utility=self.Expectiminimax(move[1],level+1,probability,alpha,beta)
            if utility>maxUtility:
                maxUtility=utility
            if maxUtility>=beta:
                break
            if maxUtility>alpha:
                alpha=maxUtility
        return maxUtility
    def heuristic(self,grid):
        empty_state=len(grid.getAvailableCells())
        monotonicity=self.monotonicity(grid)
        smoothness=self.smoothness(grid)
        total_heuristic=empty_state*heuristic_weight[0]+monotonicity*heuristic_weight[1]+smoothness*heuristic_weight[2]
        return total_heuristic
    def monotonicity(self,grid):
        total=0
        for i in range(4):
            row=grid.map[i]
            col=[grid.getCellValue((j,i))for j in range(4)]
            sorted_row=sorted(row[:])
            sorted_col=sorted(col[:])
            #check montonicity
            if sorted_col==col or sorted_col==col[::-1]:
                total+=1
            if sorted_row==row or sorted_row==row[::-1]:
                total+=1
            #check corner
            if row[0]==max(row) or row[0]==min(row):
                total+=1
            if row[3]==max(row) or row[3]==min(row):
                total+=1
            if col[0]==max(col) or col[0]==min(col):
                total+=1
            if col[3]==max(col) or col[3]==min(col):
                total+=1
        return total
    def smoothness(self,grid):
        total=0
        neighbor_pair=set()
        for i in range(4):
            for j in range(4):
                neighbors=[(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
                for neighbor in neighbors:
                    if ((i, j), neighbor) in neighbor_pair:
                        continue
                    x=neighbor[0]
                    y=neighbor[1]
                    neighbor_pair.add(((i, j), neighbor))
                    try:
                        a=grid.map[x][y] if grid else 2
                        b=grid.map[i][j] if grid else 2
                        total-=abs(a-b)
                    except:
                        total+=0
        return total