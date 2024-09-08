import functools
import json
import logging
import pathlib
import os
from typing import Dict, Tuple

import pytest
import requests


import set_path


HEADER = Dict[str, str]
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


logging.basicConfig(level=logging.INFO)


if not GOOGLE_API_KEY:
    pytest.fail('API KEY NOT Available')


@pytest.fixture
def report_paths() -> Tuple[pathlib.Path]:
    result = []
    for e_key in os.environ:
        if e_key.endswith('_REPORT'):
            report_path = pathlib.Path(os.environ[e_key])
            assert report_path.exists(), f"does not exist : {report_path}"
            assert report_path.is_file(), f"not a file : {report_path}"
            result.append(report_path)

    assert result, "Could not find report filenames"

    return tuple(result)


@functools.lru_cache
def url() -> str:
    return f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_API_KEY}'


@functools.lru_cache
def header() -> HEADER:
    return {'Content-Type': 'application/json'}


@functools.lru_cache
def assignment_code() -> str:
    return set_path.script_path().read_text()


@functools.lru_cache
def assignment_instruction() -> str:
    return (set_path.proj_folder() / 'README.md').read_text()


def ask_gemini(question:str, url=url(), header=header()) -> str:
    data = {'contents': [{'parts': [{'text': question}]}]}

    response = requests.post(url, headers=header, json=data)

    if response.status_code == 200:
        result = response.json()
        # will show result later
    else:
        print(f"Error: {response.status_code}, {response.text}")

    results = []

    for part in result['candidates'][0]['content']['parts']:
        results.append(part['text'])

    answer = '\n'.join(results)
    return answer


def test_json_reports(report_paths:Tuple[pathlib.Path]):
    message_count = gemini_qna(report_paths)

    assert 0 == message_count, (
        "\nplease check Captured stdout call\n"
        "Captured stdout call 메시지를 확인하시오"
    )


def gemini_qna(report_paths):
    message_count = 0

    for report_path in report_paths:
        data = json.loads(report_path.read_text())

        for r in data['tests']:
            if r['outcome'] != 'passed':
                message_count += 1
                print((f"* {r['nodeid']} ").ljust(60, '*'))
                print(
                    ask_gemini(
                        get_question(r['call']['longrepr'])
                    )
                )

    return message_count


def get_question(longrepr:str) -> str:
    return (
        get_question_header() + f"{longrepr}\n" + get_question_footer()
    )


@functools.lru_cache
def get_question_header() -> str:
    return (
        "# Please explain the cause of the test result in simple sentences.\n"
        "# 숙제 답안으로 제출한 코드가 오류를 일으킨 원인을 간결한 문장으로 설명하시오:\n"
        "## Begin test message 오류 메시지 시작\n"
    )


@functools.lru_cache
def get_question_footer() -> str:
    return (
        "## End test message 오류 메시지 끝\n"
        "## Begin assignment code  숙제 제출 코드 시작\n"
        f"{assignment_code()}\n"
        "## End assignment code 숙제 제출 코드 끝\n"
        "## Begin assignment instructions 과제 지침 시작\n"
        f"{assignment_instruction()}\n"
        "## End assignment instructions 과제 지침 끝\n"
    )


if "__main__" == __name__:
    pytest.main([__file__])
