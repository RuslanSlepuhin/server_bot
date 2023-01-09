from patterns.profession_collection.analyst_pattern import analyst
from patterns.profession_collection.ba_pattern import ba
from patterns.profession_collection.backend_pattern import backend
from patterns.profession_collection.designer_pattern import designer
from patterns.profession_collection.detailed_designer_pattern import detailed_designer
from patterns.profession_collection.dev_pattern import dev
from patterns.profession_collection.devops_pattern import devops
from patterns.profession_collection.frontend_pattern import frontend
from patterns.profession_collection.game_pattern import game
from patterns.profession_collection.junior_pattern import junior
from patterns.profession_collection.hr_pattern import hr
from patterns.profession_collection.marketing_pattern import marketing
from patterns.profession_collection.mobile_pattern import mobile
from patterns.profession_collection.non_code_manager import non_code_manager
from patterns.profession_collection.pm_pattern import pm
from patterns.profession_collection.qa_pattern import qa
from patterns.profession_collection.fullstack_pattern import fullstack
from patterns.profession_collection.sales_manager_pattern import sales_manager
from patterns.data_pattern._data_pattern import pattern
from patterns.data_pattern._data_pattern import params
from patterns.data_pattern._data_pattern import vacancy_pattern
from patterns.data_pattern._data_pattern import search_companies, search_companies2

export_pattern = {
    'data': {
        'vacancy': pattern['vacancy'],
        'contacts': pattern['contacts'],
        },
    'professions': {
        'junior': junior,
        'analyst': analyst,
        'ba': ba,
        'backend': backend,
        'designer': designer,
        'devops': devops,
        'frontend': frontend,
        'game': game,
        'hr': hr,
        'marketing': marketing,
        'mobile': mobile,
        'pm': pm,
        'qa': qa,
        'sales_manager': sales_manager,
        'fullstack': fullstack,
    },
    'additional': {
        'dev': dev,
        'detailed_designer': detailed_designer,
        'non_code_manager': non_code_manager,
        'admins': pattern['admins'],
    },
    'others': {
        'remote': pattern['remote'],
        'relocate': pattern['relocate'],
        'english': {
            'ma': params['english_level'],
        },
        'vacancy': {
            'ma': '',
            'mex': '',
            'sub': vacancy_pattern,
        },
        'company': {
            'ma': search_companies,
            'mex': '',
            'sub': ''
        },
        'company2': {
            'ma': search_companies2,
            'mex': '',
            'sub': ''
        }
    }
}



# from qa
export_pattern['professions']['qa']['sub']['manual_qa']['mex'] = set(export_pattern['professions']['marketing']['mex']).union(set(export_pattern['professions']['qa']['sub']['manual_qa']['mex2']))
export_pattern['professions']['qa']['sub']['aqa']['mex'] = set(export_pattern['professions']['marketing']['mex']).union(set(export_pattern['professions']['qa']['sub']['aqa']['mex2']))

# from backend
export_pattern['additional']['dev']['mex']=set(export_pattern['professions']['backend']['ma']).union(set(export_pattern['professions']['backend']['sub']['python']['ma']))\
    .union(set(export_pattern['professions']['backend']['sub']['c']['ma'])).union(set(export_pattern['professions']['backend']['sub']['php']['ma']))\
    .union(set(export_pattern['professions']['fullstack']['ma'])).union(set(export_pattern['professions']['frontend']['ma'])).union(set(export_pattern['additional']['admins']['ma']))

# from designer
export_pattern['professions']['designer']['mex']=set(export_pattern['additional']['dev']['mex']).union(set(export_pattern['professions']['mobile']['ma'])).union(set(export_pattern['professions']['designer']['mex2']))\
    .union(set(export_pattern['professions']['qa']['mdef'])).union(set(export_pattern['professions']['sales_manager']['ma'])).union(set(export_pattern['professions']['marketing']['ma']))\
    .union(set(export_pattern['professions']['ba']['ma'])).union(set(export_pattern['professions']['pm']['ma'])).union(set(export_pattern['professions']['devops']['ma']))\
    .union(set(export_pattern['professions']['analyst']['ma'])).union(set(export_pattern['professions']['hr']['mdef']))

# from detailed_designer
detailed_designer['ma'] = set(export_pattern['professions']['designer']['sub']['ui_ux']['ma']).union(set(export_pattern['professions']['designer']['sub']['motion']['ma']))\
    .union(set(export_pattern['professions']['designer']['sub']['dd']['ma'])).union(set(export_pattern['professions']['designer']['sub']['ddd']['ma']))\
    .union(set(export_pattern['professions']['designer']['sub']['game_designer']['ma'])).union(set(export_pattern['professions']['designer']['sub']['illustrator']['ma']))\
    .union(set(export_pattern['professions']['designer']['sub']['graphic']['ma'])).union(set(export_pattern['professions']['designer']['sub']['uxre_searcher']['ma']))

export_pattern['professions']['designer']['mincl']=set(export_pattern['professions']['designer']['mex']).union(set(export_pattern['additional']['detailed_designer']['ma']))

# from analyst
export_pattern['professions']['analyst']['sub']['sys_analyst']['mex']=set(export_pattern['professions']['marketing']['mex']).union(set(export_pattern['professions']['analyst']['sub']['sys_analyst']['mex2'])),
export_pattern['professions']['analyst']['sub']['data_analyst']['mex']=set(export_pattern['professions']['marketing']['mex']).union(set(export_pattern['professions']['analyst']['sub']['data_analyst']['mex2'])),
export_pattern['professions']['analyst']['sub']['data_scientist']['mex']=set(export_pattern['professions']['marketing']['mex']).union(set(export_pattern['professions']['analyst']['sub']['data_scientist']['mex2'])),
export_pattern['professions']['analyst']['sub']['ba']['mex']=set(export_pattern['professions']['marketing']['mex']).union(set(export_pattern['professions']['analyst']['sub']['ba']['mex2'])),

# from mobile
export_pattern['professions']['mobile']['mex']=set(export_pattern['professions']['mobile']['mex2']).union(set(export_pattern['professions']['designer']['ma']))

# from frontend

# from game

# from hr

#from marketing

# from pm
# from sales_manager
# from dev

# for i in export_pattern:
#     if len(i)<2:
#         print(i, export_pattern[i])
#     else:
#         for i2 in i:
#             if len(i2)<2:
#                 print('---', i2, i[i2])
#             else:
#                 for i3 in i2:
#                     print('------', i3, i2[i3])
print(export_pattern.keys())


