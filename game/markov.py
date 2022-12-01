# -*- coding: utf-8 -*-
import random

class news_flow():
    def __init__(self, transition_probability0, transition_probability1, rounds):
        self.tpye = [0,1]#分别代表差-0、好-1
        self.tp0 = transition_probability0+random.gauss(0, 0.01)#前一天是坏天，第二天是坏天的概率，加了个高斯分布
        self.tp1 = transition_probability1+random.gauss(0, 0.01)#前一天是好天，第二天是好天的概率，加了个高斯分布
        self.transition_mat = [[self.tp1,1-self.tp1],[1-self.tp0,self.tp0]]#转移矩阵
        self.rounds = rounds+1#轮数
        
    def markov_gen(self):
        markov = [random.choice(self.tpye)]#第一天初始化
        for i in range(1,self.rounds-1):#生成服从Markov Chain的时间序列
            p = random.uniform(0.0,1.0)#使用均匀分布生成概率
            if(markov[i-1]==0):#前一天是坏天
                if(p<self.tp0):
                    markov.append(0)#第i天是坏天
                else:
                    markov.append(1)#第i天是好天
            else:
                if(p<self.tp1):
                    markov.append(1)#第i天是好天
                else:
                    markov.append(0)#第i天是坏天
            self.markov = markov
        return markov#返回一个0-1数组
    
    def news_gen(self):
        self.news_flow = []
        self.news0 = ['坏天新闻0','坏天新闻1']#坏天新闻
        self.news1 = ['好天新闻0','好天新闻1']#好天新闻
        for i in range(self.rounds-1):
            if(self.markov[i]==0):#第i天为坏天
                self.news_flow.append(random.choice(self.news0))
            else:#第i天为好天
                self.news_flow.append(random.choice(self.news1))
        return self.news_flow

if __name__ == '__main__':
    news_markov = news_flow(0.2, 0.3, 15)
    print('Markov Chain:',news_markov.markov_gen())
    print('News Chain:',news_markov.news_gen())
