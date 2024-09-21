import matplotlib.pyplot as plt
import numpy as np
import exercise_code as mch


def sample_main():
    A_m2 = 1.0
    g_mpsps = 9.8
    a_m2 = np.pi*(0.1**2) # m^2
    h0_m = 2

    t_disc = mch.t_discharge(A_m2, h0_m, a_m2, g_mpsps)

    print(f"Theoretical discharge time: {t_disc:g} s")

    t_start_sec = 0.0
    t_end_sec = t_disc * 0.99

    num = mch.numerical_h(t_start_sec, t_end_sec, h0_m, a_m2, A_m2, g_mpsps)
    exact = mch.exact_h(t_start_sec, t_end_sec, h0_m, a_m2, A_m2, g_mpsps)

    plt.plot(num['t_array'], num['h_array'], label='Numerical')
    plt.plot(exact['t_array'], exact['h_array'], label='Exact')
    plt.xlabel('t(sec)')
    plt.ylabel('h(m)')
    plt.title("Torriceli's Law")
    plt.grid(True)
    plt.savefig('torricellis_law.png')


if "__main__" == __name__:
    sample_main()
