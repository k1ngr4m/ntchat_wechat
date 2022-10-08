# -*- coding: utf-8 -*-
import random
import re

import api
from api import op_gg
from api.free import FreeApi
from api.muxiaoguo import MuxiaoguoApi
from api.qingyunke import get_reply
from api.tianapi import TianApi
from api.wanplus import WanPlus
from csgo.csgo import Csgo

from base.base import BaseFunc
from game import mine
from game.ticket import Ticket


class Reply(BaseFunc):
    def get_reply(self, bf, wechat, msg, from_wxid, room_wxid, at_user_list):

        # ckd说的话
        if from_wxid == self.ckd_id:
            self.personal_statement(wechat, room_wxid, from_wxid, msg)

        self.others_statement(wechat, room_wxid, from_wxid, at_user_list, msg, bf)

    def personal_statement(self, wechat, room_wxid, from_wxid, msg):
        if msg == 'get_room_member_wxid':
            self.get_room_member_wxid(wechat, room_wxid)
        elif 'add_money' in msg:
            add_money = msg.split(' ')[1]
            Csgo().add_money(from_wxid, add_money)
            msg_1 = f'已为您添加{add_money}元。\n'
            print()
            msg_2 = Csgo().check_balance(from_wxid)
            msg = msg_1 + msg_2
            self.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)
        elif 'set_answer' in msg:
            temp = self.delete_head(msg, 'set_answer ')
            self.answer = temp
            self.send_textmsg(wechat, room_wxid, from_wxid, self.answer, self.answer)
            return

    def others_statement(self, wechat, room_wxid, from_wxid, at_user_list, msg, bf):
        nickname = "@菲菲\u2005"
        # 大家说的话
        if '电影' in msg and self.movie_signal:
            res = '买电影票找@崔崔\u2005'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
            self.movie_signal = False

        elif '@菲菲\u2005好的！' in msg:
            self.movie_signal = True
            self.cdkey_signal = True
            res = '嘿嘿！'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif msg == self.answer and self.cdkey_signal:
            msg = f'恭喜您触发隐藏密码，您将获得一个cdk：{self.cdkey}'
            self.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)
            self.cdkey_signal_2 = True
            self.cdkey_signal = False

        elif msg == self.cdkey and self.cdkey_signal_2:
            bonus = random.randint(10000, 20000)
            Csgo().add_money(from_wxid, bonus)
            msg = f'已为您添加{bonus}元'
            self.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)
            self.cdkey_signal = False
            self.cdkey_signal_2 = False

        elif '大乱斗' in msg:
            self.opgg(msg, wechat, room_wxid, from_wxid)

        elif '转账' in msg:
            self.transfer_accounts(msg, wechat, room_wxid, from_wxid, at_user_list)

        elif '开箱' in msg:
            self.open_case(msg, wechat, room_wxid, from_wxid)

        elif '查询比赛' in msg:
            self.search_game(msg, wechat, room_wxid, from_wxid)

        elif msg == 'print_user_money':
            msg = Csgo().print_user_money(wechat, room_wxid)
            self.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)

        elif msg == '模拟 龙狙':
            msg = Csgo().sim()
            self.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)

        elif msg == '热搜' or msg == '热搜安卓':
            hot_search_url = 'https://weibo.com/hot/search'
            pic_url = 'https://www.somode.com/uploadimg/ico/2022/0810/1660120968235761.jpg'
            res = TianApi().hotSearch(msg)
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif msg == '游戏资讯':
            res = TianApi().gameNews()
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif msg == '狗狗' or msg == '猫猫':
            if msg == '狗狗':
                filename = FreeApi().random_dog()
            else:
                filename = FreeApi().random_cat()
            self.send_imagemsg(wechat, room_wxid, from_wxid, filename, filename)

        elif msg == '百科题库':
            res = '此功能还在开发中'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
            # TianApi().BaikeTiku(wechat, room_wxid, from_wxid)

        elif msg == '来首网易云':
            songName, songPic, songArtists, mp3url, content = MuxiaoguoApi().wangyiyun()
            # wechat.send_text(to_wxid=room_wxid, content=msg)
            wechat.send_link_card(to_wxid=room_wxid, title=songName, desc=songArtists, url=mp3url,
                                  image_url=songPic)
            wechat.send_text(to_wxid=room_wxid, content=content)

        elif msg == '查询余额':
            res = Csgo().check_balance(from_wxid)
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif msg == '扫雷' and bf.into_mine_signal:
            bf.user = from_wxid
            bf.mine_signal = True
            bf.into_mine_signal = False
            mine.play(wechat, room_wxid, from_wxid)
            return

        elif msg == '扫雷' and bf.into_mine_signal == False:
            res = '已经有人在玩扫雷，请等待当前玩家结束。'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif from_wxid == bf.user and bf.mine_signal:
            if msg == '退出':
                res = '欢迎下次来玩。'
                self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
                bf.into_mine_signal = True
                bf.mine_signal = False
            else:
                mine.plays(wechat, room_wxid, msg, bf)

        # elif msg == '购买彩票':
        #     res = Ticket().get_num_and_save(from_wxid)
        #     self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
        #
        # elif msg == '开奖':
        #     res = Ticket().run_a_lottery(from_wxid)
        #     self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif msg == 'dust2hrj':
            res = 'hrj：默认防守\n主A。副狙（拿到狙后与主B交换位置）\na门抢下后留守a门。防守位可以在a门后、蓝箱后、大坑、大坑上、电梯位。在中门或b区交火后前压清点。回防建议：回防b区时直下中门与警家队友配合解放沙地后前往b1/b2与b门队友同步回防（交流tips：到了b2怕被狙位或大箱的人打可以喊b门外队友丢闪拿枪位）回防a区时保住a门进行简单反清a门。等待小道回防队友同步。若小道交火则拉出补枪。\na门没抢下或选择保小道（若身位不好双a时）与队友配合死守小道（若身位不好三a时）在忍者位或L位打发现或退守小道或警家（保命）等待回防。如有需要帮助小道队友丢闪返清。回防建议：回防b区时应带一眼a大保证后路安全。回防a区时与队友配合清完中路或等待队友闪光回防包点。'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
        elif msg == 'dust2sl':
            res = 'sl：默认防守\n副A。自由交火权\na门抢下后根据信息（如小道快上落位包点等待队友反清信号或闪光）快速回中门在根据对手喜好（如喜欢打a则落位警家方向、喜欢打b则落位沙地方向）进行防守打发现。若落位警家方向被夹b烟糊住则拿道具拖慢进攻等待a门队友清中路。若a门告破与b区队友清干净中路后进行回防。（交流tips：若落位b门外沙地对手进行夹b则可以在b门外箱后或狗洞外木架问队友要闪背闪并反清）若有需要向b点丢道具配合队友。\na门没抢下或选择保小道与队友配合死守小道。架点小套路：1与队友在小道台阶附近双架，队友架住b1自己架住小道。2队友直架小道在小道箱前进行补枪形成交叉火力。3队友台阶上架第二枪位死躲台阶下等待队友枪声信号。开枪就拉形成上下联动枪位。回防建议：回防a区应与队友清空中路小道后回防。回防b区与队友清空中路以及沙地后回防。'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
        elif msg == 'dust2xf':
            res = 'xf：默认防守\n主B。（副狙拿到狙后与副B交换位置）\n过中门时跳看一眼暗道取得信息。若有人在暗道里跑大概率快上小道告知队友。防rua道具丢完后若a门抢下死守b区。防守位可以在b包点、假门、狙位、大箱。根据队友站位和道具量选择直架或不直架（若没有道具选择听声音架第二枪位）与队友进行交流不得卖队友。a门没抢下或告破则与副b队友进行前压b区清理b2/b1与中路队友汇合进行回防。放a门保小道则死守b区根据队友指挥进行回防。回防建议：一定要与队友配合清完中路后回防、若得到信息如a门敌方来的很慢或战线拉的很长并没有a门外控制权则可从b2从匪家绕路从a门进行回防。注意️快速。若没有得到信息从b1回到中路与队友汇合选择小道警家或a大进行回防。'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
        elif msg == 'dust2cth':
            res = 'cth：默认防守\n副B。（副狙拿到狙后与主A交换位置）\n过中门时跳看一眼暗道取得信息。若有人在暗道里跑大概率快上小道告知队友。在主b将道具交与防rua后将自身伤害型道具与烟雾弹交与主b（若敌方选择rushB则不用）a门抢下在b门附近晃身看中路信息。敌人若夹b：a区队友没有及时回防时则退守车位死角与主b队友交流别漏给b门或狗洞。a区队友及时回防到沙地帮助队友丢闪清理中路。若中路占下则根据主b队友站位（如假门或大箱则在白车、如包点或狙位则在车位死角）选择点位。听b1/b2信息a门没抢下或告破与队友配合清理b2/b1完成后于b1进行回防。放a门保小道与a门抢下时不变。'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
        elif msg == 'dust2a':
            res = 'A区总结：清点要快要细。a门是整张地图重中之重。根据身位抢a门。a区防守者有一个在第一身位都应抢a门。'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
        elif msg == 'dust2b':
            res = 'B区总结：b区易守难攻，一旦包点被占回防很难。谨记死守。b区道具管理困难。交出烟雾弹和伤害性道具时机重要。梳理信息计算时间交道具。不要犹豫。'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
        elif msg == 'dust2':
            res = '地图总结：应是一张警图，在枪法不计的情况下应注意自身职责。好大喜功不可取。a门是整张地图的命脉。提取并梳理a门信息来选择自身决策。枪法不准不会喷，擅离职守或犯病拼枪将受到严厉谴责。希望各位不要犯病。'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif msg == '测试':
            res = Ticket().get_num_and_save(from_wxid)
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        # @菲菲说的话
        elif nickname in msg:
            temp_msg = self.delete_head(msg, nickname)
            res = api.qingyunke.get_reply(temp_msg)
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

    def open_case(self, msg, wechat, room_wxid, from_wxid):
        print(msg)
        max_count = 1000
        if msg == '开箱' or msg == '开箱帮助':
            msg = f'欢迎来到模拟开箱，请输入开箱数量（不得大于{max_count}）以及武器箱名！\n' \
                  '例如：开箱 100 命悬一线\n' \
                  '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' \
                  '目前支持的武器箱有：命悬一线、梦魇、古堡\n' \
                  '菲菲支持转账啦！\n输入"转账"并@你心爱的他 加上要转账的资金就可以啦！\n' \
                  '祝玩的开心！'
            self.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)
        else:
            try:
                temp = msg.split(' ')
                if len(temp) == 3:
                    print(temp)
                    case_count = int(temp[1])
                    case_name = temp[2]
                    print(case_name)
                    if 0 < case_count <= max_count:
                        # msg = '菲菲正在维护'
                        msg = Csgo().open_cases(from_wxid, case_count, case_name)
                    else:
                        msg = f'您输入的数量有误！当前仅支持1-{max_count}'
                else:
                    msg = '输入有误！'
                self.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)
                # wechat.send_pat(room_wxid, from_wxid)
            except Exception as e:
                self.send_textmsg(wechat, room_wxid, from_wxid, e, e)

    def search_game(self, msg, wechat, room_wxid, from_wxid):
        if msg == '查询比赛 帮助':
            res = '发送【查询比赛】：查询明天所有比赛。\n' \
                  '发送【查询比赛 昨天/今天/明天（或指定日期）】：查询指定日期所有比赛。\n' \
                  '发送【查询比赛全部lpl】：查询全部lpl比赛。\n' \
                  '发送【查询比赛lpl】：查询明天lpl比赛\n' \
                  '~~~~~~~~~~~~~\n' \
                  '暂未支持查询指定战队比赛。'
        elif msg == '查询比赛全部lpl':
            res = WanPlus().lpl_game()
        elif msg == '查询比赛lpl':
            res = WanPlus().send_tomorrow_lpl_game()
        else:
            res = WanPlus().filter_msg(msg)
        self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

    def transfer_accounts(self, msg, wechat, room_wxid, from_wxid, at_user_list):
        try:
            print(at_user_list)
            number = re.findall(r"\b\d+\b", msg)
            msgs = Csgo().transfer_accounts(from_wxid, at_user_list, number)
        except Exception as e:
            msgs = e
        self.send_textmsg(wechat, room_wxid, from_wxid, msgs, msgs)

    def opgg(self, msg, wechat, room_wxid, from_wxid):
        res = op_gg.get_opgg(wechat, msg, room_wxid, from_wxid)
        self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
