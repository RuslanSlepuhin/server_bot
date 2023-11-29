import requests
from coffee_customer_bot_apps.variables import variables


class RequestsClass:

    def __init__(self):
        pass

    # -------------- Customer side --------------

    def customer_pressed_cancel_button(self):
        requests.get(variables.customer_pressed_cancel_endpoint)
        return {}

    def customer_feedback(self, rating=None, feedback=None):
        if rating or feedback:
            requests.get(variables.customer_feedback_endpoint)
        return {}


    def customer_add_username_to_database(self, user_id):
        requests.get(variables.customer_add_username_to_database_endpoint)
        return {}


    # -------------- Horeca side --------------

    # Barista rejects the order
    def horeca_status_reject_order(self):
        requests.get(variables.main_endpoint)
        return {}

    # Barista confirms the order
    def horeca_status_confirm_order(self):
        # взял в работу
        requests.get(variables.main_endpoint)
        return {}

    # Barista: the order processes
    def horeca_status_order_processes(self):
        requests.get(variables.main_endpoint)
        return {}

    # Barista: the order ready
    def horeca_status_order_is_ready(self):
        requests.get(variables.main_endpoint)
        return {}

    # Barista: the order ready
    def horeca_status_order_has_been_taken(self):
        requests.get(variables.main_endpoint)
        return {}

    def horeca_status_goods_broken(self):
        requests.get(variables.main_endpoint)
        return {}

    def horeca_disassembles_the_goods(self):
        requests.get(variables.main_endpoint)
        return {}

    def horeca_confirms_customer_cancel(self):
        requests.get(variables.main_endpoint)
        return {}

