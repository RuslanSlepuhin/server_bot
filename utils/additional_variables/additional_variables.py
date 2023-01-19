# for add in vacancy search in db tables
additional_elements = {'admin_last_session', 'archive'}

valid_professions = ['designer', 'game', 'product', 'mobile', 'pm', 'sales_manager', 'analyst', 'frontend',
                     'marketing', 'devops', 'hr', 'backend', 'qa', 'junior']
valid_professions_extended = []
valid_professions_extended.extend(valid_professions)
valid_professions_extended.extend(['fullstack'])

not_lower_professions = ['pm', 'game', 'designer', 'hr', 'analyst', 'qa', 'ba' 'devops', 'product']

white_admin_list = [1763672666, 556128576, 758905227, 945718420, 5755261667, 5884559465]

id_owner = 1763672666

#admin database name
admin_database = 'admin_last_session'
archive_database = 'archive'
admin_table_fields = "id, chat_name, title, body, profession, vacancy, vacancy_url, company, english, relocation, " \
                             "job_type, city, salary, experience, contacts, time_of_public, created_at, agregator_link, " \
                             "session, sended_to_agregator, sub"

fields_admin_temporary = "id_admin_channel, id_admin_last_session_table, sended_to_agregator"
channel_id_for_shorts = -1001671844820

# message_for_send = f'<i>Функционал дайджеста находится в состоянии альфа-тестирования, приносим свои ' \
#                                    f'извинения, мы работаем над тем чтобы вы получали информацию максимально ' \
#                                    f'качественную и в сжатые сроки</i>\n\n'

dict_for_title_shorts = {
    '': 'Системных аналитиков',
}

pattern_path = "./excel/pattern.txt"
admin_check_file_path = './logs/check_file.txt'
sites_search_words = ['designer', 'ui', 'junior', 'product manager', 'project manager', 'python', 'php']

table_list_for_checking_message_in_db = ['admin_last_session', 'archive']

pre_message_for_shorts = '<i>Функционал дайджеста находится в состоянии альфа-тестирования, приносим свои ' \
                                   f'извинения, мы работаем над тем чтобы вы получали информацию максимально ' \
                                   f'качественную и в сжатые сроки</i>\n\n'

message_not_access = "Sorry, you have not the permissions"
path_last_pattern = "./patterns/last_changes/pattern_Alex2809 (6).py"
path_data_pattern = "./patterns/data_pattern/_data_pattern.py"