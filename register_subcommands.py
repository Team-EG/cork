import asyncio
from discord_slash.utils import manage_commands
from modules.client import CorkClient

loop = asyncio.get_event_loop()

loop.run_until_complete(manage_commands.add_slash_command(
    791679306123968553,
    CorkClient.get_settings("token"),
    None,
    "set",
    "알림 세부 설정 관련 명령어입니다.",
    [
        {
            "name": "보기",
            "description": "설정이 필요한 알림들을 보여줍니다.",
            "type": 1
        },
        {
            "name": "반복",
            "description": "반복 타임 알림 설정 명령어입니다.",
            "type": 1,
            "options": [
                manage_commands.create_option(
                    "이름",
                    "설정할 반복 타입 알림 이름",
                    3,
                    True
                ),
                manage_commands.create_option(
                    "분",
                    "울릴 시간의 분",
                    4,
                    True
                ),
                manage_commands.create_option(
                    "시간",
                    "울릴 시간의 시간 (24시간 기준)",
                    4,
                    True
                ),
                manage_commands.create_option(
                    "반복주기",
                    "어떻게 알림이 반복되는지",
                    3,
                    True,
                    [manage_commands.create_choice("daily", "날마다"),
                     manage_commands.create_choice("weekly", "요일마다"),
                     manage_commands.create_choice("monthly", "매월"),
                     manage_commands.create_choice("yearly", "매년"),
                     manage_commands.create_choice("duration", "특정 간격으로")]
                ),
                manage_commands.create_option(
                    "요일",
                    "(요일마다용) 요일을 옵션에 입력합니다. 절대 다른 옵션과 같이 사용하지 마세요!",
                    3,
                    False,
                    [manage_commands.create_choice("mon", "월요일"),
                     manage_commands.create_choice("tue", "화요일"),
                     manage_commands.create_choice("wed", "수요일"),
                     manage_commands.create_choice("thu", "목요일"),
                     manage_commands.create_choice("fri", "금요일"),
                     manage_commands.create_choice("sat", "토요일"),
                     manage_commands.create_choice("sun", "일요일")]
                ),
                manage_commands.create_option(
                    "월-일",
                    "(매년용, 양식: MM-DD) 월과 일을 옵션에 입력합니다. 양식을 지켜주시고, 절대 다른 옵션과 같이 사용하지 마세요!",
                    3,
                    False
                ),
                manage_commands.create_option(
                    "숫자입력",
                    "(매월/특정 간격용) 일 또는 간격을 입력합니다. 절대 다른 옵션과 같이 사용하지 마세요!",
                    4,
                    False
                )
            ]
        },
        {
            "name": "알림",
            "description": "알림 타입 알림 설정 명령어입니다.",
            "type": 1,
            "options": [
                manage_commands.create_option(
                    "이름",
                    "설정할 알림 타입 알림 이름",
                    3,
                    True
                ),
                manage_commands.create_option(
                    "분",
                    "울릴 시간의 분",
                    4,
                    True
                ),
                manage_commands.create_option(
                    "시간",
                    "울릴 시간의 시간 (24시간 기준)",
                    4,
                    True
                ),
                manage_commands.create_option(
                    "일",
                    "울릴 날짜, 오늘로 하고 싶으시다면 0으로 해주세요.",
                    4,
                    True
                ),
                manage_commands.create_option(
                    "월",
                    "울릴 월, 현재 월로 하고 싶으시다면 0으로 해주세요.",
                    4,
                    True
                ),
                manage_commands.create_option(
                    "년",
                    "울릴 년, 이번 년도로 하고 싶으시다면 0으로 해주세요.",
                    4,
                    True
                )
            ]
        }
    ]
))
