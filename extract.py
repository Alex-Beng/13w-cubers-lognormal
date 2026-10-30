import json, re, math, sys, time, os
import numpy as np
from scipy import stats, special

_HERE = os.path.dirname(os.path.abspath(__file__))
# 原始抓取数据（379MB，不入库）：默认从环境变量 SRC 或同级 scan-1e8.ndjson 读取
SRC = os.environ.get("SRC") or os.path.join(_HERE, "scan-1e8.ndjson")
OUT = os.path.join(_HERE, "stats.json")

t0 = time.time()
subs = []   # 秒
pbs = []
tps = []
turn = []
mc = []
reg = []
rank = []
n_lines = 0
bad = 0
rx_sub = re.compile(r'"ability":\{"sub":(-?\d+)')
rx_pb = re.compile(r'"pb":(-?\d+)')
rx_tps = re.compile(r'"tps":([-\d.]+)')
rx_turn = re.compile(r'"turn":([-\d.]+)')
rx_mc = re.compile(r'"career":\{"registerDays":(\d+),"matchCount":(\d+)\}')
rx_rr = re.compile(r'"rankRate":(-?\d+)')

with open(SRC, 'r', encoding='utf-8', errors='replace') as f:
    for line in f:
        n_lines += 1
        if '"exists":true' not in line:
            continue
        m = rx_sub.search(line)
        if not m:
            bad += 1; continue
        s = int(m.group(1))
        if s > 0:
            v = s / 1000.0
            if v < 3600:   # 剔除明显异常
                subs.append(v)
        mm = rx_mc.search(line)
        if mm:
            reg.append(int(mm.group(1))); mc.append(int(mm.group(2)))
        if s > 0:
            m2 = rx_pb.search(line)
            if m2 and int(m2.group(1)) > 0:
                pbs.append(int(m2.group(1)) / 1000.0)
            m3 = rx_tps.search(line)
            if m3:
                t = float(m3.group(1))
                if t > 0: tps.append(t)
            m4 = rx_turn.search(line)
            if m4:
                t = float(m4.group(1))
                if t > 0: turn.append(t)
            m5 = rx_rr.search(line)
            if m5 and int(m5.group(1)) > 0:
                rank.append(int(m5.group(1)))

S = np.array(subs, dtype=np.float64)
print("parsed", len(S), "lines", n_lines, "bad", bad, "in", round(time.time()-t0,1), "s")

def moments(x):
    x = np.asarray(x, float)
    m = x.mean(); sd = x.std(ddof=0)
    sk = stats.skew(x); ku = stats.kurtosis(x, fisher=True)
    return dict(n=int(len(x)), mean=float(m), sd=float(sd), min=float(x.min()),
                max=float(x.max()), median=float(np.median(x)),
                skew=float(sk), kurt=float(ku))

linear = moments(S)
L = np.log(S)
logm = moments(L)

# 截尾到 (0,300] 做“正常玩家”主群体（官方直方图上界）
Sc = S[(S > 0) & (S <= 300)]
linear_c = moments(Sc)
Lc = np.log(Sc); logm_c = moments(Lc)

# 线性正态拟合
mu_lin, sd_lin = linear_c['mean'], linear_c['sd']
# 对数正态拟合（MLE）
mu_l, sd_l = Lc.mean(), Lc.std(ddof=0)

# 正态性检验（对数尺度显著性）
ks_log = stats.kstest((Lc - mu_l) / sd_l, 'norm')
# D'Agostino 检验样本量过大几乎必然拒绝，作为对照
da_log = stats.normaltest((Lc - mu_l) / sd_l)
# 分位点比对
qs = [0.01, 0.05, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
q_emp = {str(q): float(np.quantile(Sc, q)) for q in qs}
q_fit = {str(q): float(math.exp(mu_l + sd_l * special.ndtri(q))) for q in qs}
# 线性正态在同样的分位点会给出什么（说明线性模型离谱）
q_lin = {str(q): float(mu_lin + sd_lin * special.ndtri(q)) for q in qs}

# 直方图：线性(等宽) 与 对数轴
def hist(x, lo, hi, bins, log=False):
    x = np.asarray(x)
    x = x[(x > lo) & (x <= hi)]
    if log:
        e = np.geomspace(lo, hi, bins + 1)
    else:
        e = np.linspace(lo, hi, bins + 1)
    c, _ = np.histogram(x, bins=e)
    return dict(edges=[float(v) for v in e], counts=[int(v) for v in c], total=int(len(x)),
                below=int((np.asarray(x_full) <= lo).sum()) if False else 0)

x_full = Sc
h_lin = hist(Sc, 0, 300, 60, False)
h_log = hist(Sc, 1, 300, 60, True)
h_fine = hist(Sc, 0, 120, 120, False)
h_logfine = hist(Sc, 1, 300, 90, True)

# 分桶统计：TPS / TURN / 对局数 与成绩的关系（证明乘法链条）
tps_a = np.array(tps); turn_a = np.array(turn)
corr_tps = float(np.corrcoef(tps_a, np.log(tps_a))[0,1]) if len(tps_a) else 0

# 时间按秒/按对数区间的“挡位”
bands = [0,3,4,5,6,7,8,9,10,12,15,20,30,45,60,90,120,180,300,1e9]
bc, _ = np.histogram(Sc, bins=bands)
band_rows = [(bands[i], bands[i+1], int(bc[i])) for i in range(len(bc))]

# 用户“倍率”直觉：中位 40s，最快 2s -> 20x
res = dict(
    meta=dict(source=os.path.basename(SRC), parsed=int(len(S)), lines=n_lines,
              generated=time.strftime('%Y-%m-%dT%H:%M:%S')),
    raw=dict(linear=linear, log=logm),
    trimmed=dict(cut=300.0, linear=linear_c, log=logm_c,
                 mu=float(mu_l), sigma=float(sd_l),
                 linear_mu=float(mu_lin), linear_sd=float(sd_lin)),
    tests=dict(ks_log_p=float(ks_log.pvalue), ks_log_D=float(ks_log.statistic),
               dagostino_log_p=float(da_log.pvalue),
               dagostino_log_stat=float(da_log.statistic)),
    quantiles=dict(emp=q_emp, lognormal=q_fit, linear=q_lin),
    hist=dict(lin=h_lin, log=h_log, fine=h_fine, logfine=h_logfine),
    bands=[dict(lo=a, hi=b, n=c) for a, b, c in band_rows],
    other=dict(
        pb_n=int(len(pbs)), pb_mean=float(np.mean(pbs)) if pbs else 0,
        tps_n=int(len(tps)), tps_mean=float(np.mean(tps)) if tps else 0,
        tps_median=float(np.median(tps)) if tps else 0,
        turn_n=int(len(turn)), turn_mean=float(np.mean(turn)) if turn else 0,
        turn_median=float(np.median(turn)) if turn else 0,
        mc_n=int(len(mc)), mc_mean=float(np.mean(mc)) if mc else 0,
        mc_median=float(np.median(mc)) if mc else 0,
        reg_mean=float(np.mean(reg)) if reg else 0,
        rank_n=int(len(rank)),
    ),
)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=1)

print(json.dumps({'linear': linear, 'log': logm, 'trim_lin': linear_c, 'trim_log': logm_c,
                  'mu': mu_l, 'sigma': sd_l, 'ks_p': ks_log.pvalue,
                  'q_emp': q_emp, 'q_fit': q_fit, 'q_lin': q_lin,
                  'bands': band_rows, 'other': res['other']}, ensure_ascii=False, indent=1))
