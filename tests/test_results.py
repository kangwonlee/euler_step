import pathlib
import random
import sys


import matplotlib.pyplot as plt
import numpy as np
import numpy.testing as nt
import pytest


sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.absolute()))


# Import the module containing the functions to be tested.
# 테스트할 함수를 포함하는 모듈을 불러옵니다.
try:
    import exercise_code as mch
except ImportError as e:
    pytest.fail(
        f"Error importing 'my_code_here': {e}"
        f"'my_code_here'를 불러오는 중 오류가 발생했습니다. {e}"
    )


@pytest.fixture
def t_discharge_sec() -> float:
    return random.uniform(5.0, 20.0)


@pytest.fixture
def h0_m(a_m2:float, A_m2:float, g_mpsps:float, t_discharge_sec) -> float:
    # td = A h0 / a * sqrt(2 / (g h0))
    # td * (a / A) = h0 * sqrt(2 / g) * sqrt(1/h0)
    # td * (a / A) * sqrt(g / 2) = h0 * sqrt(1/h0)
    # h0 = (td * (a / A) * sqrt(g / 2))**2
    # h0 = ((td * a) / A) ** 2 * g * 0.5
    return ((t_discharge_sec * a_m2 / A_m2) ** 2) * (g_mpsps * 0.5)


@pytest.fixture
def h_m(h0_m:float) -> float:
    '''
    h to test dh_dt()
    '''
    return random.uniform(h0_m, h0_m*2.0)


@pytest.fixture
def a_m2() -> float:
    return random.uniform(0.01, 0.1)


@pytest.fixture
def A_m2() -> float:
    return random.uniform(0.1, 1.0)


@pytest.fixture
def g_mpsps() -> float:
    return random.gammavariate(9.8, 0.1)


@pytest.fixture
def v_mps(g_mpsps:float, h_m:float,) -> float:
    return (2.0 * g_mpsps * h_m)**0.5


@pytest.fixture
def q_m3ps(v_mps:float, a_m2:float,) -> float:
    return v_mps * a_m2 * (-1.0)


@pytest.fixture
def t_sec(t_discharge_sec:float) -> float:
    return t_discharge_sec * random.uniform(0.1, 0.2)


def test_dh_dt(t_sec:float, h_m:float, a_m2:float, q_m3ps:float, A_m2:float, g_mpsps:float):
    result = mch.dh_dt(t_sec, h_m, a_m2, A_m2, g_mpsps)

    msg = (
        f"input arguments: A={A_m2}, h0_m={h0_m}, a={a_m2}, g={g_mpsps}\n"
        f"입력 매개변수: A={A_m2}, h0_m={h0_m}, a={a_m2}, g={g_mpsps}\n"
        f"Expected: {t_discharge_sec}\n"
        f"예상값: {t_discharge_sec}\n"
        f"Got: {result}\n"
        f"받은 값: {result}\n"
    )

    assert isinstance(result, float), msg
    assert result == pytest.approx(q_m3ps / A_m2), msg


def test_t_discharge(h0_m:float, a_m2:float, A_m2:float, g_mpsps:float, t_discharge_sec:float):
    result = mch.t_discharge(A_m2, h0_m, a_m2, g_mpsps)

    msg = (
        f"input arguments: A={A_m2}, h0_m={h0_m}, a={a_m2}, g={g_mpsps}\n"
        f"입력 매개변수: A={A_m2}, h0_m={h0_m}, a={a_m2}, g={g_mpsps}\n"
        f"Expected: {t_discharge_sec}\n"
        f"예상값: {t_discharge_sec}\n"
        f"Got: {result}\n"
        f"받은 값: {result}\n"
    )

    assert isinstance(result, float), msg
    assert result == pytest.approx(t_discharge_sec), msg


@pytest.fixture
def t_start_sec(t_discharge_sec:float) -> float:
    '''
    start time of the simulation
    '''
    return t_discharge_sec * random.uniform(0.01, 0.02)


@pytest.fixture
def t_end_sec(t_discharge_sec:float) -> float:
    '''
    start time of the simulation
    '''
    return t_discharge_sec * random.uniform(0.80, 0.90)


def test_exact_h(
        t_start_sec:float, t_end_sec:float,
        h0_m:float, a_m2:float, A_m2:float, g_mpsps:float,
        t_discharge_sec:float):
    result = mch.exact_h(t_start_sec, t_end_sec, h0_m, a_m2, A_m2, g_mpsps)

    msg_arg = (
        f"input arguments: t_start = {t_start_sec}, t_end = {t_end_sec}, h0 = {h0_m}, a={a_m2}, A={A_m2}, g={g_mpsps}\n"
        f"입력 매개변수: t_start = {t_start_sec}, t_end = {t_end_sec}, h0 = {h0_m}, a={a_m2}, A={A_m2}, g={g_mpsps}\n"
    )

    assert isinstance(result, dict), (
        f"{msg_arg}Expected type: dict\n"
        f"예상 자료형: dict\n"
        f"Got type: {type(result)}\n"
        f"받은 자료형: {type(result)}\n"
    )

    assert set(result.keys()) == {'t_array', 'h_array', 'n'}, (
        f"{msg_arg}Expected keys: ['t_array', 'h_array', 'n']\n"
        f"예상 키: ['t_array', 'h_array', 'n']\n"
        f"Got keys: {list(result.keys())}\n"
        f"받은 키: {list(result.keys())}\n"
    )

    assert isinstance(result['t_array'], np.ndarray), (
        f"{msg_arg}Expected type of 't_array': numpy.ndarray\n"
        f"'t_array'의 예상 자료형: numpy.ndarray\n"
        f"Got type of 't_array': {type(result['t_array'])}\n"
        f"받은 't_array'의 자료형: {type(result['t_array'])}\n"
    )

    assert isinstance(result['h_array'], np.ndarray), (
        f"{msg_arg}Expected type of 'h_array': numpy.ndarray\n"
        f"'h_array'의 예상 자료형: numpy.ndarray\n"
        f"Got type of 'h_array': {type(result['h_array'])}\n"
        f"받은 'h_array'의 자료형: {type(result['h_array'])}\n"
    )

    assert isinstance(result['n'], int), (
        f"{msg_arg}Expected type of 'n': int\n"
        f"'n'의 자료형: i예상 nt\n"
        f"Got type of 'n': {type(result['n'])}\n"
        f"받은 'n'의 자료형: {type(result['n'])}\n"
    )

    assert len(result['t_array']) == len(result['h_array']) == result['n'], (
        f"{msg_arg}Expected length of 't_array', 'h_array': {result['n']}\n"
        f"'t_array', 'h_array'의 예상 길이: {result['n']}\n"
        f"Got length of 't_array': {len(result['t_array'])}\n"
        f"받은 't_array'의 길이: {len(result['t_array'])}\n"
        f"Got length of 'h_array': {len(result['h_array'])}\n"
        f"받은 'h_array'의 길이: {len(result['h_array'])}\n"
    )

    t_array = np.array(result['t_array'])

    expected_h_m = get_expected_h(h0_m, t_discharge_sec, t_array)

    msg = (
        f"{msg_arg}Expected: {expected_h_m}\n"
        f"예상값: {expected_h_m}\n"
        f"Got: {result['h_array']}\n"
        f"받은 값: {result['h_array']}\n"
    )

    try:
        nt.assert_allclose(result['h_array'], expected_h_m, err_msg=msg)
    except AssertionError as e:
        plot_results(
            t_start_sec=t_start_sec, t_end_sec=t_end_sec,
            t_expected_array=np.array(result['t_array']), h_expected_array=expected_h_m,
            h0_m=h0_m, a_m2=a_m2, A_m2=A_m2, g_mpsps=g_mpsps,
            t_discharge_sec=t_discharge_sec,
            exact=result,)
        raise e


def get_expected_h(h0_m:float, t_discharge_sec:float, t_array:np.ndarray) -> np.ndarray:
    return h0_m * (1.0 - np.array(t_array) / t_discharge_sec)**2


def test_numerical_h(
        t_start_sec:float, t_end_sec:float,
        h0_m:float, a_m2:float, A_m2:float, g_mpsps:float,
        t_discharge_sec:float):
    result = mch.numerical_h(t_start_sec, t_end_sec, h0_m, a_m2, A_m2, g_mpsps)

    msg_arg = (
        f"input arguments: t_start = {t_start_sec}, t_end = {t_end_sec}, h0 = {h0_m}, a={a_m2}, A={A_m2}, g={g_mpsps}\n"
        f"입력 매개변수: t_start = {t_start_sec}, t_end = {t_end_sec}, h0 = {h0_m}, a={a_m2}, A={A_m2}, g={g_mpsps}\n"
    )

    assert isinstance(result, dict), (
        f"{msg_arg}Expected type: dict\n"
        f"예상 자료형: dict\n"
        f"Got type: {type(result)}\n"
        f"받은 자료형: {type(result)}\n"
    )

    assert set(result.keys()) == {'t_array', 'h_array', 'n'}, (
        f"{msg_arg}Expected keys: ['t_array', 'h_array', 'n']\n"
        f"예상 키: ['t_array', 'h_array', 'n']\n"
        f"Got keys: {list(result.keys())}\n"
        f"받은 키: {list(result.keys())}\n"
    )

    assert isinstance(result['t_array'], np.ndarray), (
        f"{msg_arg}Expected type of 't_array': numpy.ndarray\n"
        f"'t_array'의 예상 자료형: numpy.ndarray\n"
        f"Got type of 't_array': {type(result['t_array'])}\n"
        f"받은 't_array'의 자료형: {type(result['t_array'])}\n"
    )

    assert isinstance(result['h_array'], np.ndarray), (
        f"{msg_arg}Expected type of 'h_array': numpy.ndarray\n"
        f"'h_array'의 예상 자료형: numpy.ndarray\n"
        f"Got type of 'h_array': {type(result['h_array'])}\n"
        f"받은 'h_array'의 자료형: {type(result['h_array'])}\n"
    )

    assert isinstance(result['n'], int), (
        f"{msg_arg}Expected type of 'n': int\n"
        f"'n'의 자료형: i예상 nt\n"
        f"Got type of 'n': {type(result['n'])}\n"
        f"받은 'n'의 자료형: {type(result['n'])}\n"
    )

    assert len(result['t_array']) == len(result['h_array']) == result['n'], (
        f"{msg_arg}Expected length of 't_array', 'h_array': {result['n']}\n"
        f"'t_array', 'h_array'의 예상 길이: {result['n']}\n"
        f"Got length of 't_array': {len(result['t_array'])}\n"
        f"받은 't_array'의 길이: {len(result['t_array'])}\n"
        f"Got length of 'h_array': {len(result['h_array'])}\n"
        f"받은 'h_array'의 길이: {len(result['h_array'])}\n"
    )

    expected_h_m = get_expected_h(h0_m, t_discharge_sec, np.array(result['t_array']))

    msg = (
        f"{msg_arg}Exact: {expected_h_m}\n"
        f"엄밀해: {expected_h_m}\n"
        f"Got: {result['h_array']}\n"
        f"받은 값: {result['h_array']}\n"
    )

    try:
        nt.assert_allclose(result['h_array'], expected_h_m, rtol=0.4, err_msg=msg)
    except AssertionError as e:
        plot_results(
            t_start_sec=t_start_sec, t_end_sec=t_end_sec,
            t_expected_array=np.array(result['t_array']), h_expected_array=expected_h_m,
            h0_m=h0_m, a_m2=a_m2, A_m2=A_m2, g_mpsps=g_mpsps,
            t_discharge_sec=t_discharge_sec,
            numerical=result,)
        raise e


def plot_results(
        t_start_sec:float, t_end_sec:float, 
        t_expected_array:np.ndarray, h_expected_array:np.ndarray,
        h0_m:float, a_m2:float, A_m2:float, g_mpsps:float,
        t_discharge_sec:float,
        numerical:dict=None, exact:dict=None,):

    if exact is None:
        exact = mch.exact_h(t_start_sec, t_end_sec, h0_m, a_m2, A_m2, g_mpsps)
    if numerical is None:
        numerical = mch.numerical_h(t_start_sec, t_end_sec, h0_m, a_m2, A_m2, g_mpsps)

    fig, ax = plt.subplots()
    ax.plot(exact['t_array'], exact['h_array'], 'o-', label='Exact (result)')
    ax.plot(numerical['t_array'], numerical['h_array'], '.-', label='Numerical (result)')
    ax.plot(t_expected_array, h_expected_array, 'r-', label='Exact (expected)')
    ax.axvline(t_discharge_sec, color='r', linestyle='--', label='Discharge time')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Height (m)')
    ax.grid(True)
    ax.legend()
    plt.savefig('torricellis_law_result.png')


if __name__ == "__main__":
    pytest.main([__file__])
