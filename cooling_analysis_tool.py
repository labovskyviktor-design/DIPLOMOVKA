#!/usr/bin/env python3
"""
Nástroj pre analýzu chladenia vnutorných priestorov
Cooling Analysis Tool - pre tézu o chladení vnutorných priestorov
"""

import math
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Pre serverové prostredia bez GUI
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json

# Nastavenie slovenčiny pre grafy
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

@dataclass
class CoolingSystem:
    """Definícia chladiaceho systému"""
    name: str
    type: str  # "split", "VRF", "chiller", "evaporačný", "absorpčný"
    cooling_capacity_kW: float
    electrical_power_kW: float
    cop: float
    installation_cost_eur: float
    annual_maintenance_cost_eur: float
    
    def efficiency_ratio(self) -> float:
        """Pomer účinnosti (vyšší = lepší)"""
        return self.cooling_capacity_kW / self.electrical_power_kW

@dataclass
class BuildingParameters:
    """Parametre budovy pre výpočet chladiacej potreby"""
    name: str
    floor_area_m2: float
    window_area_m2: float
    number_of_people: int
    lighting_power_W: float
    equipment_power_W: float
    u_value_walls: float  # W/(m².K)
    u_value_roof: float
    u_value_windows: float
    shading_factor: float  # 0-1
    internal_temp_C: float = 24.0
    
    def calculate_envelope_area(self) -> float:
        """Odhad plochy obálky budovy"""
        # Zjednodušený výpočet pre štvorec
        side_length = math.sqrt(self.floor_area_m2)
        wall_area = 4 * side_length * 3  # predpokladáme výšku 3m
        roof_area = self.floor_area_m2
        return wall_area + roof_area - self.window_area_m2

class CoolingAnalyzer:
    """Hlavná trieda pre analýzu chladiacich systémov"""
    
    def __init__(self):
        self.slovak_climate_data = {
            "bratislava": {
                "design_temp_C": 32,
                "avg_summer_temp_C": 26,
                "solar_radiation_W_m2": 800,
                "cooling_hours_per_day": 8,
                "cooling_days_per_year": 90,
                "relative_humidity": 0.65
            },
            "košice": {
                "design_temp_C": 31,
                "avg_summer_temp_C": 25,
                "solar_radiation_W_m2": 750,
                "cooling_hours_per_day": 7.5,
                "cooling_days_per_year": 85,
                "relative_humidity": 0.68
            },
            "žilina": {
                "design_temp_C": 29,
                "avg_summer_temp_C": 24,
                "solar_radiation_W_m2": 700,
                "cooling_hours_per_day": 6,
                "cooling_days_per_year": 70,
                "relative_humidity": 0.70
            }
        }
    
    def calculate_cooling_load(self, building: BuildingParameters, 
                             location: str = "bratislava") -> Dict[str, float]:
        """
        Komplexný výpočet chladiacej potreby budovy
        
        Returns:
            Slovník s rozložením chladiacej záťaže [W]
        """
        climate = self.slovak_climate_data.get(location, self.slovak_climate_data["bratislava"])
        
        # 1. Tepelné zisky od osôb (ASHRAE 2017)
        people_sensible_W = building.number_of_people * 70  # W/osoba
        people_latent_W = building.number_of_people * 45    # W/osoba
        people_total_W = people_sensible_W + people_latent_W
        
        # 2. Tepelné zisky od osvetlenia
        lighting_W = building.lighting_power_W * 0.95  # 95% premena na teplo
        
        # 3. Tepelné zisky od zariadení
        equipment_W = building.equipment_power_W * 0.7 * 0.8  # usage × simultaneity
        
        # 4. Solárne zisky cez okná
        solar_W = (building.window_area_m2 * 
                  climate["solar_radiation_W_m2"] * 
                  0.85 *  # SHGC typické pre dvojsklo
                  building.shading_factor)
        
        # 5. Tepelné zisky prechodom cez obálku
        temp_diff = climate["design_temp_C"] - building.internal_temp_C
        envelope_area = building.calculate_envelope_area()
        
        transmission_walls_W = (envelope_area * 0.8 *  # 80% sú steny
                               building.u_value_walls * temp_diff)
        transmission_roof_W = (envelope_area * 0.2 *   # 20% je strecha
                              building.u_value_roof * temp_diff)
        transmission_windows_W = (building.window_area_m2 * 
                                 building.u_value_windows * temp_diff)
        
        transmission_total_W = transmission_walls_W + transmission_roof_W + transmission_windows_W
        
        # 6. Ventilačné zisky (predpokladáme 30 m³/h na osobu)
        air_flow_m3_s = (building.number_of_people * 30) / 3600
        ventilation_sensible_W = 1.2 * 1010 * air_flow_m3_s * temp_diff  # ρ × cp × V × ΔT
        ventilation_latent_W = ventilation_sensible_W * 0.3  # odhad latentného zisku
        ventilation_total_W = ventilation_sensible_W + ventilation_latent_W
        
        # Celková chladiaca potreba
        total_sensible_W = (people_sensible_W + lighting_W + equipment_W + 
                           solar_W + transmission_total_W + ventilation_sensible_W)
        total_latent_W = people_latent_W + ventilation_latent_W
        total_cooling_W = total_sensible_W + total_latent_W
        
        return {
            "people_W": people_total_W,
            "lighting_W": lighting_W,
            "equipment_W": equipment_W,
            "solar_W": solar_W,
            "transmission_W": transmission_total_W,
            "ventilation_W": ventilation_total_W,
            "total_sensible_W": total_sensible_W,
            "total_latent_W": total_latent_W,
            "total_cooling_W": total_cooling_W,
            "specific_cooling_W_m2": total_cooling_W / building.floor_area_m2
        }
    
    def calculate_system_performance(self, system: CoolingSystem, 
                                   cooling_load_W: float,
                                   location: str = "bratislava") -> Dict[str, float]:
        """
        Výpočet výkonnostných parametrov chladiaceho systému
        """
        climate = self.slovak_climate_data.get(location, self.slovak_climate_data["bratislava"])
        
        # Prevádzkové hodiny za rok
        annual_hours = climate["cooling_days_per_year"] * climate["cooling_hours_per_day"]
        
        # COP závislý od vonkajšej teploty (zjednodušené)
        temp_correction = 1 - (climate["avg_summer_temp_C"] - 25) * 0.02  # -2% na °C nad 25°C
        effective_cop = system.cop * temp_correction
        
        # Elektrická spotreba
        electrical_power_W = cooling_load_W / effective_cop
        annual_energy_kWh = electrical_power_W * annual_hours / 1000
        
        # Náklady
        electricity_price_eur_kWh = 0.18  # priemer SR 2024
        annual_energy_cost_eur = annual_energy_kWh * electricity_price_eur_kWh
        total_annual_cost_eur = annual_energy_cost_eur + system.annual_maintenance_cost_eur
        
        return {
            "effective_cop": effective_cop,
            "electrical_power_W": electrical_power_W,
            "annual_energy_kWh": annual_energy_kWh,
            "annual_energy_cost_eur": annual_energy_cost_eur,
            "annual_maintenance_cost_eur": system.annual_maintenance_cost_eur,
            "total_annual_cost_eur": total_annual_cost_eur,
            "operating_hours": annual_hours
        }
    
    def economic_analysis(self, systems: List[CoolingSystem], 
                         cooling_load_W: float,
                         analysis_period_years: int = 20,
                         discount_rate: float = 0.04) -> pd.DataFrame:
        """
        Ekonomická analýza rôznych chladiacich systémov
        """
        results = []
        
        for system in systems:
            perf = self.calculate_system_performance(system, cooling_load_W)
            
            # NPV výpočet
            annual_costs = perf["total_annual_cost_eur"]
            
            # Súčasná hodnota prevádzkových nákladov
            pv_operating_costs = 0
            for year in range(1, analysis_period_years + 1):
                pv_operating_costs += annual_costs / ((1 + discount_rate) ** year)
            
            # Celkové náklady životného cyklu
            total_lcc = system.installation_cost_eur + pv_operating_costs
            
            # Payback period (zjednodušené)
            if annual_costs > 0:
                payback_years = system.installation_cost_eur / annual_costs
            else:
                payback_years = float('inf')
            
            results.append({
                'Systém': system.name,
                'Typ': system.type,
                'Chladiaci výkon [kW]': system.cooling_capacity_kW,
                'COP [-]': system.cop,
                'Investične náklady [€]': system.installation_cost_eur,
                'Ročné náklady [€/rok]': perf["total_annual_cost_eur"],
                'Ročná spotreba [kWh]': perf["annual_energy_kWh"],
                'LCC 20 rokov [€]': total_lcc,
                'Payback [roky]': min(payback_years, 99),
                'NPV [€]': -total_lcc  # záporné = náklad
            })
        
        return pd.DataFrame(results).round(2)
    
    def create_cooling_load_chart(self, cooling_loads: Dict[str, float], 
                                building_name: str = "Budova") -> None:
        """
        Vytvorenie grafu rozloženia chladiacej záťaže
        """
        # Príprava dát
        categories = ['Osoby', 'Osvetlenie', 'Zariadenia', 'Solárne zisky', 
                     'Transmisia', 'Ventilácia']
        values = [
            cooling_loads.get('people_W', 0),
            cooling_loads.get('lighting_W', 0),
            cooling_loads.get('equipment_W', 0),
            cooling_loads.get('solar_W', 0),
            cooling_loads.get('transmission_W', 0),
            cooling_loads.get('ventilation_W', 0)
        ]
        
        # Kolorová paleta
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#DDA0DD']
        
        # Vytvorenie grafu
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Stĺpcový graf
        bars = ax1.bar(categories, values, color=colors, alpha=0.8)
        ax1.set_title(f'Rozloženie chladiacej záťaže - {building_name}', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Chladiaca záťaž [W]', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        
        # Pridanie hodnôt na stĺpce
        for bar, value in zip(bars, values):
            if value > 0:
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                        f'{int(value)}W', ha='center', va='bottom', fontsize=10)
        
        # Koláčový graf
        wedges, texts, autotexts = ax2.pie(values, labels=categories, colors=colors, autopct='%1.1f%%',
                                          startangle=90, textprops={'fontsize': 10})
        ax2.set_title(f'Percentuálne rozloženie záťaže - {building_name}', fontsize=14, fontweight='bold')
        
        # Celková záťaž
        total_load = sum(values)
        fig.suptitle(f'Celková chladiaca záťaž: {total_load:.0f} W ({total_load/1000:.1f} kW)', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        plt.tight_layout()
        plt.savefig(f'chladiaca_zataz_{building_name.lower().replace(" ", "_")}.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Graf uložený ako: chladiaca_zataz_{building_name.lower().replace(' ', '_')}.png")
    
    def create_system_comparison_chart(self, comparison_df: pd.DataFrame) -> None:
        """
        Graf porovnania chladiacich systémov
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        systems = comparison_df['Systém']
        colors = plt.cm.Set3(np.linspace(0, 1, len(systems)))
        
        # 1. Investičné náklady
        bars1 = ax1.bar(systems, comparison_df['Investične náklady [€]'], color=colors, alpha=0.8)
        ax1.set_title('Investičné náklady systémov', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Investičné náklady [€]', fontsize=11)
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Ročné prevádzkové náklady
        bars2 = ax2.bar(systems, comparison_df['Ročné náklady [€/rok]'], color=colors, alpha=0.8)
        ax2.set_title('Ročné prevádzkové náklady', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Ročné náklady [€/rok]', fontsize=11)
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. COP porovnanie
        bars3 = ax3.bar(systems, comparison_df['COP [-]'], color=colors, alpha=0.8)
        ax3.set_title('Coefficient of Performance (COP)', fontsize=12, fontweight='bold')
        ax3.set_ylabel('COP [-]', fontsize=11)
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Payback period
        bars4 = ax4.bar(systems, comparison_df['Payback [roky]'], color=colors, alpha=0.8)
        ax4.set_title('Návratnosť investície', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Payback period [roky]', fontsize=11)
        ax4.tick_params(axis='x', rotation=45)
        
        # Pridanie hodnôt na grafy
        for ax, bars, values in [(ax1, bars1, comparison_df['Investične náklady [€]']),
                                (ax2, bars2, comparison_df['Ročné náklady [€/rok]']),
                                (ax3, bars3, comparison_df['COP [-]']),
                                (ax4, bars4, comparison_df['Payback [roky]'])]:
            for bar, value in zip(bars, values):
                if not pd.isna(value) and value < 90:  # Nezobrazuj extrémne hodnoty
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                           f'{value:.1f}', ha='center', va='bottom', fontsize=9)
        
        plt.suptitle('Porovnanie chladiacich systémov', fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.savefig('porovnanie_chladiacich_systemov.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Graf uložený ako: porovnanie_chladiacich_systemov.png")

def create_example_analysis():
    """
    Príklad analýzy pre administratívnu budovu
    """
    print("=== ANALÝZA CHLADENIA VNUTORNÝCH PRIESTOROV ===")
    print("Príklad: Administratívna budova v Bratislave\n")
    
    # Inicializácia analyzéra
    analyzer = CoolingAnalyzer()
    
    # Definícia budovy
    building = BuildingParameters(
        name="Administratívna budova Bratislava",
        floor_area_m2=1500,
        window_area_m2=300,
        number_of_people=60,
        lighting_power_W=15000,  # 10 W/m²
        equipment_power_W=22500,  # 15 W/m²
        u_value_walls=0.32,
        u_value_roof=0.20,
        u_value_windows=1.2,
        shading_factor=0.7  # čiastočné tienenie
    )
    
    # Výpočet chladiacej potreby
    cooling_loads = analyzer.calculate_cooling_load(building, "bratislava")
    
    print("📊 VÝSLEDKY ANALÝZY CHLADIACEJ POTREBY:")
    print(f"  Tepelné zisky od osôb: {cooling_loads['people_W']:.0f} W")
    print(f"  Tepelné zisky od osvetlenia: {cooling_loads['lighting_W']:.0f} W")
    print(f"  Tepelné zisky od zariadení: {cooling_loads['equipment_W']:.0f} W")
    print(f"  Solárne zisky: {cooling_loads['solar_W']:.0f} W")
    print(f"  Tepelné zisky prechodom: {cooling_loads['transmission_W']:.0f} W")
    print(f"  Ventilačné zisky: {cooling_loads['ventilation_W']:.0f} W")
    print(f"  ➡️ CELKOVÁ CHLADIACA POTREBA: {cooling_loads['total_cooling_W']:.0f} W ({cooling_loads['total_cooling_W']/1000:.1f} kW)")
    print(f"  ➡️ Merná potreba: {cooling_loads['specific_cooling_W_m2']:.1f} W/m²\n")
    
    # Definícia chladiacich systémov
    systems = [
        CoolingSystem("Split systém (Multi)", "split", 80, 25, 3.2, 15000, 800),
        CoolingSystem("VRF systém", "VRF", 80, 22, 3.6, 35000, 1200),
        CoolingSystem("Chiller + FCU", "chiller", 80, 20, 4.0, 45000, 2000),
        CoolingSystem("Evaporačný chladič", "evaporačný", 80, 12, 6.7, 25000, 1500),
        CoolingSystem("Absorpčný chladič", "absorpčný", 80, 15, 5.3, 60000, 2500)
    ]
    
    # Ekonomická analýza
    economic_results = analyzer.economic_analysis(systems, cooling_loads['total_cooling_W'])
    
    print("💰 EKONOMICKÁ ANALÝZA SYSTÉMOV:")
    print(economic_results.to_string(index=False))
    print()
    
    # Vytvorenie grafov
    analyzer.create_cooling_load_chart(cooling_loads, building.name)
    analyzer.create_system_comparison_chart(economic_results)
    
    # Odporúčania
    print("🎯 ODPORÚČANIA:")
    best_lcc = economic_results.loc[economic_results['LCC 20 rokov [€]'].idxmin()]
    best_cop = economic_results.loc[economic_results['COP [-]'].idxmax()]
    
    print(f"  • Najnižšie LCC: {best_lcc['Systém']} ({best_lcc['LCC 20 rokov [€]']:,.0f} €)")
    print(f"  • Najvyšší COP: {best_cop['Systém']} (COP = {best_cop['COP [-]']:.1f})")
    print(f"  • Pre administratívne budovy sa odporúčajú VRF systémy alebo chillery")
    print(f"  • Evaporačné chladenie je vhodné len v suchom klímate")
    print(f"  • Absorpčné systémy sú efektívne pri dostupnosti odpadového tepla\n")
    
    # Uloženie výsledkov do JSON
    results_summary = {
        "building": {
            "name": building.name,
            "floor_area_m2": building.floor_area_m2,
            "total_cooling_load_kW": cooling_loads['total_cooling_W'] / 1000,
            "specific_load_W_m2": cooling_loads['specific_cooling_W_m2']
        },
        "cooling_loads": cooling_loads,
        "systems_comparison": economic_results.to_dict('records')
    }
    
    with open('cooling_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results_summary, f, ensure_ascii=False, indent=2)
    
    print("💾 Výsledky uložené do: cooling_analysis_results.json")
    print("📈 Grafy vytvorené: chladiaca_zataz_*.png, porovnanie_chladiacich_systemov.png")

if __name__ == "__main__":
    create_example_analysis()