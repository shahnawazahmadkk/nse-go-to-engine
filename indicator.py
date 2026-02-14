import yfinance as yf
import pandas as pd
import numpy as np
import json
from datetime import datetime, timezone

from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange


# ============================================================
# 1) STOCK LIST (UPDATED + FIXED TICKERS)
# ============================================================
def get_nifty50_tickers():
    return [
        # --- NIFTY 50 (your base) ---
        "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS",
        "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BHARTIARTL.NS",
        "BPCL.NS", "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS",
        "DRREDDY.NS", "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS",
        "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS",
        "INDUSINDBK.NS", "INFY.NS", "ITC.NS", "JSWSTEEL.NS",
        "LT.NS", "LTIM.NS", "M&M.NS", "MARUTI.NS", "NESTLEIND.NS",
        "NTPC.NS", "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS",
        "SHRIRAMFIN.NS", "SUNPHARMA.NS", "TATACONSUM.NS",
        "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS",
        "ULTRACEMCO.NS", "WIPRO.NS",

        # --- Extra (100+), non-finance focused ---
        "3MINDIA.NS", "ABB.NS", "ABBOTINDIA.NS", "ACC.NS", "ADANIGREEN.NS",
        "ATGL.NS", "ADVENZYMES.NS",

        # FIXED: AEGISCHEM -> AEGISLOG
        "AEGISLOG.NS",

        "AFFLE.NS", "AIAENG.NS",
        "AJANTPHARM.NS", "ALKEM.NS", "ALKYLAMINE.NS", "ALLCARGO.NS",
        "ALOKINDS.NS", "AMBER.NS", "AMBUJACEM.NS", "ANGELONE.NS",
        "ANUPAMRAS.NS", "APLAPOLLO.NS", "APOLLOTYRE.NS", "APTUS.NS",
        "ASAHIINDIA.NS", "ASHOKLEY.NS", "ASTERDM.NS", "ASTRAL.NS",
        "ATUL.NS", "AUROPHARMA.NS", "AVANTIFEED.NS", "BALKRISIND.NS",
        "BALRAMCHIN.NS", "BASF.NS", "BATAINDIA.NS", "BAYERCROP.NS",
        "BDL.NS", "BEL.NS", "BERGEPAINT.NS", "BHARATFORG.NS",
        "BHEL.NS", "BIOCON.NS", "BIRLACORPN.NS", "BLUEDART.NS",
        "BLUESTARCO.NS", "BORORENEW.NS", "BOSCHLTD.NS", "BRIGADE.NS",
        "BSE.NS", "BSOFT.NS", "CAPLIPOINT.NS", "CARBORUNIV.NS",
        "CASTROLIND.NS", "CCL.NS", "CDSL.NS", "CEATLTD.NS",
        "CENTURYPLY.NS", "CENTURYTEX.NS", "CESC.NS", "CGPOWER.NS",
        "CHALET.NS", "CHAMBLFERT.NS", "CHEMPLASTS.NS", "CHOLAFIN.NS",
        "CLEAN.NS", "COCHINSHIP.NS", "COFORGE.NS", "COLPAL.NS",
        "CONCOR.NS", "COROMANDEL.NS", "CRISIL.NS", "CROMPTON.NS",
        "CUMMINSIND.NS", "CYIENT.NS", "DABUR.NS", "DALBHARAT.NS",
        "DCMSHRIRAM.NS", "DEEPAKNTR.NS", "DEVYANI.NS", "DIXON.NS",
        "DLF.NS", "DMART.NS", "EASEMYTRIP.NS", "ECLERX.NS",

        # FIXED: EMAMI -> EMAMILTD
        "EMAMILTD.NS",

        "ENDURANCE.NS", "ERIS.NS",
        "ESCORTS.NS", "EXIDEIND.NS", "FDC.NS", "FINCABLES.NS",
        "FINEORG.NS", "FINPIPE.NS", "FORTIS.NS", "FSL.NS",
        "GAIL.NS", "GALAXYSURF.NS", "GARFIBRES.NS", "GESHIP.NS",
        "GLAND.NS", "GLAXO.NS", "GLENMARK.NS", "GMMPFAUDLR.NS",
        "GMRINFRA.NS", "GODREJAGRO.NS", "GODREJCP.NS", "GODREJIND.NS",
        "GODREJPROP.NS", "GRANULES.NS", "GRAPHITE.NS", "GRINDWELL.NS",
        "GRINFRA.NS", "GUJGASLTD.NS", "HAPPSTMNDS.NS", "HAVELLS.NS",
        "HFCL.NS", "HINDCOPPER.NS", "HINDZINC.NS", "HOMEFIRST.NS",
        "HONAUT.NS", "HUDCO.NS", "IEX.NS", "IFBIND.NS",
        "IGL.NS", "INDHOTEL.NS", "INDIAMART.NS", "INDIGO.NS",
        "INDIGOPNTS.NS", "INDUSTOWER.NS", "INFIBEAM.NS", "IOC.NS",
        "IPCALAB.NS", "IRB.NS", "IRCON.NS", "IRCTC.NS",
        "IRFC.NS", "JINDALSTEL.NS", "JKCEMENT.NS", "JKLAKSHMI.NS",
        "JKPAPER.NS", "JSL.NS", "JSWENERGY.NS", "JUBLFOOD.NS",
        "JYOTHYLAB.NS", "KAJARIACER.NS", "KALYANKJIL.NS", "KANSAINER.NS",
        "KEC.NS", "KEI.NS", "KIMS.NS", "KNRCON.NS",
        "KPITTECH.NS", "KPRMILL.NS", "KRBL.NS", "LAURUSLABS.NS",
        "LAXMIMACH.NS", "LINDEINDIA.NS", "LODHA.NS", "LTTS.NS",
        "LUPIN.NS", "LUXIND.NS", "LXCHEM.NS", "MARICO.NS",
        "MAXHEALTH.NS", "MAZDOCK.NS", "METROBRAND.NS", "MPHASIS.NS",
        "MRF.NS", "NATCOPHARM.NS", "NATIONALUM.NS", "NAVINFLUOR.NS",
        "NAZARA.NS", "NBCC.NS", "NCC.NS", "NETWORK18.NS",
        "NHPC.NS", "NLCINDIA.NS", "NMDC.NS", "NOCIL.NS",
        "NYKAA.NS", "OBEROIRLTY.NS", "OIL.NS", "ORIENTELEC.NS",
        "PAGEIND.NS", "PCBL.NS", "PERSISTENT.NS", "PETRONET.NS",
        "PFIZER.NS", "PIDILITIND.NS", "PIIND.NS", "POLYCAB.NS",
        "POLYMED.NS", "POLYPLEX.NS", "PRAJIND.NS", "PRESTIGE.NS",
        "PRINCEPIPE.NS",

        # FIXED: PRISM -> PRISMJOHNSN
        "PRISMJOHNSN.NS",

        "PVRINOX.NS", "RADICO.NS",
        "RAILTEL.NS", "RAIN.NS", "RAJESHEXPO.NS", "RALLIS.NS",
        "RAMCOCEM.NS", "RATNAMANI.NS", "REDINGTON.NS", "RELAXO.NS",
        "RITES.NS", "ROSSARI.NS", "ROUTE.NS", "RVNL.NS",
        "SAIL.NS", "SANOFI.NS", "SAPPHIRE.NS", "SAREGAMA.NS",
        "SHREECEM.NS", "SHYAMMETL.NS", "SIEMENS.NS", "SOBHA.NS",
        "SOLARINDS.NS", "SONACOMS.NS", "SONATSOFTW.NS", "SPICEJET.NS",
        "SRF.NS", "STARHEALTH.NS", "STLTECH.NS", "SUDARSCHEM.NS",
        "SUMICHEM.NS", "SUNTV.NS", "SUPREMEIND.NS", "SUZLON.NS",
        "SYMPHONY.NS", "SYNGENE.NS", "TANLA.NS", "TATACHEM.NS",
        "TATACOMM.NS", "TATAELXSI.NS", "TATAMOTORS.NS", "TATAPOWER.NS",
        "TCIEXP.NS", "TEAMLEASE.NS", "THERMAX.NS", "TIINDIA.NS",
        "TIMKEN.NS", "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS",
        "TRIDENT.NS", "TRITURBINE.NS", "TTKPRESTIG.NS", "TV18BRDCST.NS",
        "TVSMOTOR.NS", "UFLEX.NS", "UPL.NS", "UTIAMC.NS",
        "VAKRANGEE.NS", "VBL.NS", "VEDL.NS", "VGUARD.NS",

        # FIXED: VIJAYADIAG -> VIJAYA
        "VIJAYA.NS",

        "VINATIORGA.NS", "VIPIND.NS", "VOLTAS.NS",
        "WHIRLPOOL.NS", "WOCKPHARMA.NS", "ZEEL.NS", "ZOMATO.NS",
        "ZYDUSLIFE.NS", "ZYDUSWELL.NS"
    ]


# ============================================================
# 2) Download + Fixes (SAFE, NO SPAM)
# ============================================================
def download_daily(ticker: str, years=5):
    period = f"{years}y"
    try:
        df = yf.download(
            ticker,
            period=period,
            interval="1d",
            progress=False,
            auto_adjust=False,
            threads=False
        )
    except Exception:
        return None

    if df is None or len(df) == 0:
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.dropna()
    if len(df) == 0:
        return None

    return df


def ensure_1d_series(x):
    if isinstance(x, pd.DataFrame):
        x = x.iloc[:, 0]
    if isinstance(x, np.ndarray):
        x = x.reshape(-1)
        x = pd.Series(x)
    return x


def to_weekly(df_daily: pd.DataFrame) -> pd.DataFrame:
    w = pd.DataFrame()
    w["Open"] = df_daily["Open"].resample("W-FRI").first()
    w["High"] = df_daily["High"].resample("W-FRI").max()
    w["Low"] = df_daily["Low"].resample("W-FRI").min()
    w["Close"] = df_daily["Close"].resample("W-FRI").last()
    w["Volume"] = df_daily["Volume"].resample("W-FRI").sum()
    w = w.dropna()
    return w


# ============================================================
# 3) Indicators
# ============================================================
def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    close = ensure_1d_series(df[["Close"]])
    high = ensure_1d_series(df[["High"]])
    low = ensure_1d_series(df[["Low"]])
    volume = ensure_1d_series(df[["Volume"]])

    df["ema10"] = EMAIndicator(close, window=10).ema_indicator()
    df["ema20"] = EMAIndicator(close, window=20).ema_indicator()
    df["ema50"] = EMAIndicator(close, window=50).ema_indicator()
    df["ema200"] = EMAIndicator(close, window=200).ema_indicator()

    df["rsi14"] = RSIIndicator(close, window=14).rsi()

    macd = MACD(close, window_slow=26, window_fast=12, window_sign=9)
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_hist"] = macd.macd_diff()

    atr = AverageTrueRange(high, low, close, window=14)
    df["atr14"] = atr.average_true_range()
    df["atr_pct"] = (df["atr14"] / df["Close"]) * 100

    adx = ADXIndicator(high, low, close, window=14)
    df["adx14"] = adx.adx()

    df["vol_sma20"] = df["Volume"].rolling(20).mean()
    df["vol_ratio"] = df["Volume"] / df["vol_sma20"]

    df["high20"] = df["High"].rolling(20).max()

    return df


# ============================================================
# 4) Market regime (BULL / SIDEWAYS)
# ============================================================
def get_market_regime(nifty_df_daily: pd.DataFrame) -> str:
    d = nifty_df_daily.copy()
    d = add_indicators(d)
    d = d.dropna()

    if len(d) < 250:
        return "SIDEWAYS"

    last = d.iloc[-1]
    bull = (last["Close"] > last["ema50"]) and (last["ema20"] > last["ema50"])
    return "BULL" if bull else "SIDEWAYS"


# ============================================================
# 5) Entry Types
# ============================================================
def detect_breakout(row):
    return row["Close"] >= 0.995 * row["high20"] and row["vol_ratio"] >= 1.2


def detect_pullback(row):
    price = row["Close"]
    ema20 = row["ema20"]
    ema50 = row["ema50"]

    if price > ema50 and ema20 > ema50:
        if abs((price - ema20) / ema20) <= 0.012:
            return True
    return False


def detect_rsi_bounce_setup(row):
    """
    Sideways market short-term setup:
    - RSI low-ish
    - price near EMA20/EMA50
    """
    rsi = row["rsi14"]
    price = row["Close"]
    ema20 = row["ema20"]
    ema50 = row["ema50"]

    if np.isnan(rsi) or np.isnan(ema20) or np.isnan(ema50):
        return False

    near_ema20 = abs((price - ema20) / ema20) <= 0.02
    near_ema50 = abs((price - ema50) / ema50) <= 0.025

    if (35 <= rsi <= 48) and (near_ema20 or near_ema50):
        return True

    return False


# ============================================================
# 6) Holding buckets
# ============================================================
def holding_bucket_3(last_daily, last_weekly):
    """
    Returns:
    - SHORT_TERM (<7 days)
    - SWING (7–30 days)
    - POSITIONAL (>30 days)
    """

    price = last_daily["Close"]

    ema10 = last_daily["ema10"]
    ema20 = last_daily["ema20"]
    ema50 = last_daily["ema50"]
    ema200 = last_daily["ema200"]

    weekly_close = last_weekly["Close"]
    weekly_ema50 = last_weekly["ema50"]

    # POSITIONAL
    if (
        weekly_close > weekly_ema50
        and price > ema200
        and ema50 > ema200
    ):
        return "POSITIONAL (>30 days)"

    # SWING
    if price > ema50 and ema20 > ema50:
        return "SWING (7–30 days)"

    # SHORT TERM
    if price > ema20 and ema10 > ema20:
        return "SHORT_TERM (<7 days)"

    return "AVOID"


# ============================================================
# 7) Score Model (SIDEWAYS MODE ADDED)
# ============================================================
def score_for_bucket(row, bucket, market_regime="BULL"):
    score = 0

    price = row["Close"]
    ema10 = row["ema10"]
    ema20 = row["ema20"]
    ema50 = row["ema50"]
    ema200 = row["ema200"]

    rsi = row["rsi14"]
    macd = row["macd"]
    macd_signal = row["macd_signal"]
    macd_hist = row["macd_hist"]

    adx = row["adx14"]
    vol_ratio = row["vol_ratio"]
    atr_pct = row["atr_pct"]

    breakout = detect_breakout(row)
    pullback = detect_pullback(row)
    bounce = detect_rsi_bounce_setup(row)

    # Market regime
    score += 8 if market_regime == "BULL" else 2

    # ATR penalty
    if atr_pct >= 6:
        score -= 12
    elif atr_pct >= 4:
        score -= 6

    # MACD
    if macd > macd_signal:
        score += 10
    else:
        score -= 3 if market_regime == "SIDEWAYS" else 7

    # ADX
    if market_regime == "BULL":
        if adx >= 20:
            score += 8
        elif adx < 15:
            score -= 6
    else:
        if adx <= 18:
            score += 6
        elif adx > 25:
            score -= 5

    # ====================================================
    # Bucket logic
    # ====================================================
    if bucket == "SHORT_TERM (<7 days)":

        if market_regime == "BULL":
            if price > ema20:
                score += 12
            if ema10 > ema20:
                score += 12

            if 40 <= rsi <= 72:
                score += 8
            elif rsi > 72:
                score -= 6
            else:
                score -= 6

            if breakout:
                score += 10
            if pullback:
                score += 6

        else:
            # SIDEWAYS: mean reversion
            if bounce:
                score += 22

            if 32 <= rsi <= 50:
                score += 12
            elif rsi > 65:
                score -= 10

            if abs((price - ema20) / ema20) <= 0.03:
                score += 8

            if macd_hist > -0.2:
                score += 6

        # volume bonus
        if vol_ratio >= 1.5:
            score += 8
        elif vol_ratio >= 1.1:
            score += 4

    elif bucket == "SWING (7–30 days)":

        if market_regime == "BULL":
            if price > ema50:
                score += 15
            if ema20 > ema50:
                score += 12

            if 45 <= rsi <= 72:
                score += 10
            elif rsi > 72:
                score -= 6
            else:
                score -= 8

            if breakout:
                score += 10
            if pullback:
                score += 10

        else:
            # SIDEWAYS: early reversal
            if price > ema20:
                score += 15
            if ema10 > ema20:
                score += 8
            if price > ema50:
                score += 6

            if 40 <= rsi <= 60:
                score += 12
            elif rsi > 70:
                score -= 8
            elif rsi < 35:
                score -= 8

            if bounce:
                score += 10

        if vol_ratio >= 1.3:
            score += 6

    elif bucket == "POSITIONAL (>30 days)":
        # Always trend based
        if price > ema200:
            score += 18
        if ema50 > ema200:
            score += 15
        if ema20 > ema50:
            score += 10

        if 45 <= rsi <= 70:
            score += 8
        elif rsi < 40:
            score -= 10
        elif rsi > 75:
            score -= 6

        if adx >= 20:
            score += 8

        if pullback:
            score += 8

    score = max(0, min(100, score))
    return score


def decision_from_score(score):
    if score >= 75:
        return "BUY"
    if score >= 60:
        return "WATCH"
    return "AVOID"


# ============================================================
# 8) Risk / Targets (SIDEWAYS MODE TIGHTER)
# ============================================================
def risk_targets(price, atr, bucket, market_regime="BULL"):
    if atr is None or np.isnan(atr) or atr == 0:
        return None, None, None

    # tighter stop in sideways
    stop_mult = 1.5 if market_regime == "SIDEWAYS" else 2.0
    stoploss = price - stop_mult * atr

    # reward multipliers
    if market_regime == "SIDEWAYS":
        if bucket == "SHORT_TERM (<7 days)":
            mult = 1.6
        elif bucket == "SWING (7–30 days)":
            mult = 2.4
        else:
            mult = 4.5
    else:
        if bucket == "SHORT_TERM (<7 days)":
            mult = 2.0
        elif bucket == "SWING (7–30 days)":
            mult = 3.5
        else:
            mult = 6.0

    target = price + mult * atr
    rr = (target - price) / (price - stoploss) if (price - stoploss) != 0 else None
    return stoploss, target, rr


# ============================================================
# 9) Analyze one stock
# ============================================================
def analyze_stock(ticker, market_regime="BULL"):
    df = download_daily(ticker, years=5)
    if df is None or len(df) < 260:
        return None

    df = add_indicators(df)

    w = to_weekly(df)
    w = add_indicators(w)

    df_valid = df.dropna()
    w_valid = w.dropna()

    if len(df_valid) == 0 or len(w_valid) == 0:
        return None

    last = df_valid.iloc[-1].copy()
    wlast = w_valid.iloc[-1].copy()

    bucket = holding_bucket_3(last, wlast)
    if bucket == "AVOID":
        return None

    score = score_for_bucket(last, bucket, market_regime=market_regime)
    decision = decision_from_score(score)

    sl, tgt, rr = risk_targets(last["Close"], last["atr14"], bucket, market_regime=market_regime)

    return {
        "Ticker": ticker,
        "Price": round(float(last["Close"]), 2),
        "Bucket": bucket,
        "Decision": decision,
        "Score": int(score),
        "Stoploss": round(float(sl), 2) if sl else None,
        "Target": round(float(tgt), 2) if tgt else None,
        "RR": round(float(rr), 2) if rr else None,
        "RSI": round(float(last["rsi14"]), 2),
        "ADX": round(float(last["adx14"]), 2),
        "VolRatio": round(float(last["vol_ratio"]), 2) if not np.isnan(last["vol_ratio"]) else None,
    }


# ============================================================
# 10) Run full scan + split into 3 lists of 20
# ============================================================
def run_engine():
    tickers = get_nifty50_tickers()

    nifty = download_daily("^NSEI", years=5)
    market_regime = get_market_regime(nifty)

    print(f"\nMarket regime detected: {market_regime}\n")

    results = []
    for t in tickers:
        try:
            r = analyze_stock(t, market_regime=market_regime)
            if r:
                results.append(r)
        except Exception:
            pass

    df = pd.DataFrame(results)
    if len(df) == 0:
        return df, None, None, None, market_regime

    df = df.sort_values(by="Score", ascending=False)

    df_good = df[df["Decision"].isin(["BUY", "WATCH"])].copy()

    short_df = df_good[df_good["Bucket"] == "SHORT_TERM (<7 days)"].head(20).reset_index(drop=True)
    swing_df = df_good[df_good["Bucket"] == "SWING (7–30 days)"].head(20).reset_index(drop=True)
    pos_df = df_good[df_good["Bucket"] == "POSITIONAL (>30 days)"].head(20).reset_index(drop=True)

    # Save into docs/ for GitHub Pages
    df.to_csv("docs/nse_all_signals.csv", index=False)
    short_df.to_csv("docs/nse_short_term_20.csv", index=False)
    swing_df.to_csv("docs/nse_swing_20.csv", index=False)
    pos_df.to_csv("docs/nse_positional_20.csv", index=False)

    payload = {
        "updated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "market_regime": market_regime,
        "short_term": short_df.to_dict(orient="records"),
        "swing": swing_df.to_dict(orient="records"),
        "positional": pos_df.to_dict(orient="records"),
    }

    with open("docs/signals.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    return df, short_df, swing_df, pos_df, market_regime


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    all_df, short_df, swing_df, pos_df, market_regime = run_engine()

    print("\n===============================")
    print(" NSE GO-TO ENGINE (3 BUCKETS) ")
    print("===============================\n")

    if all_df is None or len(all_df) == 0:
        print("No signals found today.")
    else:
        print("\n--- TOP 20 SHORT TERM (<7 days) ---\n")
        print(short_df.to_string(index=False))

        print("\n--- TOP 20 SWING (7–30 days) ---\n")
        print(swing_df.to_string(index=False))

        print("\n--- TOP 20 POSITIONAL (>30 days) ---\n")
        print(pos_df.to_string(index=False))

        print("\nSaved files into docs/:")
        print(" - docs/signals.json")
        print(" - docs/nse_all_signals.csv")
        print(" - docs/nse_short_term_20.csv")
        print(" - docs/nse_swing_20.csv")
        print(" - docs/nse_positional_20.csv")
