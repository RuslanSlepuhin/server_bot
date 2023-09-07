import asyncio
import random
import re
import time
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from helper_functions.progress import ShowProgress


class ShortsPoster:

    def __init__(self, **kwargs):
        self.bot_aiogram = kwargs['bot'] if 'bot' in kwargs else None
        self.report = kwargs['report'] if 'report' in kwargs else None
        self.db = kwargs['db'] if 'db' in kwargs else None
        self.variable = kwargs['variable'] if 'variable' in kwargs else None
        self.helper = kwargs['helper'] if 'helper' in kwargs else None
        self.bot_class = kwargs['bot_class'] if 'bot_class' in kwargs else None
        self.telegraph_poster = kwargs['telegraph_poster'] if 'telegraph_poster' in kwargs else None
        self.config = kwargs['config'] if 'config' in kwargs else None
        self.client = kwargs['client'] if 'client' in kwargs else None

        self.history_messages = []
        self.prof_list = []
        self.get_vacancies_from_tg_admin = None

    async def compose_and_send_short(
            self,
            message,
            hard_push_profession,
            only_approved_by_admin=False,
            get_vacancies_from_tg_admin=False
    ):
        self.get_vacancies_from_tg_admin = get_vacancies_from_tg_admin
        self.only_approved_by_admin = only_approved_by_admin
        self.message = message
        self.prof_list = []
        self.db.delete_table(table_name=self.variable.shorts_database)

        # init additional classes when all variables were imported
        await self.init_classes()

        if hard_push_profession in ['*', 'all']:
            self.prof_list = self.variable.profession_list_for_pushing_by_schedule
        else:
            if type(hard_push_profession) is str:
                self.prof_list = [hard_push_profession,]
            elif type(hard_push_profession) in [list, tuple, set]:
                self.prof_list = hard_push_profession

        if self.prof_list:
            # this logic only for juniors when check all subs by all profession\
            # I need the other logic for the mono profession

            for profession in self.prof_list:
                self.profession = profession

                # get vacancies for build the shorts
                there_are_vacancies = await self.get_correct_vacancies()

                if there_are_vacancies:

                    self.short_session_name = await self.helper.get_short_session_name(prefix=profession)
                    self.db.write_short_session(self.short_session_name)
                    await self.bot_aiogram.send_message(message.chat.id, f"Shorts session: {self.short_session_name}")

                    # # update shorts session in current vacancies in table
                    # await self.update_shorts_session_vacancies()

                    # compose the dict by subs
                    await self.compose_message_for_send()

                    # public shorts to aggregator
                    loop = asyncio.get_event_loop()
                    task = loop.create_task(self.aggregator_vacancies_publisher())
                    await task
                    # await self.aggregator_vacancies_publisher()

                    await self.check_dictionaries()

                    # build several text short vacancy in common sub key
                    await self.rebuild_subs_to_str_dict()

                    if self.profession != self.variable.manual_posting_shorts:
                        # push to the telegraph
                        self.telegraph_links_dict = self.telegraph_poster.telegraph_post_digests(
                            self.sub_short_vacancies_dict['shorts_for_publishing'],
                            self.profession
                        )

                        # push the final pivot general short
                        await self.send_pivot_shorts()

                        # spread across prof tables
                        await self.spread_across_prof_tables()

                       # remove vacancies from admin_table
                        await self.clean_admin_table()

                        markup = InlineKeyboardMarkup()
                        button = InlineKeyboardButton('rollback short session', callback_data=f"rollback_short_session|{self.short_session_name}")
                        markup.add(button)
                        await self.bot_aiogram.send_message(self.message.chat.id, "Pushing has been done", reply_markup=markup)

                    else:
                        return False
                else:
                    print(f'there are not {self.profession} vacancies')
                    await self.send_message(html_text=f'There are not the {self.profession} vacancies')
        else:
            print('there is not professions')

        return True

    async def init_classes(self):
        self.show_progress = ShowProgress({'bot': self.bot_aiogram, 'chat_id': self.message.chat.id})

    async def get_correct_vacancies(self):
        # взять вакансии или из тг админки или из базы
        if self.get_vacancies_from_tg_admin:
            self.history_messages = await self.bot_class.get_tg_history_messages(self.message)
            await self.rebuild_from_tg_admin()
            return True if self.history_messages else False

        else:
            history_messages = {}
            query = f"WHERE profession LIKE '%{self.profession}%' AND approved='approves by admin'" if self.only_approved_by_admin else f"WHERE profession LIKE '%{self.profession}%'"
            self.history_messages = self.db.get_all_from_db(
                table_name=self.variable.admin_database,
                param=query,
                field=self.variable.admin_table_fields
            )
            if self.history_messages:
                for vacancy in self.history_messages:
                    vacancy_dict = await self.helper.to_dict_from_admin_response(vacancy, self.variable.admin_table_fields)
                    if vacancy_dict:
                        history_messages[vacancy_dict['id']] = vacancy_dict
                self.history_messages = history_messages.copy()
                return True
            else:
                return False

    async def rebuild_from_tg_admin(self):
        history_messages = {}
        for one_vacancy in self.history_messages:
            admin_vacancy_id = self.db.get_all_from_db(
                table_name=self.variable.admin_temporary,
                field=self.variable.admin_temporary_fields,
                param=f"WHERE id_admin_channel = '{str(one_vacancy['id'])}'",
                without_sort=True
            )
            if admin_vacancy_id and type(admin_vacancy_id) in [list, tuple, set]:
                vacancy_from_admin_table = self.db.get_all_from_db(
                    table_name=self.variable.admin_database,
                    field=self.variable.admin_table_fields,
                    param=f"WHERE id={str(admin_vacancy_id[0][2])}",

                )
                if vacancy_from_admin_table and type(vacancy_from_admin_table) in [list, tuple, set]:
                    vacancy_from_admin_table_dict = await self.helper.to_dict_from_admin_response(vacancy_from_admin_table[0], self.variable.admin_table_fields)
                    if vacancy_from_admin_table_dict:
                        vacancy_from_admin_table_dict['id_admin_channel'] = one_vacancy['id']
                        history_messages[vacancy_from_admin_table_dict['id']] = vacancy_from_admin_table_dict
        self.history_messages = history_messages

    async def update_shorts_session_vacancies(self):
        for id in self.history_messages.keys():
            self.db.update_table(
                table_name=self.variable.admin_database,
                field='short_session_numbers',
                value=self.short_session_name,
                param=f"WHERE id={id}",
                notification=False
            )

    async def compose_message_for_send(self):
        self.sub_short_vacancies_dict = {}
        subs = []
        if self.history_messages:
            self.last_id_message_agregator = await self.bot_class.get_last_admin_channel_id(
                message=self.message,
                channel=self.config['My_channels']['agregator_channel']
            )
            for vacancy in self.history_messages:
                self.vacancy = self.history_messages[vacancy]
                # взять каждый саб, сделать его ключом, проверить есть ли этот ключ в итоговом словаре и вписать туда с ключом
                subs = self.vacancy['sub'].split(self.variable.sub_separator)

                found_subs = False

# -------------------------------------------------------------------------------------------
                self.subs_dict = {}
                removed_subs = []
                for sub in subs:
                    sub_split = sub.split(": ")

                    if self.profession == 'junior':
                        if sub_split[0] != 'junior':
                            if sub_split[0] not in self.subs_dict:
                                self.subs_dict[sub_split[0]] = []
                            self.subs_dict[sub_split[0]].append(sub_split[1])
                        else:
                            removed_subs.append(sub)

                    else:
                        if sub_split[0] == self.profession:
                            if sub_split[0] not in self.subs_dict:
                                self.subs_dict[sub_split[0]] = []
                            self.subs_dict[sub_split[0]].append(sub_split[1])
                            removed_subs.append(sub)

                self.vacancy['sub'] = ", ".join(set(subs) - set(removed_subs))
                await self.build_aggregator_vacancy()

# -------------------------------------------------------------------------------------------

                if self.vacancy['approved'] != 'approves by admin':
                    self.db.update_table(table_name=self.variable.admin_database, field='approved',
                                         value='approves by admin', param=f"WHERE id={self.vacancy['id']}")
                    self.history_messages[self.vacancy['id']]['approved'] = 'approves by admin'
        else:
            print('there are not vacancies')

        # professions = ", ".join(list(filter(self.profession, self.vacancy['profession'].split(", "))))


    async def build_aggregator_vacancy(self):
        subs_list = []
        for profession in self.subs_dict:
            result = list(filter(None, self.subs_dict[profession]))
            if result:
                subs_list.extend(result)
            else:
                subs_list.append(profession)
        if not subs_list:
            subs_list.append(self.profession)



        vacancy_text = ''
        if 'sorted_by_subs' not in self.sub_short_vacancies_dict:
            self.sub_short_vacancies_dict['sorted_by_subs'] = {}
        for key in self.variable.fields_for_agregator_vacancy:
            if key in self.vacancy:
                if key not in ['title', 'body']:
                    vacancy_text += f"{key.capitalize().replace('_', ' ')}: {self.vacancy[key]}\n" if key != self.variable.double_n_before_field else f"{key.capitalize().replace('_', ' ')}: {self.vacancy[key]}\n\n"
                else:
                    vacancy_text += f"{self.vacancy[key]}\n"
        if vacancy_text:
            for sub in subs_list:
                self.vacancy_text = vacancy_text
                await self.check_len_and_add_extra()
                if sub not in self.sub_short_vacancies_dict['sorted_by_subs']:
                    self.sub_short_vacancies_dict['sorted_by_subs'][sub] = []
                self.sub_short_vacancies_dict['sorted_by_subs'][sub].append(
                    {
                        'id': self.vacancy['id'],
                        'id_admin_channel': self.vacancy['id_admin_channel'] if 'id_admin_channel' in self.vacancy else None,
                        'vacancy_text': self.vacancy_text,
                    }
                )
        else:
            self.vacancy_text = ''
            print('There is not vacancy_text 103')


    async def check_len_and_add_extra(self):
        extra_text_html = f"\n---- \n" \
                          f"В этом канале выводятся все собранные вакансии (агрегатор), для вашего удобства мы рекомендуем " \
                          f"подписаться на наиболее подходящие для вас каналы (ссылки подобраны в каждом из сообщений):\n" \
                          f"<a href=\"{self.config['Links']['junior']}\">Канал с вакансиями для Junior IT специалистов</a>"
        if self.profession != 'junior':
            extra_text_html += f"\n<a href=\"{self.config['Links'][self.profession]}\">Канал с вакансиями для {self.profession.title()} специалистов</a>"

        if len(self.vacancy_text) <= 4096:
            if len(self.vacancy_text) + len(extra_text_html) <= 4096:
                self.vacancy_text += extra_text_html
        else:
            self.vacancy_text = self.vacancy_text[:4093] + '...'

    async def aggregator_vacancies_publisher(self):
        with open("./aggregator_vacancies_publisher.txt", 'w') as file:
            file.write("\n")

        self.current_aggregator_id = await self.bot_class.get_last_admin_channel_id(
                    message=self.message,
                    channel=self.config['My_channels']['agregator_channel']
                )

        await self.show_progress.reset_percent()
        length = 0
        for sub in self.sub_short_vacancies_dict['sorted_by_subs']:
            length += len(self.sub_short_vacancies_dict['sorted_by_subs'][sub])
        n=0
        await self.show_progress.start()

        for sub in self.sub_short_vacancies_dict['sorted_by_subs']:
            for vacancy in self.sub_short_vacancies_dict['sorted_by_subs'][sub]:
                try:
                    if not self.history_messages[vacancy['id']]['sended_to_agregator']:

                        # loop = asyncio.get_event_loop()
                        # task = loop.create_task(self.send_message(chat_id=int(self.config['My_channels']['agregator_channel']), html_text=vacancy['vacancy_text']))
                        # await task
                        msg = await self.send_message(chat_id=int(self.config['My_channels']['agregator_channel']), html_text=vacancy['vacancy_text'])
                        if msg:
                            self.current_aggregator_id += 1

                            self.db.update_table(
                                table_name=self.variable.admin_database,
                                field='sended_to_agregator',
                                value=self.current_aggregator_id,
                                param=f"WHERE id={vacancy['id']}",
                                output_text=f'{n}:vacancy has been updated [field: sended_to_agregator]'
                            )
                            self.history_messages[vacancy['id']]['sended_to_agregator'] = self.current_aggregator_id
                            index_vacancy = self.sub_short_vacancies_dict['sorted_by_subs'][sub].index(vacancy)
                            self.sub_short_vacancies_dict['sorted_by_subs'][sub][index_vacancy]['id_admin_channel'] = self.current_aggregator_id

                            vacancy_name = vacancy['vacancy_text'].split("\n")[0].split(": ")[1]
                            with open("./aggregator_vacancies_publisher.txt", 'a') as file:
                                file.write(f"{vacancy['id']}: {self.current_aggregator_id}\n{vacancy_name} (vacancy_name)\n{self.history_messages[vacancy['id']]['vacancy']} (vacancy_history)\n")

                            await asyncio.sleep(random.randrange(2, 4))
                        else:
                            print("!!!ALARM !!!")
                            await self.send_message(chat_id=self.message.chat.id, html_text="!!!ALARM !!! Vacancies numbering failure, please get a help from developer")
                            pass

                    else:
                        print("vacancy has been not changed :)")
                        vacancy_name = vacancy['vacancy_text'].split("\n")[0].split(": ")[1]
                        with open("./aggregator_vacancies_publisher.txt", 'a') as file:
                            file.write(f"->{vacancy['id']}: {self.history_messages[vacancy['id']]['sended_to_agregator']}\n{vacancy_name} (vacancy_name)\n{self.history_messages[vacancy['id']]['vacancy']} (vacancy_history)\n")

                        index_vacancy = self.sub_short_vacancies_dict['sorted_by_subs'][sub].index(vacancy)
                        self.sub_short_vacancies_dict['sorted_by_subs'][sub][index_vacancy]['id_admin_channel'] = self.history_messages[vacancy['id']]['sended_to_agregator']

                    try:
                        self.db.update_table(
                            table_name=self.variable.admin_database,
                            field='short_session_numbers',
                            value=self.short_session_name,
                            param=f"WHERE id={vacancy['id']}",
                            output_text=f'{n}:vacancy has been updated [field: short_session_numbers]'
                        )
                        self.history_messages[vacancy['id']]['short_session_numbers'] = self.short_session_name


                    except Exception as e:
                        print('error 22', e)
                        pass

                except Exception as ex:
                    print(ex, "error 1")
                    pass
                n += 1
                await self.show_progress.show_the_progress(message=None, current_number=n, end_number=length)
        pass

    async def rebuild_subs_to_str_dict(self):
        self.sub_short_vacancies_dict['shorts_for_publishing'] = {}
        for sub in self.sub_short_vacancies_dict['sorted_by_subs']:
            # if sub in self.profession:
                for vacancy_id in self.sub_short_vacancies_dict['sorted_by_subs'][sub]:

                    vacancy_from_agregator = vacancy_id['vacancy_text'].split('\n')[0].split(': ')[1]
                    print(f"{vacancy_from_agregator} vacancy from sub_shorts")
                    print(f"{self.history_messages[vacancy_id['id']]['vacancy']} vacancy from history")
                    pass


                    short_str = await self.get_short_str(vacancy_id['id'])

                    pass

                    if sub not in self.sub_short_vacancies_dict['shorts_for_publishing']:
                        self.sub_short_vacancies_dict['shorts_for_publishing'][sub] = ''
                    self.sub_short_vacancies_dict['shorts_for_publishing'][sub] += f"{short_str}\n\n"
                    pass

                self.sub_short_vacancies_dict['shorts_for_publishing'][sub] = f"Дайджест вакансий для #{sub.title()} за {datetime.now().strftime('%d-%m-%Y')}\n\n" + self.sub_short_vacancies_dict['shorts_for_publishing'][sub]
                if self.profession in self.variable.manual_posting_shorts:
                    try:
                        # await self.bot_aiogram.send_message(self.message.chat.id, self.sub_short_vacancies_dict['shorts_for_publishing'][sub], parse_mode='html', disable_web_page_preview=True)

                        await self.send_message(html_text=self.sub_short_vacancies_dict['shorts_for_publishing'][sub], chat_id=self.message.chat.id)
                        await asyncio.sleep(random.randrange(1, 3))

                    except Exception as ex:
                        print(ex, 'error 2')
                        pass
            # else:
            #     pass
        pass

    async def get_short_str(self, vacancy_id):
        short_str = ''
        vacancy = self.history_messages[vacancy_id]
        short_str += f"<a href='{self.config['My_channels']['agregator_link']}/{vacancy['sended_to_agregator']}'>{vacancy['vacancy'].title()}</a> " \
            if 'vacancy' in vacancy and vacancy['vacancy'] \
            else f"<a href='{self.config['Channel_links']['agregator_channel']}/{vacancy['sended_to_agregator']}'>987 </a>"
        print(short_str)
        short_str += f"в {vacancy['company'].title()} " if 'company' in vacancy and vacancy['company'] else ''
        short_str += '('
        short_str += f"eng: {vacancy['english'].title()}, " if 'english' in vacancy and vacancy['english'] else ''
        short_str += f"{vacancy['job_type']}, " if 'job_type' in vacancy and vacancy['job_type'] else ''
        short_str += f"{vacancy['salary_from']} " if 'salary_from' in vacancy and vacancy['salary_from'] else ''
        short_str += f"- {vacancy['salary_to']} " if 'salary_to' in vacancy and vacancy['salary_to'] else ''
        short_str += f"{vacancy['salary_currency']} " if 'salary_currency' in vacancy and vacancy['salary_currency'] else ''
        if short_str[-1:] != '(':
            if short_str[-2:] == ', ':
                short_str = short_str[:-2] + ')'
            else:
                short_str = short_str.strip() + ')'
        else:
            short_str = short_str[:-1]
        return short_str

    async def send_pivot_shorts(self):
        numbers_vacancies_dict = self.telegraph_links_dict['numbers_vacancies_dict']
        telegraph_links_dict = self.telegraph_links_dict['telegraph_links_dict']

        digest_dict = {}
        from utils.custom_subs.custom_subs import custom_subs, name_professions

        for key in telegraph_links_dict:
            has_been_written = False
            for profession in custom_subs:
                if key in custom_subs[profession]:
                    if profession not in digest_dict:
                        digest_dict[profession] = {}
                    digest_dict[profession][key] = telegraph_links_dict[key]
                    has_been_written = True
                    break

                elif key == profession:
                    if profession not in digest_dict:
                        digest_dict[profession] = {}
                    digest_dict[profession][profession] = telegraph_links_dict[key]
                    has_been_written = True
                    break

            if not has_been_written:
                if key not in digest_dict:
                    digest_dict[key] = {}
                digest_dict[key][key] = telegraph_links_dict[key]

        for key in digest_dict:
            if len(digest_dict[key]) == 1 and key in digest_dict[key]:
                digest_dict[key] = digest_dict[key][key]

        telegram_digest = f"{sum(numbers_vacancies_dict.values())} вакансий и стажировок на канале для <a href='{self.config['Channel_links'][f'{self.profession}_channel']}'><b>{name_professions[self.profession]} специалистов</b></a> за {datetime.now().strftime('%d.%m.%Y')}:\n\n"

        for prof in digest_dict:

            if type(digest_dict[prof]) is str:
                """
                if it's the profession without subs
                """
                prof_clean = prof.split("(")[0].strip() if "(" in prof else prof
                profession_name = name_professions[prof_clean] if prof_clean in name_professions else prof.title()
                profession_name = profession_name + f" ({prof.split('(')[1]}" if "(" in prof else profession_name
                telegram_digest += f"<a href='{telegraph_links_dict[prof]}'><b>{profession_name}:</b> {numbers_vacancies_dict[prof]} предложений</a>\n\n"

            elif type(digest_dict[prof]) is dict:
                """
                If it's profession with subs
                """
                amount = 0
                for key in digest_dict[prof].keys():
                    amount += numbers_vacancies_dict[key]
                profession_name = name_professions[prof] if prof in name_professions else prof.title()
                telegram_digest += f"{profession_name} ({amount} предложений):\n\n"

                for sub in digest_dict[prof]:
                    profession_name = name_professions[sub] if sub in name_professions else sub.title()
                    telegram_digest += f"    - <a href='{telegraph_links_dict[sub]}'><b>{profession_name.capitalize()}:</b> {numbers_vacancies_dict[sub]} предложений</a>\n\n"
                telegram_digest += "\n"

        if self.profession in self.variable.manual_posting_shorts:
            await self.bot_aiogram.send_message(self.message.chat.id, telegram_digest, disable_web_page_preview=True, parse_mode='html')
        else:
            from utils.pictures.pictures_urls.pictures_urls import pictures_urls
            picture = pictures_urls[self.profession] if self.profession in pictures_urls else pictures_urls['common']

            channel_list = [int(self.config['My_channels'][f"{self.profession}_channel"]), self.variable.channel_id_for_shorts, self.message.chat.id] if self.profession not in self.variable.manual_posting_shorts else [self.variable.channel_id_for_shorts, self.message.chat.id]

            for id_channel in channel_list:
                try:
                    await self.bot_aiogram.send_photo(id_channel, picture, caption=telegram_digest, parse_mode='html')
                    break
                except Exception as ex:
                    print(f'bot can\'t send shorts to channel {id_channel}: {str(ex)}', 'error 3')

        self.sub = None
        # self.profession = None
        return True

    async def clean_admin_table(self):

        if self.get_vacancies_from_tg_admin:

            await self.bot_aiogram.send_message(self.message.chat.id, "Clean admin channel")
            await self.show_progress.reset_percent()
            await self.show_progress.start()
            n = 0
            length = len(self.history_messages)

            for key in self.history_messages:
                if 'id_admin_channel' in self.history_messages[key]:
                    await self.client.delete_messages(int(self.config['My_channels']['admin_channel']), self.history_messages[key]['id_admin_channel'])
                    await asyncio.sleep(random.randrange(0, 2))

                n += 1
                await self.show_progress.show_the_progress(message=None, current_number=n, end_number=length)

        await self.bot_aiogram.send_message(self.message.chat.id, "Update profession or transfer to the archive")
        await self.show_progress.reset_percent()
        await self.show_progress.start()
        n = 0
        length = len(self.history_messages)

        for key in self.history_messages:
            profession_list = self.history_messages[key]['profession'].split(', ')
            if len(profession_list) > 1:
                profession_list.remove(self.profession)
                update_profession = ", ".join(profession_list)
                self.db.update_table(table_name=self.variable.admin_database, field='profession',
                                     value=update_profession, param=f"WHERE id={key}")
            else:
                transfer = self.db.transfer_vacancy(table_from=self.variable.admin_database, table_to=self.variable.archive_database, id=key)
                if transfer:
                    self.db.delete_data(table_name=self.variable.admin_database, param=f"WHERE id={key}")

            n += 1
            await self.show_progress.show_the_progress(message=None, current_number=n, end_number=length)

    async def send_message(self, html_text, chat_id=None):
        msg = None
        if not chat_id:
            chat_id = self.message.chat.id

        html_text_list = self.helper.split_text_limit(html_text)
        counter = 0
        # while True:
        #     try:
        while counter <= len(html_text_list) - 1:
            try:
                msg = await self.bot_aiogram.send_message(chat_id, html_text_list[counter], parse_mode='html', disable_web_page_preview=True)
                counter += 1

            except Exception as ex1:

                if 'flood control' in ex1.args[0].lower():
                    print('error 34: flood control: ')
                    await self.flood_control(ex1)

                elif 'unsupported start tag "100%"' in ex1.args[0]:
                    print('error 35: unsupported start tag "100%": ')
                    html_text_list[counter] = re.sub(r"[^bap\"](>)", ' больше ', html_text_list[counter])
                    html_text_list[counter] = re.sub(r"(<)[^bap\/]", " меньше ", html_text_list[counter])

                elif 'unsupported start tag' in ex1.args[0]:
                    print('error 36: ', ex1)
                    match = re.findall(r"<[a-zA-Zа-яА-Я\s,.]*>", html_text_list[counter])
                    if match:
                        for one_match in match:
                            html_text_list[counter] = re.sub(rf"{one_match}", one_match[1:-1], html_text_list[counter])
                    else:
                        return False

                else:
                    print('error 37: ', ex1)
                    print(html_text_list[counter])
                    pass
                    return False

        # msg = await self.bot_aiogram.send_message(chat_id, html_text, parse_mode='html', disable_web_page_preview=True)
        return msg
            # except Exception as ex2:
            #     if 'flood control' in ex2.args[0].lower():
            #         print('error 36: flood control: ')
            #         await self.flood_control(ex2)
            #     if 'unsupported start tag "100%"' in ex2.args[0]:
            #         print('error 37: flood unsupported start tag "100%": ')
            #         html_text = re.sub(r"[^bap\"](>)", ' больше ', html_text)
            #         html_text = re.sub(r"(<)[^bap\/]", " меньше ", html_text)

        # while True:
        #     msg = None
        #     try:
        #         for text in html_text_list:
        #             try:
        #                 msg = await self.bot_aiogram.send_message(chat_id, text, parse_mode='html', disable_web_page_preview=True)
        #                 if len(html_text_list)>1:
        #                     await asyncio.sleep(random.randrange(0, 2))
        #
        #             except Exception as ex:
        #                 if 'flood control' in ex.args[0].lower():
        #                     await self.flood_control(ex)
        #                     msg = await self.bot_aiogram.send_message(chat_id, text, parse_mode='html', disable_web_page_preview=True)
        #                     await asyncio.sleep(random.randrange(1, 3))
        #         return msg
        #     except Exception as ex:
        #         if 'flood control' in ex.args[0].lower():
        #             await self.flood_control(ex)
        #         if 'unsupported start tag "100%"' in ex.args[0]:
        #             html_text = re.sub(r"[^bap\"](>)", ' больше ', html_text)
        #             html_text = re.sub(r"(<)[^bap\/]", " меньше ", html_text)

    async def flood_control(self, ex):
        match = re.findall(r"[0-9]{1,4} seconds", ex.args[0])
        if match:
            seconds = match[0].split(' ')[0]
            print(f"\n--------------\nFlood control [{seconds} seconds]\n--------------\n")
            time.sleep(int(seconds) + 5)

    async def spread_across_prof_tables(self):
        for key in self.history_messages:
            time = datetime.now()
            vacancy = self.history_messages[key]

            vacancy['created_at'] = time
            vacancy['short_session_numbers'] = self.short_session_name

            self.db.update_table(table_name=self.variable.admin_database, field='created_at', value=time, param=f"WHERE id={key}")

            vacancy_from_admin_table = self.db.get_all_from_db(
                table_name=self.variable.admin_database,
                param=f"WHERE id={key}",
                field=self.variable.admin_table_fields,
            )
            vacancy_from_admin_table_dict = await self.helper.to_dict_from_admin_response(vacancy_from_admin_table[0], self.variable.admin_table_fields)

            for table_to in [self.variable.vacancies_database, self.profession]:
                exists = self.db.check_vacancy_exists_in_db(tables_list=[table_to, ], title=vacancy['title'], body=vacancy['body'])
                if not exists['has_been_found']:

                    # response = self.db.push_to_db_common(table_name=table_to, fields_values_dict=vacancy)
                    print('3689545')
                    # transfer = self.db.transfer_vacancy(
                    #     table_from=self.variable.admin_database,
                    #     table_to=table_to,
                    #     id=vacancy['id'])
                    # transfer=True
                    profession_list = {}
                    profession_list['profession'] = [self.profession]
                    # results_dict = {'title': 'title', 'body': 'body', 'profession': 'junior', 'sub': ''}

                    self.db.push_to_bd(results_dict=vacancy_from_admin_table_dict, profession_list=profession_list)

                    # if transfer:
                    #     print(f'Vacancy has been added to {table_to}')
                else:
                    print(f"vacancy has been found in {table_to}")
                    self.db.update_table(
                        table_name=table_to,
                        field='short_session_numbers',
                        value=self.short_session_name,
                        param=f"WHERE id={exists['id']}"
                    )

    async def check_dictionaries(self):
        for sub in self.sub_short_vacancies_dict['sorted_by_subs']:
            for item in self.sub_short_vacancies_dict['sorted_by_subs'][sub]:
                id = item['id']
                aggregator_id = item['id_admin_channel']
                if aggregator_id != self.history_messages[id]['sended_to_agregator']:
                    print("NOT MATCHING ID: ", id)
                    pass
                else:
                    print("MATCH")



