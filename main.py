import numpy as np
import matplotlib.pyplot as plt

# 工程数と製品数
num_processes = 5
num_products = 100

# 作業者数と処理時間（例: 5工程ぶん）
workers = [3, 2, 4, 2, 3]               # 各工程の作業者数
process_time = [6, 8, 4, 10, 5]         # 各工程の1製品あたりの処理時間（分）

# 製品ごとの処理開始時間と終了時間（各工程）
start_time = np.zeros((num_products, num_processes))
end_time = np.zeros((num_products, num_processes))

# 各工程の作業者ごとの次に空く時間
worker_available = [np.zeros(w) for w in workers]

for p in range(num_products):
    for proc in range(num_processes):
        # 作業者で一番早く空く人を探す
        available = worker_available[proc]
        earliest = np.min(available)
        # 開始時間は「前工程終了後」か「作業者が空く時点」
        if proc == 0:
            start = earliest
        else:
            start = max(end_time[p][proc-1], earliest)

        end = start + process_time[proc]

        start_time[p][proc] = start
        end_time[p][proc] = end

        # 作業者の空き時間を更新
        idx = np.argmin(available)
        worker_available[proc][idx] = end

# WIP数を時間ごとにカウント
time_range = np.linspace(0, np.max(end_time), 200)
wip = np.zeros_like(time_range)

for t_idx, t in enumerate(time_range):
    for proc in range(num_processes):
        # proc+1に渡る前に滞留中かどうか
        for p in range(num_products):
            if start_time[p][proc] <= t < end_time[p][proc]:
                wip[t_idx] += 1

# 可視化
plt.plot(time_range, wip)
plt.xlabel('Time (min)')
plt.ylabel('WIP count')
plt.title('WIP vs Time (across all processes)')
plt.grid(True)
plt.show()
