# Oracle SQL + Python DTW 유사도 계산

## 1. Oracle SQL 예시

```sql
SELECT * /*+ parallel(20) */
FROM TABLE (
    apGroupEvalParallel (
        cursor (
            SELECT PRODUCT_ID, LOT_ID, EQP_ID, ST_TIME, PARAMETER_ID, VALUE
            FROM TRACE_DATA
            WHERE LOT_ID = 'LOT001'
              AND PRODUCT_ID = 'PRX_0283'
              AND EQP_ID = 'EQP_321'
              AND ST_TIME BETWEEN TIMESTAMP '2022-10-23 00:00:00.000'
                              AND TIMESTAMP '2022-10-23 23:59:59.999'
        ), 
        cursor (
            SELECT PRODUCT_ID, LOT_ID, EQP_ID, ST_TIME, PARAMETER_ID, VALUE
            FROM GOLDEN_EQP_REF
            WHERE PRODUCT_ID = 'PRX_0283'
              AND EQP_ID = 'EQP_321'
        ),
        'SELECT CAST(NULL AS VARCHAR2(40)) PARAMETER_ID, 1.0 SIMILARITY FROM DUAL',
        'EQP_ID, PRODUCT_ID, LOT_ID, PARAMETER_ID',
        'DefectUtil:FastDTW'   -- FastDTW 내부에서 자동으로 Z-정규화 적용
    )
);
```

이 SQL은 Oracle의 **파이프라인 테이블 함수**를 이용하여
- 실제 설비 데이터(TRACE_DATA)
- 골든 데이터(GOLDEN_EQP_REF)

를 Python 함수 `DefectUtil.FastDTW`로 넘겨주고,
유사도를 계산하여 행 집합으로 반환합니다.

---

## 2. Z-정규화 적용

- `VALUE` 시계열은 DTW 계산 전에 **Z-정규화**(평균 0, 표준편차 1) 처리합니다.
- SQL에는 옵션을 넣지 않아도, Python 함수 내부에서 기본 처리됩니다.

---

## 3. DefectUtil.py

```python
import pandas as pd
import numpy as np

def _zscore(x: np.ndarray) -> np.ndarray:
    """Z-정규화: 평균 0, 표준편차 1"""
    x = np.asarray(x, dtype=float)
    mu = np.nanmean(x)
    sigma = np.nanstd(x)
    if sigma == 0 or np.isnan(sigma):
        return np.zeros_like(x)
    return (x - mu) / sigma

def _dtw_distance(a: np.ndarray, b: np.ndarray) -> float:
    """Classic DTW 거리 계산"""
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return float("inf")

    dp = np.full((n + 1, m + 1), np.inf)
    dp[0, 0] = 0.0

    for i in range(1, n + 1):
        ai = a[i - 1]
        for j in range(1, m + 1):
            bj = b[j - 1]
            cost = abs(ai - bj)
            dp[i, j] = cost + min(
                dp[i - 1, j],    # 삽입
                dp[i, j - 1],    # 삭제
                dp[i - 1, j - 1] # 매칭
            )
    return float(dp[n, m])

def _prep_series(df: pd.DataFrame) -> pd.DataFrame:
    """ST_TIME 기준 정렬, 중복 시간 평균, NaN 제거"""
    out = df.copy()
    out["ST_TIME"] = pd.to_datetime(out["ST_TIME"])
    out = out.sort_values("ST_TIME").groupby("ST_TIME", as_index=False)["VALUE"].mean()
    out = out.dropna(subset=["VALUE"])
    return out

def _series_to_array(df_group: pd.DataFrame, z_norm: bool = True) -> np.ndarray:
    """그룹별 시계열을 numpy array로 변환"""
    series_df = _prep_series(df_group[["ST_TIME", "VALUE"]])
    arr = series_df["VALUE"].to_numpy()
    if z_norm:
        arr = _zscore(arr)
    return arr

def FastDTW(df: pd.DataFrame, df_ref: pd.DataFrame) -> pd.DataFrame:
    """
    df vs df_ref를 DTW로 비교하여 PARAMETER_ID별 유사도를 반환.
    SQL 테이블 함수가 PARAMETER_ID 단위로 호출하기 때문에
    결과는 항상 한 PARAMETER_ID에 대한 1건임.
    """
    required_cols = {"PRODUCT_ID", "LOT_ID", "EQP_ID", "ST_TIME", "PARAMETER_ID", "VALUE"}
    for name, d in [("df", df), ("df_ref", df_ref)]:
        missing = required_cols - set(d.columns)
        if missing:
            raise ValueError(f"{name} is missing columns: {sorted(missing)}")

    if df.empty or df_ref.empty:
        return pd.DataFrame({"PARAMETER_ID": [], "SIMILARITY": []})

    param_id = df["PARAMETER_ID"].iloc[0]

    a = _series_to_array(df)
    b = _series_to_array(df_ref)

    if len(a) == 0 or len(b) == 0:
        return pd.DataFrame({"PARAMETER_ID": [param_id], "SIMILARITY": [0.0]})

    dist = _dtw_distance(a, b)
    norm = (len(a) + len(b)) or 1
    dist_per_step = dist / norm
    similarity = 1.0 / (1.0 + dist_per_step)

    return pd.DataFrame({"PARAMETER_ID": [param_id], "SIMILARITY": [similarity]})
```

---

## 4. 동작 요약

1. SQL에서 `DefectUtil:FastDTW` 호출
2. `TRACE_DATA`와 `GOLDEN_EQP_REF`가 pandas DataFrame으로 전달
3. 각 `PARAMETER_ID` 단위로 `FastDTW(df, df_ref)` 실행
4. 내부에서 **Z-정규화 + DTW 거리 → 유사도 변환**
5. `PARAMETER_ID, SIMILARITY` 결과 DataFrame 반환

---

## 5. 확장 아이디어

- 결과에 `EQP_ID, PRODUCT_ID, LOT_ID` 컬럼도 포함 가능
- DTW 성능 최적화를 위해 fastdtw 패키지 사용 가능
- 유사도 스케일을 0~100 점수화 등으로 변경 가능
