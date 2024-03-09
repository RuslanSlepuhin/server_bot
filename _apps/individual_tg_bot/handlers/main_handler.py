import _apps.individual_tg_bot.text as text
from _apps.individual_tg_bot.handlers.callback.direction_callback import (
    direction_analyst_callback,
    direction_backend_callback,
    direction_design_callback,
    direction_dev_ops_callback,
    direction_frontend_callback,
    direction_fullstack_callback,
    direction_game_dev_callback,
    direction_hr_callback,
    direction_marketing_callback,
    direction_mobile_callback,
    direction_product_project_manager_callback,
    direction_qa_callback,
    direction_sales_callback,
    direction_support_callback,
)
from _apps.individual_tg_bot.handlers.callback.key_word_callback import key_word_handler
from _apps.individual_tg_bot.handlers.callback.level_callback import (
    level_callback_handler,
)
from _apps.individual_tg_bot.handlers.callback.location_callback import (
    location_callback_handler,
)
from _apps.individual_tg_bot.handlers.callback.menu_callback import (
    get_notification_callback,
    get_restart_callback,
    get_vacancy_filter,
)
from _apps.individual_tg_bot.handlers.callback.new_request_callback import (
    comeback_request_callback,
    reset_request_callback,
)
from _apps.individual_tg_bot.handlers.callback.notification_callback import (
    cancel_change_user_notification,
    cancel_user_notification,
    confirm_change_user_notification,
    get_on_getting_notification,
    get_per_day_notification,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.analyst_specialization import (
    analyst_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.backend_specialization import (
    backend_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.design_specialization import (
    design_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.dev_ops_specialization import (
    dev_ops_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.frontend_specialization import (
    frontend_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.fullstack_specialization import (
    fullstack_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.game_dev_specialization import (
    game_dev_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.hr_specialization import (
    hr_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.marketing_specialization import (
    marketing_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.mobile_specialization import (
    mobile_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.product_project_manager_specialization import (
    product_project_manager_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.qa_specialization import (
    qa_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.sales_specialization import (
    sales_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.specialization_callback.support_specialization import (
    support_specialization_callback,
)
from _apps.individual_tg_bot.handlers.callback.work_format_callback import (
    work_format_callback_handler,
)
from _apps.individual_tg_bot.handlers.command_router import (
    bot_info,
    cancel_handler,
    get_menu,
    start_handler,
)
from _apps.individual_tg_bot.keyboards.inline.level_button import level_button_dict
from _apps.individual_tg_bot.keyboards.inline.location_button import (
    location_button_dict,
)
from _apps.individual_tg_bot.keyboards.inline.specializations.buttons import (
    buttons_analyst,
    buttons_backend,
    buttons_design,
    buttons_dev_ops,
    buttons_frontend,
    buttons_fullstack,
    buttons_game_dev,
    buttons_hr,
    buttons_marketing,
    buttons_mobile,
    buttons_product_project_manager,
    buttons_qa,
    buttons_sales,
    buttons_support,
)
from _apps.individual_tg_bot.keyboards.inline.work_format import work_format_dict
from aiogram import Dispatcher


class Handlers:
    def __init__(self, dp: Dispatcher) -> None:
        self.dp = dp
        self.register_message_handlers()
        self.register_direction_handlers()
        self.register_specializations_handlers()
        self.register_level_handler()
        self.register_location_handler()
        self.register_work_format_handler()
        self.register_keyword_handler()
        self.register_notification_handlers()
        self.reset_request_handler()
        self.register_menu_callback()

    def register_message_handlers(self):
        """Регистрация message handlers"""
        self.dp.register_message_handler(start_handler, commands=["start"])
        self.dp.register_message_handler(cancel_handler, commands=["cancel"])
        self.dp.register_message_handler(get_menu, commands=["menu"])
        self.dp.register_message_handler(bot_info, commands=["info"])

    def register_notification_handlers(self):
        """Регистрация callback notification handlers"""

        self.dp.register_callback_query_handler(
            confirm_change_user_notification, text=text.confirm_change_notification
        )
        self.dp.register_callback_query_handler(
            cancel_user_notification, text=text.cancel_notification
        )
        self.dp.register_callback_query_handler(
            get_per_day_notification, text=text.per_day_notification
        )
        self.dp.register_callback_query_handler(
            get_on_getting_notification, text=text.on_getting_notification
        )
        self.dp.register_callback_query_handler(
            cancel_change_user_notification, text=text.cancel_change_notification
        )

    def register_menu_callback(self):
        """Регистрация callback menu handlers"""
        self.dp.register_callback_query_handler(
            get_vacancy_filter, text=text.vacancy_filter
        )
        self.dp.register_callback_query_handler(
            get_notification_callback, text=text.notification
        )
        self.dp.register_callback_query_handler(get_restart_callback, text=text.restart)

    def register_direction_handlers(self):
        """Регистрация callback  direction handlers"""
        self.dp.register_callback_query_handler(
            direction_design_callback, text=text.design
        )
        self.dp.register_callback_query_handler(
            direction_backend_callback, text=text.backend
        )
        self.dp.register_callback_query_handler(
            direction_analyst_callback, text=text.analyst
        )
        self.dp.register_callback_query_handler(
            direction_mobile_callback, text=text.mobile
        )
        self.dp.register_callback_query_handler(
            direction_marketing_callback, text=text.marketing
        )
        self.dp.register_callback_query_handler(
            direction_product_project_manager_callback,
            text=text.product_project_manager,
        )
        self.dp.register_callback_query_handler(
            direction_sales_callback, text=text.sales
        )
        self.dp.register_callback_query_handler(
            direction_dev_ops_callback, text=text.dev_ops
        )
        self.dp.register_callback_query_handler(
            direction_frontend_callback, text=text.frontend
        )
        self.dp.register_callback_query_handler(
            direction_support_callback, text=text.support
        )
        self.dp.register_callback_query_handler(
            direction_fullstack_callback, text=text.fullstack
        )
        self.dp.register_callback_query_handler(direction_hr_callback, text=text.hr)
        self.dp.register_callback_query_handler(
            direction_game_dev_callback, text=text.game_dev
        )
        self.dp.register_callback_query_handler(direction_qa_callback, text=text.qa)

    def register_specializations_handlers(self):
        """Регистрация callback  specializations handlers"""
        self.dp.register_callback_query_handler(
            design_specialization_callback, text=buttons_design
        )
        self.dp.register_callback_query_handler(
            analyst_specialization_callback, text=buttons_analyst
        )
        self.dp.register_callback_query_handler(
            backend_specialization_callback, text=buttons_backend
        )
        self.dp.register_callback_query_handler(
            dev_ops_specialization_callback, text=buttons_dev_ops
        )
        self.dp.register_callback_query_handler(
            frontend_specialization_callback, text=buttons_frontend
        )
        self.dp.register_callback_query_handler(
            fullstack_specialization_callback, text=buttons_fullstack
        )
        self.dp.register_callback_query_handler(
            game_dev_specialization_callback, text=buttons_game_dev
        )
        self.dp.register_callback_query_handler(
            hr_specialization_callback, text=buttons_hr
        )
        self.dp.register_callback_query_handler(
            marketing_specialization_callback, text=buttons_marketing
        )
        self.dp.register_callback_query_handler(
            mobile_specialization_callback, text=buttons_mobile
        )
        self.dp.register_callback_query_handler(
            product_project_manager_specialization_callback,
            text=buttons_product_project_manager,
        )
        self.dp.register_callback_query_handler(
            qa_specialization_callback, text=buttons_qa
        )
        self.dp.register_callback_query_handler(
            sales_specialization_callback, text=buttons_sales
        )
        self.dp.register_callback_query_handler(
            support_specialization_callback, text=buttons_support
        )

    def register_level_handler(self):
        """Регистрация callback  level handlers"""
        self.dp.register_callback_query_handler(
            level_callback_handler, text=level_button_dict
        )

    def register_location_handler(self):
        """Регистрация callback  location handlers"""
        self.dp.register_callback_query_handler(
            location_callback_handler, text=location_button_dict
        )

    def register_work_format_handler(self):
        """Регистрация callback  work_format handlers"""
        self.dp.register_callback_query_handler(
            work_format_callback_handler, text=work_format_dict
        )

    def register_keyword_handler(self):
        """Регистрация callback  keyword_ handlers"""
        self.dp.register_message_handler(key_word_handler, state="*")

    def reset_request_handler(self):
        """Регистрация callback  reset_request handlers"""
        self.dp.register_callback_query_handler(
            comeback_request_callback, text=text.come_back
        )
        self.dp.register_callback_query_handler(
            reset_request_callback, text=text.reset_request
        )
