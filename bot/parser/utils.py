import logging
import sys
import random
import httpx

from user_agents import user_agent_list  # список из значений user-agent


def random_user_agent_headers():
    '''Возвращет рандомный user-agent и друге параметры для имитации запроса из браузера'''
    rnd_index = random.randint(0, len(user_agent_list) - 1)

    header = {
        'User-Agent': user_agent_list[rnd_index],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
    }

    return header
