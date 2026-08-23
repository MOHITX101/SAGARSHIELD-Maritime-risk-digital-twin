from scipy.optimize import linprog

class AdaptiveProcurementOrchestrator:
    def optimize_procurement(self, total_demand_mbd: float, suppliers: list) -> tuple:
        c = [s["cost_per_barrel"] for s in suppliers]
        
        A_eq = [[1.0] * len(suppliers)]
        b_eq = [total_demand_mbd]
        
        bounds = [(0.0, s["capacity_mbd"]) for s in suppliers]
        
        res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        allocations = []
        total_daily_cost = 0.0
        
        if res.success:
            for idx, qty in enumerate(res.x):
                allocated_mbd = round(float(qty), 2)
                daily_cost = allocated_mbd * suppliers[idx]["cost_per_barrel"]
                total_daily_cost += daily_cost
                
                allocations.append({
                    "Supplier": suppliers[idx]["name"],
                    "Route": suppliers[idx]["route"],
                    "Allocated Volume (MBD)": allocated_mbd,
                    "Landed Cost ($/bbl)": round(suppliers[idx]["cost_per_barrel"], 2),
                    "Total Daily Spend ($M)": round(daily_cost, 2)
                })
        else:
            for s in suppliers:
                allocations.append({
                    "Supplier": s["name"],
                    "Route": s["route"],
                    "Allocated Volume (MBD)": 0.0,
                    "Landed Cost ($/bbl)": round(s["cost_per_barrel"], 2),
                    "Total Daily Spend ($M)": 0.0
                })

        return allocations, round(total_daily_cost, 2)