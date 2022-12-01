from otree.api import *
import random
import time

doc = ' 实验流程描述文档 '

'''
根据马尔科夫链生成十五天的新闻数据
'''


class news_flow():
    def __init__(self, transition_probability0, transition_probability1, rounds):
        self.tpye = [0, 1]  # 分别代表差-0、好-1
        self.tp0 = transition_probability0 + random.gauss(0, 0.01)  # 前一天是坏天，第二天是坏天的概率，加了个高斯分布
        self.tp1 = transition_probability1 + random.gauss(0, 0.01)  # 前一天是好天，第二天是好天的概率，加了个高斯分布
        self.transition_mat = [[self.tp1, 1 - self.tp1], [1 - self.tp0, self.tp0]]  # 转移矩阵
        self.rounds = rounds + 1  # 轮数

    def markov_gen(self):  # 生成新闻类别序列
        markov = [random.choice(self.tpye)]  # 第一天初始化
        for i in range(1, self.rounds - 1):  # 生成服从Markov Chain的时间序列
            p = random.uniform(0.0, 1.0)  # 使用均匀分布生成概率
            if (markov[i - 1] == 0):  # 前一天是坏天
                if (p < self.tp0):
                    markov.append(0)  # 第i天是坏天
                else:
                    markov.append(1)  # 第i天是好天
            else:
                if (p < self.tp1):
                    markov.append(1)  # 第i天是好天
                else:
                    markov.append(0)  # 第i天是坏天
            self.markov = markov
        return markov  # 返回一个0-1数组

    def news_gen(self):  # 生成新闻序列
        self.news_flow = []
        self.news0 = ['坏天新闻0', '坏天新闻1']  # 坏天新闻
        self.news1 = ['好天新闻0', '好天新闻1']  # 好天新闻
        for i in range(self.rounds - 1):
            if (self.markov[i] == 0):  # 第i天为坏天
                self.news_flow.append(random.choice(self.news0))
            else:  # 第i天为好天
                self.news_flow.append(random.choice(self.news1))
        return self.news_flow

    def daily_news(self):
        markov_chain = self.markov_gen()  # 新闻类别序列
        news_chain = self.news_gen()  # 新闻序列
        # 将生成结果写回文档
        with open('data.txt', 'a+') as f:
            f.writelines('\n\n')
            time_now = str(time.time()) + '\n'
            f.write(time_now)
            f.write('markov_chain: ')
            f.writelines(str(markov_chain))
            f.write('\nnews chain: ')
            f.writelines(str(news_chain))
            f.writelines('\n\n')
        return markov_chain, news_chain


MKV = news_flow(0.2, 0.3, 15)
markov_chain, news_chain = MKV.daily_news()
news_chain.reverse()
print(news_chain)
'''
常量部分
'''


class Constants(BaseConstants):
    name_in_url = 'public_goods_simple'  # 类别URL
    players_per_group = 3  # 每组成员数目
    '''
    是不是还有一个组别的数目
    '''
    num_rounds = 1  # 一共循环次数，由于程序设计采用串行设计，因此只需要进行一轮
    endowment = cu(100)  # 初始经济
    multiplier = 1.8
    '''
    初始商品数目
    '''
    a_num = 15
    b_num = 15
    c_num = 15
    '''
    初始商品价格
    '''
    a_price = 15
    b_price = 15
    c_price = 15
    '''
    熔断阈值
    '''
    fusing_threshold = 0.1
    group_num = 2
    news_chain = news_chain


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    '''
    新闻
    '''
    daily_news = models.StringField(initial=news_chain[0])
    '''
    商品数目
    '''
    a_num = models.IntegerField(initial=Constants.a_num, label='商品A数目', min=0, max=Constants.a_num * 3)
    b_num = models.IntegerField(initial=Constants.b_num, label='商品B数目', min=0, max=Constants.a_num * 3)
    c_num = models.IntegerField(initial=Constants.c_num, label='商品C数目', min=0, max=Constants.a_num * 3)
    '''
    商品价格
    '''
    a_price = models.FloatField(initial=10, label='商品A的价格', min=0)
    b_price = models.FloatField(initial=10, label='商品B的价格', min=0)
    c_price = models.FloatField(initial=10, label='商品C的价格', min=0)
    '''
    熔断情况
    '''
    all_fusing = models.FloatField(initial=-1)
    a_fusing = models.FloatField(initial=-1)  # A 商品是否熔断
    b_fusing = models.FloatField(initial=-1)
    c_fusing = models.FloatField(initial=-1)


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment, label="How much will you contribute?"
    )

    # 所属阵营
    BelongToWhichGroup = models.BooleanField()

    currency = models.FloatField(initial=100, label='您当前金钱')
    a_num = models.IntegerField(initial=Constants.a_num, label='您持有的商品A数目', min=0, max=Group.a_num)
    b_num = models.IntegerField(initial=Constants.b_num, label='您持有的商品B数目', min=0, max=Group.b_num)
    c_num = models.IntegerField(initial=Constants.c_num, label='您持有的商品C数目', min=0, max=Group.c_num)
    a_price = models.FloatField(label='您计划出售商品A的价格', min=0)
    b_price = models.FloatField(label='您计划出售商品B的价格', min=0)
    c_price = models.FloatField(label='您计划出售商品C的价格', min=0)
    a_sell = models.IntegerField(label='您计划出售商品A的数目', min=0)
    b_sell = models.IntegerField(label='您计划出售商品B的数目', min=0)
    c_sell = models.IntegerField(label='您计划出售商品C的数目', min=0)
    a_buy = models.IntegerField(label='您计划购买商品A的数目', min=0)
    b_buy = models.IntegerField(label='您计划购买商品B的数目', min=0)
    c_buy = models.IntegerField(label='您计划购买商品C的数目', min=0)
    news = models.StringField(initial=news_chain[0])


# 价格限制
def price(group: Group):
    return


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (
            group.total_contribution * Constants.multiplier / Constants.players_per_group
    )
    for p in players:
        p.payoff = Constants.endowment - p.contribution + group.individual_share


# 今日新闻
def daily_news(group: Group):
    '''
    读入上一轮数据
    '''
    '''
    prev_player = player.in_round(player.round_number - 1)  # 上一个环节的对象
    prev_group = group.in_round(group.round_number - 1)  # 上一个环节的组
    if not prev_player:
        # 若非空，则传递
        player.a_num = prev_player.a_num
        player.b_num = prev_player.b_num
        player.c_num = prev_player.c_num
        player.BelongToWhichGroup = prev_player.BelongToWhichGroup
        player.currency = prev_player.currency
    else:
        pass

    if not prev_group:
        group.a_num = prev_group.a_num
        group.b_num = prev_group.b_num
        group.c_num = prev_group.c_num
        group.a_price = prev_group.a_price
        group.b_price = prev_group.b_price
        group.c_price = prev_group.c_price
        group.a_fusing = prev_group.a_fusing
        group.b_fusing = prev_group.b_fusing
        group.c_fusing = prev_group.c_fusing
        group.all_fusing = prev_group.all_fusing
    '''
    '''
    读入新闻
    '''

    players = group.get_players()
    for p in players:
        p.news = news_chain[-1]  # 最后一条新闻，因为是逆序表示，所以是当前轮数的新闻
    # print(news_chain[-1])
    news_chain.pop()


# 购买


def purchase(group: Group):
    players = group.get_players()
    '''
    熔断与否可以在html页面中体现
    '''
    p = Player
    # 判断上次操作行为是否造成熔断
    # 商品A
    Group.a_fusing = (p.a_price - Group.a_price) * (p.a_price - Group.a_price) - (
            Constants.fusing_threshold * Group.a_price) * (Constants.fusing_threshold * Group.a_price)  # 大于0出现熔断现象
    # 商品B
    Group.b_fusing = (p.b_price - Group.b_price) * (p.b_price - Group.b_price) - (
            Constants.fusing_threshold * Group.b_price) * (Constants.fusing_threshold * Group.b_price)  # 大于0出现熔断现象
    # 商品C
    Group.c_fusing = (p.c_price - Group.c_price) * (p.c_price - Group.c_price) - (
            Constants.fusing_threshold * Group.c_price) * (Constants.fusing_threshold * Group.c_price)  # 大于0出现熔断现象

    '''
    for p in players:
        # 判断上次操作行为是否造成熔断
        # 商品A
        if bool((p.a_price - Group.a_price) >= Constants.fusing_threshold * Group.a_price):
            Group.a_fusing = True
        # 商品B
        if (p.b_price - Group.b_price) >= Constants.fusing_threshold * Group.b_price:
            Group.b_fusing = True
        # 商品C
        if (p.c_price - Group.c_price) >= Constants.fusing_threshold * Group.c_price:
            Group.c_fusing = True
    # 完全熔断
    Group.all_fusing = Group.a_fusing and Group.b_fusing and Group.c_fusing
    '''
    # 在非熔断的情况下，结算商品
    # 结算出售商品的客户
    a_price = [p.a_price for p in players]  # A商品价格
    b_price = [p.b_price for p in players]  # B商品价格
    c_price = [p.c_price for p in players]  # C商品价格
    a_sell = [p.a_sell for p in players]  # A商品数目
    b_sell = [p.b_sell for p in players]  # B商品数目
    c_sell = [p.c_sell for p in players]  # C商品数目
    if Group.all_fusing:
        pass
    else:
        if Group.a_fusing:
            pass
        else:
            # 结算A商品
            average_price = Group.a_price * Group.a_num
            for i in range(len(a_price)):
                average_price = average_price + a_price[i] * a_sell[i]
                pass
            Group.a_num = sum(a_sell) + Group.a_num
            Group.a_price = average_price / Group.a_num
            for p in players:
                p.currency = p.a_price * p.a_sell
            pass
        if Group.b_fusing:
            pass
        else:
            # 结算B商品
            average_price = Group.b_price * Group.b_num
            for i in range(len(b_price)):
                average_price = average_price + b_price[i] * b_sell[i]
                pass
            Group.b_num = sum(b_sell) + Group.b_num
            Group.b_price = average_price / Group.b_num
            for p in players:
                p.currency = p.b_price * p.b_sell
            pass
        if Group.c_fusing:
            pass
        else:
            # 结算C商品
            average_price = Group.c_price * Group.c_num
            for i in range(len(c_price)):
                average_price = average_price + c_price[i] * c_sell[i]
                pass
            Group.c_num = sum(c_sell) + Group.c_num
            Group.c_price = average_price / Group.c_num
            for p in players:
                p.currency = p.c_price * p.c_sell
            pass
    # 结算购买商品的客户
    # 还没写捏


# PAGES
'''
牢记一点，在页面中做数据传输
'''


class Contribute(Page):
    # 填写表单的界面
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    '''
    熔断与否可以在html页面中体现
    '''
    '''
    for p in players:
        # 判断上次操作行为是否造成熔断
        # 商品A
        if bool((p.a_price - Group.a_price) >= Constants.fusing_threshold * Group.a_price):
            Group.a_fusing = True
        # 商品B
        if (p.b_price - Group.b_price) >= Constants.fusing_threshold * Group.b_price:
            Group.b_fusing = True
        # 商品C
        if (p.c_price - Group.c_price) >= Constants.fusing_threshold * Group.c_price:
            Group.c_fusing = True
    # 完全熔断
    Group.all_fusing = Group.a_fusing and Group.b_fusing and Group.c_fusing
    '''

    # 完全熔断
    # Group.all_fusing = 1

    # 所有玩家投票之后的等待界面
    after_all_players_arrive = purchase


class Results(Page):
    # 最终结果界面
    pass


class waitpage_1st(WaitPage):
    def after_all_players_arrive(self):
        pass


class waitpage(WaitPage):
    after_all_players_arrive = daily_news


class WelcomePage(WaitPage):
    form_model = 'group'


class Stage1(Page):
    form_model = 'player'
    form_fields = ['a_price', 'a_sell', 'b_price', 'b_sell', 'c_price', 'c_sell']


class welcome_to_game(Page):
    pass


class bye_bye(Page):
    pass


page_sequence = [welcome_to_game,
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 1
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 2
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 3
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 4
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 5
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 6
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 7
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 8
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 9
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 10
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 11
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 12
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 13
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 14
                 waitpage, WelcomePage, Stage1, ResultsWaitPage, Results,  # 15
                 bye_bye]
