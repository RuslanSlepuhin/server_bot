from typing import Tuple


class GetFilteredParams:
    @staticmethod
    def get_filtered_params(parsed_params: dict) -> Tuple[str, str, str, str, str]:

        direction_ = parsed_params.get("selected_direction", "")

        specialization_ = parsed_params.get("selected_specializations", "")[2:-2]

        level_ = parsed_params.get("selected_level", "")[2:-2]

        # selected_location_ = parsed_params.get("selected_location", "")[2:-2]
        work_format_ = parsed_params.get("selected_work_format", "")[2:-2]

        keyword = parsed_params.get("keyword", "")

        #  interval = parsed_params.get("interval", "")

        level = level_.replace("'", "").strip()
        direction = direction_.replace("'", "").strip()
        specialization = specialization_.replace("'", "").strip()
        # selected_location = selected_location_.replace("'", "").strip()
        work_format = work_format_.replace("'", "").strip()

        return level, direction, work_format, specialization, keyword
