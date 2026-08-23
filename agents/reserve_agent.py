class StrategicReserveAgent:
    """
    Simulates the drawdown of Strategic Petroleum Reserves (SPR) 
    over a multi-day horizon when an import supply deficit occurs.
    """
    def __init__(self, initial_reserve_mb: float = 39.5, max_drawdown_mbd: float = 1.2):
        self.initial_reserve_mb = initial_reserve_mb  # Total SPR reserve capacity in Million Barrels
        self.max_drawdown_mbd = max_drawdown_mbd      # Maximum daily extraction limit in MBD

    def calculate_drawdown_schedule(self, unmet_demand_mbd: float, horizon_days: int = 14) -> list:
        """
        Generates a day-by-day drawdown projection based on current supply deficit.
        """
        schedule = []
        current_reserve = float(self.initial_reserve_mb)

        for day in range(1, horizon_days + 1):
            # Calculate daily drawdown based on deficit, daily limit, and remaining stock
            daily_drawdown = min(unmet_demand_mbd, self.max_drawdown_mbd, current_reserve)
            current_reserve = max(0.0, current_reserve - daily_drawdown)
            remaining_unmet = max(0.0, unmet_demand_mbd - daily_drawdown)

            schedule.append({
                "Day": f"Day {day}",
                "Deficit (MBD)": round(unmet_demand_mbd, 2),
                "Reserve Drawdown (MBD)": round(daily_drawdown, 2),
                "Unmet Deficit (MBD)": round(remaining_unmet, 2),
                "Remaining Reserve (MB)": round(current_reserve, 2)
            })

        return schedule