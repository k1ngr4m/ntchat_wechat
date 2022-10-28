import datetime
import json
import os
import random


class Ticket:
    def get_random_number(self):
        red_ball = []
        blue_ball = []

        while len(red_ball) < 6:
            red_num = random.randint(1, 33)
            if red_num not in red_ball:
                red_ball.append(red_num)
        red_ball.sort()

        blue_num = random.randint(1, 16)
        blue_ball.append(blue_num)

        # print(red_ball)
        # print(blue_ball)
        return red_ball, blue_ball

    def get_num_and_save(self, from_wxid):
        try:
            red_ball, blue_ball = self.get_random_number()
            ticket = {
                'red_ball': red_ball,
                'blue_ball': blue_ball
            }
            new_data = [{'from_wxid': from_wxid,
                         'ticket_list': [ticket]}]
            print(ticket)
            dir_name = r'data'
            if not os.path.isdir(dir_name):
                os.makedirs(dir_name)

            msg = f'红球号码为：{red_ball}\n蓝球号码为：{blue_ball}'

            date = datetime.date.today().strftime('%Y-%m-%d')
            file_name = fr'data/{date}_ticket.json'
            if not os.path.exists(file_name):
                with open(file_name, 'a', encoding='UTF-8') as a:
                    init_list = json.dumps(new_data, ensure_ascii=False)
                    a.write(init_list)
                    print(init_list)
                    return msg

            with open(file_name, 'r', encoding='utf-8') as a:
                result = json.load(a)

            add = False
            for i in range(len(result)):
                wxid = result[i]['from_wxid']
                if from_wxid == wxid:
                    ticket_list = result[i]['ticket_list']
                    ticket_list.append(ticket)
                    add = True
                    break
            if not add:
                result.append(new_data)

            with open(file_name, 'w', encoding='utf-8') as b:
                res = json.dumps(result, ensure_ascii=False)
                b.write(res)
                print(res)
            return msg
        except Exception as e:
            print(e)

    def run_a_lottery(self, from_wxid):
        try:
            red_res, blue_res = self.get_random_number()
            lucky_ball_msg = f'红球中奖号码：{red_res}。蓝球中奖号码：{blue_res}\n'
            print(lucky_ball_msg)

            msg = ''

            date = datetime.date.today().strftime('%Y-%m-%d')
            file_name = fr'data/{date}_ticket.json'
            with open(file_name, 'r', encoding='utf-8') as a:
                buy_data = json.load(a)

            for i in range(len(buy_data)):
                wxid = buy_data[i]['from_wxid']
                ticket_list = buy_data[i]['ticket_list']
                if wxid == from_wxid:
                    for j in range(len(ticket_list)):

                        red_lucky_count = 0
                        blue_lucky_count = 0

                        red_ball_buy = ticket_list[j]['red_ball']
                        blue_ball_buy = ticket_list[j]['blue_ball']

                        for red_result_item in red_res:
                            for red_buy_item in red_ball_buy:
                                if red_result_item == red_buy_item:
                                    red_lucky_count += 1

                        if blue_res == blue_ball_buy:
                            blue_lucky_count = 1

                        buy_msg = f'您购买的红色球：{red_ball_buy}。您购买的蓝色球：{blue_ball_buy}。\n'
                        prize_count_msg = f'您中的红球数{red_lucky_count}。您中的蓝球数{blue_lucky_count}。\n'
                        # print(f'您购买的红色球：{red_ball_buy}。您购买的蓝色球：{blue_ball_buy}')
                        # print(f'您中的红球数{red_lucky_count}。您中的蓝球数{blue_lucky_count}')

                        prize = self.situations_of_winning(red_lucky_count, blue_lucky_count)
                        if prize != -1:
                            prize_msg = f'恭喜您，中了{prize}等奖！\n'
                        else:
                            prize_msg = '很遗憾，您没有中奖。\n'

                        msg = msg + buy_msg + prize_msg
                        # print(msg)

                self.delete_ticket(from_wxid)
                print("!!!!!!")
                print(lucky_ball_msg + msg)
                return lucky_ball_msg + msg
        except Exception as e:
            print(e)
            return e

    def situations_of_winning(self, red_lucky_count, blue_lucky_count):
        if red_lucky_count == 6 and blue_lucky_count == 1:
            luck_level = 1  # 一等奖（6+1）
        elif red_lucky_count == 6 and blue_lucky_count == 0:
            luck_level = 2
        elif red_lucky_count == 5 and blue_lucky_count == 1:
            luck_level = 3
        elif red_lucky_count == 5 and blue_lucky_count == 0:
            luck_level = 4
        elif red_lucky_count == 4 and blue_lucky_count == 1:
            luck_level = 4
        elif red_lucky_count == 4 and blue_lucky_count == 0:
            luck_level = 5
        elif red_lucky_count == 3 and blue_lucky_count == 1:
            luck_level = 5
        elif red_lucky_count == 2 and blue_lucky_count == 1:
            luck_level = 6
        elif red_lucky_count == 1 and blue_lucky_count == 1:
            luck_level = 6
        elif red_lucky_count == 0 and blue_lucky_count == 1:
            luck_level = 6
        else:
            luck_level = -1
        return luck_level

    def delete_ticket(self, from_wxid):
        date = datetime.date.today().strftime('%Y-%m-%d')
        file_name = fr'data/{date}_ticket.json'
        with open(file_name, 'r', encoding='utf-8') as a:
            buy_data = json.load(a)

        for i in range(len(buy_data)):
            wxid = buy_data[i]['from_wxid']
            if wxid == from_wxid:
                buy_data.remove(buy_data[i])

    def bet_one(self):
        red_ball_buy, blue_ball_buy = self.get_random_number()
        print(f'您购买的红色球：{red_ball_buy}。您购买的蓝色球：{blue_ball_buy}')
        red_ball_res, blue_ball_res = self.get_random_number()
        print(f'红球中奖号码：{red_ball_res}。蓝球中奖号码：{blue_ball_res}\n')

        red_lucky_count = 0
        blue_lucky_count = 0

        for red_result_item in red_ball_res:
            for red_buy_item in red_ball_buy:
                if red_result_item == red_buy_item:
                    red_lucky_count += 1

        if blue_ball_res == blue_ball_buy:
            blue_lucky_count = 1

        prize = self.situations_of_winning(red_lucky_count, blue_lucky_count)
        if prize != -1:
            prize_msg = f'恭喜您，中了{prize}等奖！\n'
        else:
            prize_msg = '很遗憾，您没有中奖。\n'
        print(prize_msg)


if __name__ == '__main__':
    # Ticket().get_num_and_save('2')
    # Ticket().run_a_lottery('2')
    Ticket().bet_one()
