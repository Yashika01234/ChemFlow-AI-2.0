import numpy as np

def monte_carlo_yield(mean_yield: float, std_yield: float, trials: int = 5000, seed: int | None = None):
    if not 0 <= mean_yield <= 1:
        raise ValueError("mean_yield must be between 0 and 1")
    if std_yield < 0 or std_yield > 0.5:
        raise ValueError("std_yield must be between 0 and 0.5")
    if not 100 <= trials <= 100000:
        raise ValueError("trials must be between 100 and 100000")
    rng = np.random.default_rng(seed)
    samples = np.clip(rng.normal(mean_yield, std_yield, trials), 0, 1)
    hist, edges = np.histogram(samples, bins=12, range=(0, 1))
    return {
        "trials": trials,
        "mean": round(float(samples.mean()), 5),
        "median": round(float(np.median(samples)), 5),
        "std_dev": round(float(samples.std()), 5),
        "p05": round(float(np.quantile(samples, 0.05)), 5),
        "p95": round(float(np.quantile(samples, 0.95)), 5),
        "probability_above_80_percent": round(float(np.mean(samples >= 0.8)), 5),
        "histogram": [{"range_start": round(float(edges[i]), 3),
                       "range_end": round(float(edges[i+1]), 3),
                       "count": int(hist[i])} for i in range(len(hist))],
        "assumption": "Normal yield uncertainty clipped to [0, 1]; change the distribution if experimental evidence supports another model."
    }
