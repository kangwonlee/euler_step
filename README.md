
# Torricelli's Law : How long does it takes to drain a water tank?<br>토리첼리의 정리 : 물탱크의 물을 빼는데 걸리는 시간은 ?

## Description<br>설명

* Suppose there is a circular cylindical water tank with following parameters.<br>다음 매개변수의 원통형 물탱크를 생각해 보자.

parameter<br>매개변수 | unit<br>단위 | description<br>설명
:-------:|:-----:|-----
$V(t)$ | $m^3$ | volume of the water in the tank<br>탱크에 들어있는 물의 부피
$A$ | $m^2$ | cross section area of the tank<br>원통형 탱크의 단면적
$a$ | $m^2$ | cross section area of the drain at the bottom of the tank<br>물탱크 바닥의 배수구의 단면적
$h(t)$ | $m$ | water level of the tank<br>탱크의 물의 높이
$g$ | $$m/{sec^2}$$ | gravitational acceleration<br>중력가속도

* The tank has a cross-sectional area of `A` $m^2$ and initially has an initial water level of `h0` $m$ at time `t` = 0 sec.<br>해당 탱크의 단면적은 `A` $m^2$ 이고 `t` = 0 $sec$ 일 때 초기 수위 `h0` $m$ 까지 물이 차 있다.

* At the bottom of the tank there is a closed hole with cross section area `a` $m^2$.<br>물탱크의 바닥에 단면적 `a` 인 구멍이 막혀 있다.

* If you open the hole, the water will flow out due to gravity, thus the water level will decrease.<br>구멍의 마개를 열면, 중력에 의해 물이 흘러나올 것이며, 따라서 수위는 낮아질 것이다.

* Let's express this as a differential equation.<br>이를 미분방정식으로 표현해 보자.

$$
    \frac{d}{dt}h(t) = \frac{1}{A}q(t)= -\frac{a}{A}\sqrt{2 g h(t)}
$$

* The theoretical discharge time is known as follows.<br>배수 시간의 엄밀해는 다음과 같다고 알려져 있다.

$$
T_{discharge}=\frac{V}{A_A}\sqrt{\frac{2}{gH}}=\frac{AH}{a}\sqrt{\frac{2}{gH}}
$$

* Also, the exact solution of `h(t)` is known as follows.<br>또한 `h(t)`의 엄밀해도 다음과 같다고 알려져 있다.

$$
h(t)=H\left(1-\frac{t}{T_{discharge}}\right)^2
$$

## Implementation<br>구현

* Please implement the following functions in the `my_code_here.py` file.<br>다음 함수를 `my_code_here.py` 파일에 구현하시오.

| function<br>함수 | return type<br>반환 형 | unit<br>단위 | return value<br>반환값 |
|:--------:|:-----------:|:-----------:|:-----------:|
| `dh_dt(t, h, a, A, g)` | `float` | $m/s$ | The time derivative of the height.<br> 높이의 시간에 대한 변화율. |
| `numerical_h(t_start, t_end, h0, a, A, g)` | `dict` | - | Numerical approximation solution of the differential equation above. (see below) <br> 위 미분방정식의 수치 근사해. (아래 참고) |
| `t_discharge(A, h0, a, g)` | `float` | sec | Exact solution of the drain time.<br>배수 시간의 엄밀해. |
| `exact_h(t_start, t_end, h0, a, A, g)` | `dict` | - | Exact solution of the differential equation above. (see below) <br> 위 미분방정식의 엄밀해. (아래 참고) |

* The functions will take the following arguments.<br>해당 함수들은 아래와 같은 매개변수를 받아들일것임.

| argument<br>매개변수 | type<br>형 | unit<br>단위 | description<br>설명 |
|:--------:|:-----------:|:-----------:|:-----------:|
| `t` | `float` | $sec$ | time to calculate $\frac{d}{dt}h(t)$<br> $\frac{d}{dt}h(t)$을 계산할 시간 |
| `t_start` | `float` | $sec$ | start time of the solution <br> 엄밀해 또는 수치해를 계산할 시작 시간 |
| `t_end` | `float` | $sec$ | end time of the solution <br> 엄밀해 또는 수치해를 계산할 마지막 시간 |
| `h` | `float` | $m$ | current height<br> 현재 높이 |
| `h0` | `float` | $m$ | initial height<br> 초기 높이 |
| `a` | `float` | $m^2$ | cross section area of the drain<br> 배수구의 단면적 |
| `A` | `float` | $m^2$ | cross section area of the tank<br> 탱크의 단면적 |
| `g` | `float` | $m/s/s$ | gravitatinal acceleration<br> 중력가속도 |

* Please return a `dict` with following keys regarding the functions `numerical_h()` and `exact_h()`.<br>과제 함수 `numerical_h()`, `exact_h()` 에 대해서는, 다음 key를 담은 `dict`를 반환하시오.

| return value key<br>반환값 key | type<br>형 |unit<br>단위 | value |
|:--------:|:-----------:|:-----------:|:-----------:|
| `'t_array'` | `numpy.ndarray` | $sec$ | time array of the exact or numerical solution. The first and last values would be `t_start` and `t_end` respectively. <br>엄밀해 또는 수치해의 시간 배열. 첫번째와 마지막 값은 각각 `t_start`와 `t_end`. |
| `'h_array'` | `numpy.ndarray` | $m$ | array of the height at each time of `'time_array'`. The first value would be `h0`. <br>`'time_array'`의 각 시간에서의 높이. 첫번째 값은 `h0` |
| `'n'` | `int` | - | length of each array<br>각 배열의 길이 |

### File Table<br>파일 목록

| File or Folder<br>파일 또는 폴더 | Type<br>형식 | Purpose<br>목적 | Description<br>설명 | Permission<br>권한 |
|-----------------------|----------|---------------------------|-------------------------------------------------------------------------------------|:-------------:|
| `my_code_here.py`    | Python   | Main Script<br>주 파일 | Write your code to solve the assignment problem in this file.<br>이 파일에 과제 코드를 작성.  | Modify<br>수정 |
| `sample.py`           | Python   | Example Usage<br>사용 예 | This file demonstrates how to use the assignment code.<br>과제 코드 사용 예. | Read-Only<br>읽기 전용 |
| `.github/workflows/` | YAML     | Continuous Integration/Continuous Deployment Configuration<br>연속 통합/배포 설정 | Defines automated workflows for testing and deployment.<br>시험 배포 자동화 절차 설정. | Read-Only<br>읽기 전용 |
| `tests/`              | Python   | Test Cases<br>시험 파일 | Tests to check the correctness of your code.<br>코드가 맞는지 시험. | Read-Only<br>읽기 전용 |

### Allowed Modules<br>허용 모듈 목록

* In the `my_code_here.py` file, please `import` these modules only.<br>`my_code_here.py` 파일에서는 아래 모듈만 `import` 바랍니다.

| module<br>모듈 | description<br>설명 |
|:--------:|:-----------:|
| `numpy` | numpy |
| `scipy.integrate` | numerical solver<br>수치 해법 |

## Grading<br>평가

| Criteria<br>기준	| Points<br>배점 |
|:---------:|:------:|
| Python Grammar<br>파이썬 문법	| 2 |
| Coding Style<br>모든 코드는 함수 안에	| 1 |
| Final Result<br>최종 결과	| 2 |


## Example<br>예

* Please run `sample.py` file to see an example of how to use the functions and visualize the results. <br>해당 함수들의 사용법과 해당 결과를 시각화 하는 법에 대해서는 `sample.py` 를 실행시켜 보기 바랍니다.

## References<br>참고문헌

* [Torricelli's law](https://en.wikipedia.org/wiki/Torricelli%27s_law)<br>[토리첼리의 정리](https://ko.wikipedia.org/wiki/토리첼리의_정리)

## NOTICE REGARDING STUDENT SUBMISSIONS<br>제출 결과물에 대한 알림

* Your submissions for this assignment may be used for various educational purposes. These purposes may include developing and improving educational tools, research, creating test cases, and training datasets.<br>제출 결과물은 다양한 교육 목적으로 사용될 수 있을 밝혀둡니다. (교육 도구 개발 및 개선, 연구, 테스트 케이스 및 교육용 데이터셋 생성 등).

* The submissions will be anonymized and used solely for educational or research purposes. No personally identifiable information will be shared.<br>제출된 결과물은 익명화되어 교육 및 연구 목적으로만 사용되며, 개인 식별 정보는 공유되지 않을 것입니다.

* If you do not wish to have your submission used for any of these purposes, please inform the instructor before the assignment deadline.<br>위와 같은 목적으로 사용되기 원하지 않는 경우, 과제 마감일 전에 강사에게 알려주기 바랍니다.
