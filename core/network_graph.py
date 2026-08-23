class DynamicEnergyNetworkTwin:
    def __init__(self):
        self.nodes = {
            "Ras Tanura (Saudi)": [26.6439, 50.1581],
            "Strait of Hormuz": [26.5667, 56.2500],
            "Jamnagar Refinery (India)": [22.4707, 70.0577],
            "Cape of Good Hope": [-34.3568, 18.4740],
            "Fujairah Port": [25.1164, 56.3419]
        }
        
    def compute_dynamic_edge(self, origin: str, destination: str, corridor_risk: float, vessel_speed_knots: float) -> dict:
        distance_matrix = {
            ("Ras Tanura (Saudi)", "Jamnagar Refinery (India)"): 1250,
            ("Ras Tanura (Saudi)", "Cape of Good Hope"): 6800,
            ("Fujairah Port", "Jamnagar Refinery (India)"): 1020
        }
        
        distance_nm = distance_matrix.get((origin, destination), 1500)
        
        hours = distance_nm / vessel_speed_knots
        days = hours / 24.0
        
        base_freight_per_bbl = (distance_nm * 0.0025)
        war_risk_surcharge = (corridor_risk * 28.00)
        total_unit_cost = base_freight_per_bbl + war_risk_surcharge

        return {
            "origin": origin,
            "destination": destination,
            "distance_nm": distance_nm,
            "transit_days": round(days, 1),
            "base_freight_cost": round(base_freight_per_bbl, 2),
            "war_risk_surcharge": round(war_risk_surcharge, 2),
            "total_unit_cost": round(total_unit_cost, 2)
        }