import json
import pandas as pd
import numpy as np


############################################
# Load Price Data
############################################

def load_price_data(path):
    price_map = {}

    with open(path, "r") as f:
        for line in f:
            obj = json.loads(line)

            symbol = obj["Meta Data"]["2. Symbol"]
            ts = obj["Time Series (60min)"]

            df_rows = []

            for t, values in ts.items():
                if "1. buy price" not in values or "4. sell price" not in values:
                    continue

                mid_price = (
                    float(values["1. buy price"]) +
                    float(values["4. sell price"])
                ) / 2

                df_rows.append([pd.to_datetime(t), mid_price])

            df = pd.DataFrame(df_rows, columns=["date", "price"])
            df = df.sort_values("date").set_index("date")

            price_map[symbol] = df

    return price_map


############################################
# Load Position Trajectory
############################################

def load_positions(path,
                   start_date="2025-11-05 15:00:00",
                   end_date="2025-11-07 15:00:00"):

    records = []

    with open(path, "r") as f:
        for line in f:
            obj = json.loads(line)

            date = pd.to_datetime(obj["date"])

            if pd.to_datetime(start_date) <= date <= pd.to_datetime(end_date):
                records.append(obj)

    df = pd.DataFrame(records)

    if len(df) == 0:
        raise ValueError("No data inside date range!")

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    return df


############################################
# Compute Portfolio Value
def compute_portfolio_value(position_df, price_map):

    position_df["date"] = pd.to_datetime(position_df["date"])

    portfolio_values = []

    # Sort price data
    for symbol in price_map:
        price_map[symbol] = price_map[symbol].sort_index()

    for _, row in position_df.iterrows():

        timestamp = row["date"]

        positions = row["positions"]
        cash = row["positions"]["CASH"]   # ✅ extract cash safely

        total_value = cash

        # --- Compute asset market value ---
        for symbol, qty in positions.items():

            if symbol == "CASH":
                continue

            if qty == 0:
                continue

            if symbol not in price_map:
                continue

            price_df = price_map[symbol]

            # Get last price before timestamp
            price_row = price_df.loc[price_df.index <= timestamp]

            if price_row.empty:
                continue

            price = float(price_row.iloc[-1]["price"])

            total_value += qty * price 

        portfolio_values.append(total_value)

    position_df["portfolio_value"] = portfolio_values

    return position_df


############################################
# Performance Metrics
############################################

def evaluate_strategy(portfolio_df, steps_name=""):

    values = portfolio_df["portfolio_value"].values

    returns = pd.Series(values).pct_change().dropna()

    total_return = values[-1] / values[0] - 1

    # Hourly data → assume 252*6.5 trading hours/year
    annual_factor = np.sqrt(252 * 6.5)

    sharpe = returns.mean() / (returns.std() + 1e-9) * annual_factor

    volatility = returns.std() * annual_factor

    peak = np.maximum.accumulate(values)
    drawdown = (values - peak) / peak
    max_drawdown = np.min(drawdown)

    print(f"\n===== {steps_name} Strategy =====")
    print(f"Start Portfolio Value: {values[0]:.4f}")
    print(f"End Portfolio Value: {values[-1]:.4f}")
    print(f"Total Return: {total_return:.6f}")
    print(f"Sharpe Ratio: {sharpe:.6f}")
    print(f"Volatility: {volatility:.6f}")
    print(f"Max Drawdown: {max_drawdown:.6f}")


############################################
# MAIN
############################################

if __name__ == "__main__":

    price_map = load_price_data("data/merged.jsonl")

    pos5 = load_positions("data/agent_data/gpt-5/position/position.jsonl")

    pos5 = compute_portfolio_value(pos5, price_map)

    evaluate_strategy(pos5, "5-Step")
