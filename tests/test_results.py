import pathlib
import random
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.absolute()))

# Import the module containing the functions to be tested.
# 테스트할 함수를 포함하는 모듈을 불러옵니다.
try:
    import my_code_here as mch
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

    assert isinstance(result, float), (
        f"input arguments: t={t_sec}, h={h_m}, a={a_m2}, A={A_m2}, g={g_mpsps}\n"
        f"입력 매개변수: t={t_sec}, h={h_m}, a={a_m2}, A={A_m2}, g={g_mpsps}\n"
        f"Expected: {q_m3ps / A_m2}\n"
        f"예상값: {q_m3ps / A_m2}\n"
        f"Got: {result}\n"
        f"받은 값: {result}\n"
    )

    assert result == pytest.approx(q_m3ps / A_m2), (
        f"input arguments: t={t_sec}, h={h_m}, a={a_m2}, A={A_m2}, g={g_mpsps}\n"
        f"입력 매개변수: t={t_sec}, h={h_m}, a={a_m2}, A={A_m2}, g={g_mpsps}\n"
        f"Expected: {q_m3ps / A_m2}\n"
        f"예상값: {q_m3ps / A_m2}\n"
        f"Got: {result}\n"
        f"받은 값: {result}\n"
    )


if __name__ == "__main__":
    pytest.main([__file__])
