# src/runtime/sim_open_loop.py
from __future__ import annotations
import os, time, argparse, sys
import numpy as np
import matplotlib.pyplot as plt

# Add project root to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.plant.power_avg import BoostParams, BoostParasitics, BoostAveragedPlant

def steady_state_ic(Vin: float, R: float, D: float) -> tuple[float, float]:
    """Equilibrium ideal (điểm làm việc) để bỏ quá độ khởi động."""
    vo = Vin / max(1e-12, (1.0 - D))
    iL = Vin / (R * max(1e-12, (1.0 - D))**2)
    return iL, vo

def main():
    ap = argparse.ArgumentParser("Open-loop boost: continuous plant + ZOH (no save)")
    ap.add_argument("--L", type=float, default=100e-6)
    ap.add_argument("--C", type=float, default=1e-3)
    ap.add_argument("--Vin", type=float, default=24.0)
    ap.add_argument("--R", type=float, default=4.5)
    ap.add_argument("--duty", type=float, default=0.55)
    ap.add_argument("--Ts", type=float, default=10e-5)
    ap.add_argument("--duration", type=float, default=0.2)
    ap.add_argument("--init", choices=["equil","zero"], default="zero",
                    help="equil: khởi tạo tại điểm làm việc; zero: iL=vo=0")
    
    DEFAULT_NON_IDEAL = True  # đổi True/False tùy lần chạy
    ap.add_argument("--non_ideal", action="store_true", default=DEFAULT_NON_IDEAL,
                help="bật mô hình phi lý tưởng")
    ap.add_argument("--ideal", dest="non_ideal", action="store_false",
                help="tắt non_ideal khi cần")

    ap.add_argument("--rL", type=float, default=0.08)
    ap.add_argument("--rDS", type=float, default=0.0)
    ap.add_argument("--VF", type=float, default=0.0)
    ap.add_argument("--RF", type=float, default=0.0)
    args = ap.parse_args()

    par = BoostParasitics(rL=args.rL, rDS=args.rDS, VF=args.VF, RF=args.RF)
    cfg = BoostParams(L=args.L, C=args.C, Vin=args.Vin, R=args.R,
                      d_min=0.02, d_max=0.98, non_ideal=args.non_ideal, par=par)
    plant = BoostAveragedPlant(cfg)

    if args.init == "zero":
        plant.reset((0.0, 0.0))
    else:
        # equilibrium ideal (gần đúng cả khi bật non_ideal)
        plant.reset(steady_state_ic(args.Vin, args.R, args.duty))

    Ts, T = args.Ts, args.duration
    n = int(T / Ts)
    t = 0.0
    t_list = np.empty(n); i_list = np.empty(n); v_list = np.empty(n)
    for k in range(n):
        x, _ = plant.propagate(t, t + Ts, duty=args.duty)  # ZOH duty
        t += Ts
        t_list[k], i_list[k], v_list[k] = t, x[0], x[1]

    # Vẽ không lưu file
    fig, ax = plt.subplots(2, 1, figsize=(8,5), sharex=True)
    ax[0].plot(t_list, i_list); ax[0].set_ylabel("iL [A]")
    ax[1].plot(t_list, v_list); ax[1].set_ylabel("vo [V]"); ax[1].set_xlabel("t [s]")
    fig.suptitle("Boost open-loop (continuous plant, ZOH duty)")
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
