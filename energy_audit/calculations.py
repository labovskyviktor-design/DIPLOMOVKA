"""
Tepelno-technické výpočty podľa STN noriem
Implementované podľa skrípt Krajčík, Petráš, Skalíková
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from .models import (
    Building, Zone, Construction, Window, ConstructionType,
    ClimateData, HeatingSystemType
)


@dataclass
class ThermalAssessmentResult:
    """Výsledok tepelno-technického posúdenia"""
    construction_name: str
    u_value_calculated: float  # vypočítaná hodnota U [W/(m².K)]
    u_value_required: float  # požadovaná hodnota U [W/(m².K)]
    compliant: bool  # vyhovuje/nevyhovuje
    assessment_type: str  # typ posúdenia (U_r1, U_r2, atď.)


class ThermalCalculations:
    """Trieda pre tepelno-technické výpočty"""
    
    @staticmethod
    def calculate_surface_resistances(construction_type: ConstructionType, 
                                    heat_flow_direction: str = "horizontal") -> Tuple[float, float]:
        """
        Výpočet tepelných odporov na povrchoch podľa STN EN ISO 6946
        
        Args:
            construction_type: typ konštrukcie
            heat_flow_direction: smer tepelného toku (horizontal, upward, downward)
            
        Returns:
            (Rsi, Rse): vnútorný a vonkajší tepelný odpor [(m².K)/W]
        """
        # Vonkajší tepelný odpor
        rse = 0.04  # štandardný pre všetky konštrukcie
        
        # Vnútorný tepelný odpor podľa smeru tepelného toku
        if heat_flow_direction == "horizontal":
            rsi = 0.13
        elif heat_flow_direction == "upward":  # tepelný tok smerom nahor
            rsi = 0.10
        elif heat_flow_direction == "downward":  # tepelný tok smerom nadol
            rsi = 0.17
        else:
            rsi = 0.13  # default horizontal
            
        return rsi, rse
    
    @staticmethod
    def assess_construction_compliance(construction: Construction, 
                                     assessment_level: str = "U_r1") -> ThermalAssessmentResult:
        """
        Posúdenie konštrukcie podľa STN 73 0540-2/Z1
        
        Args:
            construction: konštrukcia na posúdenie
            assessment_level: úroveň posúdenia (U_max, U_N, U_r1, U_r2)
            
        Returns:
            výsledok posúdenia
        """
        u_calculated = construction.u_value()
        
        # Určenie typu konštrukcie pre požiadavky
        construction_key = ""
        if construction.construction_type == ConstructionType.EXTERNAL_WALL:
            construction_key = "vonkajšia_stena"
        elif construction.construction_type == ConstructionType.ROOF:
            construction_key = "strecha"
        elif construction.construction_type in [ConstructionType.FLOOR_ON_GROUND, 
                                               ConstructionType.FLOOR_ABOVE_UNHEATED]:
            construction_key = "podlaha"
        elif construction.construction_type in [ConstructionType.WINDOW, ConstructionType.DOOR]:
            construction_key = "okná"
        
        if construction_key not in STN_REQUIREMENTS:
            raise ValueError(f"Neznámy typ konštrukcie: {construction.construction_type}")
        
        u_required = STN_REQUIREMENTS[construction_key][assessment_level]
        compliant = u_calculated <= u_required
        
        return ThermalAssessmentResult(
            construction_name=construction.name,
            u_value_calculated=u_calculated,
            u_value_required=u_required,
            compliant=compliant,
            assessment_type=assessment_level
        )
    
    @staticmethod
    def calculate_thermal_bridges_effect(thermal_bridges: List, 
                                       total_envelope_area: float,
                                       delta_u_method: str = "detailed") -> float:
        """
        Výpočet vplyvu tepelných mostov
        
        Args:
            thermal_bridges: zoznam tepelných mostov
            total_envelope_area: celková plocha obálky budovy [m²]
            delta_u_method: metóda výpočtu (detailed, simplified)
            
        Returns:
            ΔU: zvýšenie súčiniteľa prechodu tepla [W/(m².K)]
        """
        if delta_u_method == "detailed":
            # Detailný výpočet podľa STN EN ISO 13789
            psi_total = sum(tb.psi_value * tb.length for tb in thermal_bridges)
            return psi_total / total_envelope_area if total_envelope_area > 0 else 0.0
        else:
            # Zjednodušený výpočet podľa STN 73 0540-2
            # Hodnoty podľa prílohy F normy
            return 0.1  # pre jednovrstvové murované konštrukcie
    
    @staticmethod
    def calculate_air_change_rate(building: Building, 
                                windows_tightness: Dict[str, float]) -> float:
        """
        Výpočet intenzity výmeny vzduchu infiltráciou
        
        Args:
            building: budova
            windows_tightness: súčinitele škárovej prievzdušnosti okien
            
        Returns:
            intenzita výmeny vzduchu [1/h]
        """
        total_window_length = 0.0
        weighted_tightness = 0.0
        
        for zone in building.zones:
            for window in zone.windows:
                # Predpokladaná dĺžka škár okna (obvod)
                window_length = 2 * math.sqrt(window.area * 4)  # aproximácia pre štvorec
                
                # Získanie súčiniteľa prievzdušnosti
                tightness = windows_tightness.get(window.name, 1.4e-4)  # default pre drevené okná
                
                total_window_length += window_length
                weighted_tightness += tightness * window_length
        
        if total_window_length == 0:
            return 0.5  # minimálna výmena vzduchu
        
        avg_tightness = weighted_tightness / total_window_length
        building_volume = building.total_volume()
        
        # Výpočet podľa vzorca (2.5) zo skrípt
        if building_volume > 0:
            n_inf = 25 * 200 * (avg_tightness * total_window_length) / building_volume
            return max(n_inf, 0.5)  # minimálne 0.5 h⁻¹
        
        return 0.5


class HeatingCalculations:
    """Výpočty potreby tepla na vykurovanie"""
    
    @staticmethod
    def calculate_transmission_heat_loss_coefficient(building: Building,
                                                   thermal_bridges_delta_u: float = 0.1) -> float:
        """
        Merná tepelná strata prechodom tepla HT [W/K]
        Podľa rovnice (2.3) zo skrípt
        """
        ht_total = 0.0
        
        for zone in building.zones:
            # Tepelné straty cez konštrukcie
            for construction in zone.constructions:
                # Redukčný faktor bx (pre vonkajšie konštrukcie = 1.0)
                bx = 1.0 if construction.construction_type in [
                    ConstructionType.EXTERNAL_WALL, ConstructionType.ROOF
                ] else 0.5  # pre konštrukcie do nevykurovaných priestorov
                
                ht_total += bx * construction.u_value() * construction.area
            
            # Tepelné straty cez okná
            for window in zone.windows:
                ht_total += window.u_value * window.area
        
        # Vplyv tepelných mostov
        total_envelope_area = building.envelope_area()
        ht_total += thermal_bridges_delta_u * total_envelope_area
        
        return ht_total
    
    @staticmethod
    def calculate_ventilation_heat_loss_coefficient(building: Building,
                                                  air_change_rate: float) -> float:
        """
        Merná tepelná strata vetraním HV [W/K]
        Podľa rovnice (2.4) zo skrípt
        """
        # Fyzikálne vlastnosti vzduchu
        rho_air = 1.2  # kg/m³
        c_air = 1010   # J/(kg.K)
        
        # Pomer vnútorného a obostavaného objemu
        volume_ratio = 0.85  # pre obnovovné budovy v pôvodnom stave
        
        building_volume = building.total_volume()
        
        hv = (volume_ratio * rho_air * c_air * air_change_rate * building_volume) / 3600
        
        return hv
    
    @staticmethod
    def calculate_total_heat_loss(building: Building,
                                climate_data: ClimateData,
                                air_change_rate: float) -> float:
        """
        Celková tepelná strata Qht [kWh]
        Podľa rovnice (2.2) zo skrípt
        """
        ht = HeatingCalculations.calculate_transmission_heat_loss_coefficient(building)
        hv = HeatingCalculations.calculate_ventilation_heat_loss_coefficient(building, air_change_rate)
        
        # Priemerná vnútorná teplota (predpokladáme 20°C)
        theta_int = 20.0
        theta_e = climate_data.external_temperature
        heating_days = climate_data.heating_days
        
        # Celková tepelná strata
        qht = (ht + hv) * (theta_int - theta_e) * heating_days * 0.024
        
        return qht
    
    @staticmethod
    def calculate_internal_heat_gains(building: Building,
                                    climate_data: ClimateData) -> float:
        """
        Vnútorné tepelné zisky Qint [kWh]
        Podľa rovnice (2.7) zo skrípt
        """
        # Špecifický tepelný výkon vnútorných zdrojov
        if building.category.value == "bytový_dom":
            qi = 5.0  # W/m²
        elif building.category.value == "rodinný_dom":
            qi = 4.0  # W/m²
        else:
            qi = 6.0  # W/m² pre nebytové budovy
        
        floor_area = building.total_floor_area()
        heating_days = climate_data.heating_days
        
        qint = qi * 0.024 * heating_days * floor_area
        
        return qint
    
    @staticmethod
    def calculate_solar_heat_gains(building: Building,
                                 climate_data: ClimateData) -> float:
        """
        Solárne tepelné zisky Qsol [kWh]
        Podľa rovníc (2.8) a (2.9) zo skrípt
        """
        qsol_total = 0.0
        
        for zone in building.zones:
            for window in zone.windows:
                # Orientácia okna
                orientation = window.orientation.upper()
                if orientation not in climate_data.solar_radiation:
                    orientation = 'J'  # default na juh
                
                # Intenzita slnečného žiarenia
                i_sol = climate_data.solar_radiation[orientation]
                
                # Účinná kolekčná plocha (rovnica 2.9)
                # Predpokladáme FF = 0.2 (podiel rámov), teda (1-FF) = 0.8
                a_sol = window.shading_factor * window.g_value * 0.8 * window.area
                
                # Tieniaci faktor pre vonkajšie prekážky
                f_sh_ob = 0.8  # štandardná hodnota
                
                # Solárne zisky z okna
                qsol_window = f_sh_ob * a_sol * i_sol
                qsol_total += qsol_window
        
        return qsol_total
    
    @staticmethod
    def calculate_utilization_factor(building: Building) -> float:
        """
        Faktor využitia tepelných ziskov ηgn [-]
        Podľa Tab. 2.6 zo skrípt
        """
        if building.category.value == "bytový_dom":
            return 0.95  # pre nízkoenergetické budovy
        else:
            return 0.95  # pre rodinné domy
    
    @staticmethod
    def calculate_heating_demand(building: Building,
                               climate_data: ClimateData,
                               air_change_rate: float) -> Dict[str, float]:
        """
        Celkový výpočet potreby tepla na vykurovanie
        Podľa rovnice (2.1) zo skrípt
        
        Returns:
            slovník s výsledkami výpočtu
        """
        # Tepelné straty
        qht = HeatingCalculations.calculate_total_heat_loss(
            building, climate_data, air_change_rate
        )
        
        # Tepelné zisky
        qint = HeatingCalculations.calculate_internal_heat_gains(building, climate_data)
        qsol = HeatingCalculations.calculate_solar_heat_gains(building, climate_data)
        qgn = qint + qsol
        
        # Faktor využitia tepelných ziskov
        eta_gn = HeatingCalculations.calculate_utilization_factor(building)
        
        # Potreba tepla na vykurovanie
        qh = qht - eta_gn * qgn
        qh = max(0, qh)  # nemôže byť záporná
        
        # Merná potreba tepla
        floor_area = building.total_floor_area()
        qh_specific = qh / floor_area if floor_area > 0 else 0
        
        return {
            'total_heat_loss': qht,
            'internal_gains': qint,
            'solar_gains': qsol,
            'total_gains': qgn,
            'utilization_factor': eta_gn,
            'heating_demand': qh,
            'specific_heating_demand': qh_specific,
            'air_change_rate': air_change_rate
        }


class EnergyCalculations:
    """Výpočty potreby energie na vykurovanie a prípravu TV"""
    
    @staticmethod
    def calculate_emission_losses(building: Building, heating_demand: float) -> float:
        """
        Tepelná strata systému odovzdávania tepla [kWh]
        Zjednodušený výpočet podľa kapitoly 3.1.1 zo skrípt
        """
        # Zjednodušené pre príklad - závislé od typu systému
        if building.heating_system:
            if building.heating_system.system_type.value == "radiátorový":
                # Pre radiátory s P-regulátorom
                delta_theta = 1.2  # zvýšenie teploty [K]
            else:
                delta_theta = 0.5  # pre podlahové systémy
        else:
            delta_theta = 1.2  # default
        
        theta_int_inc = 20.0 + delta_theta
        theta_e_comb = building.climate_data.external_temperature
        
        # Podľa rovnice (3.1)
        qem_ls = heating_demand * (delta_theta / (theta_int_inc - theta_e_comb))
        
        return qem_ls
    
    @staticmethod
    def calculate_distribution_losses(building: Building) -> float:
        """
        Tepelné straty z rozvodov vykurovacieho systému [kWh]
        Zjednodušený výpočet
        """
        # Odhad na základe objemu budovy a typu rozvodov
        volume = building.total_volume()
        
        # Odhad dĺžky rozvodov (m)
        estimated_pipe_length = volume * 0.1  # približne 0.1 m potrubia na m³
        
        # Predpokladané straty (kWh/m za rok)
        specific_losses = 15.0  # pre neizolované stúpacie potrubia
        
        distribution_losses = estimated_pipe_length * specific_losses
        
        return distribution_losses
    
    @staticmethod
    def calculate_auxiliary_energy(building: Building) -> float:
        """
        Vlastná spotreba energie obehových čerpadiel [kWh]
        Zjednodušený výpočet
        """
        floor_area = building.total_floor_area()
        
        # Odhad príkonu čerpadla na základe plochy
        if floor_area < 500:
            pump_power = 100  # W
        elif floor_area < 2000:
            pump_power = 200  # W
        else:
            pump_power = 300  # W
        
        # Prevádzkové hodiny (predpokladáme cez celú vykurovaciu sezónu)
        operating_hours = building.climate_data.heating_days * 24
        
        auxiliary_energy = (pump_power * operating_hours) / 1000  # kWh
        
        return auxiliary_energy
    
    @staticmethod
    def calculate_hot_water_demand(building: Building) -> Dict[str, float]:
        """
        Potreba energie na prípravu teplej vody [kWh]
        Podľa kapitoly 4 zo skrípt
        """
        floor_area = building.total_floor_area()
        
        # Špecifická potreba tepla na TV podľa typu budovy
        if building.category.value == "bytový_dom":
            qw_specific = 20.0  # kWh/(m².rok)
        else:
            qw_specific = 15.0  # kWh/(m².rok)
        
        # Potreba tepla na ohrev TV
        qw = qw_specific * floor_area
        
        # Tepelné straty z distribúcie TV (odhad 50% z potreby tepla)
        qw_distribution_losses = 0.5 * qw
        
        # Celková potreba energie na TV
        qtv = qw + qw_distribution_losses
        
        return {
            'hot_water_heat_demand': qw,
            'distribution_losses': qw_distribution_losses,
            'total_hot_water_energy': qtv,
            'specific_hot_water_energy': qtv / floor_area if floor_area > 0 else 0
        }


class HydraulicCalculations:
    """Výpočty hydraulického vyregulovania vykurovacích systémov"""
    
    @staticmethod
    def calculate_required_flow_rate(heating_demand: float, 
                                   supply_temp: float = 90.0, 
                                   return_temp: float = 70.0) -> float:
        """
        Výpočet požadovaného prietoku vykurovacej vody [kg/s]
        
        Args:
            heating_demand: tepelný výkon [W]
            supply_temp: teplota prívodnej vody [°C]
            return_temp: teplota vratnej vody [°C]
            
        Returns:
            požadovaný prietok [kg/s]
        """
        if supply_temp <= return_temp:
            raise ValueError("Teplota prívodnej vody musí byť vyššia ako vratnej")
        
        delta_t = supply_temp - return_temp  # teplotný spád [K]
        c_water = 4186  # merná tepelná kapacita vody [J/(kg.K)]
        
        flow_rate = heating_demand / (c_water * delta_t)  # kg/s
        return flow_rate
    
    @staticmethod
    def calculate_pressure_loss(flow_rate: float, 
                              pipe_length: float,
                              pipe_diameter: float,
                              fittings_factor: float = 1.5) -> float:
        """
        Výpočet tlakovej straty v potrubí [Pa]
        
        Args:
            flow_rate: prietok [kg/s]
            pipe_length: dĺžka potrubia [m]
            pipe_diameter: vnútorný priemer potrubia [m]
            fittings_factor: faktor armatur a tvaroviek [-]
            
        Returns:
            tlaková strata [Pa]
        """
        if pipe_diameter <= 0:
            raise ValueError("Priemer potrubia musí byť kladný")
        
        # Fyzikálne vlastnosti vody pri 60°C
        rho_water = 983.2  # kg/m³
        mu_water = 0.466e-3  # Pa.s
        
        # Plocha prierezu potrubia
        area = math.pi * (pipe_diameter / 2) ** 2  # m²
        
        # Rýchlosť prúdenia
        velocity = flow_rate / (rho_water * area)  # m/s
        
        # Reynoldsovo číslo
        reynolds = (rho_water * velocity * pipe_diameter) / mu_water
        
        # Súčiniteľ trenia (pre hydraulicky hladké potrubia)
        if reynolds < 2300:  # laminárne prúdenie
            friction_factor = 64 / reynolds
        else:  # turbulentné prúdenie
            friction_factor = 0.3164 / (reynolds ** 0.25)
        
        # Tlaková strata pri prúdení v potrubí
        pressure_loss_linear = friction_factor * (pipe_length / pipe_diameter) * \
                              (rho_water * velocity ** 2) / 2
        
        # Celková tlaková strata včítane armatur
        pressure_loss_total = pressure_loss_linear * fittings_factor
        
        return pressure_loss_total
    
    @staticmethod
    def calculate_valve_authority(valve_pressure_loss: float,
                                total_circuit_pressure_loss: float) -> float:
        """
        Výpočet autority regulačného ventilu [-]
        
        Args:
            valve_pressure_loss: tlaková strata na ventile pri plnom otvorení [Pa]
            total_circuit_pressure_loss: celková tlaková strata okruhu [Pa]
            
        Returns:
            autorita ventilu [-] (optimálne 0.3-0.7)
        """
        if total_circuit_pressure_loss <= 0:
            raise ValueError("Celková tlaková strata musí byť kladná")
        
        authority = valve_pressure_loss / total_circuit_pressure_loss
        return authority
    
    @staticmethod
    def calculate_balancing_valve_setting(required_flow: float,
                                        available_pressure: float,
                                        valve_kv_100: float) -> Tuple[float, float]:
        """
        Výpočet nastavenia vyvažovacieho ventilu
        
        Args:
            required_flow: požadovaný prietok [m³/h]
            available_pressure: dostupný diferenčný tlak [kPa]
            valve_kv_100: prietokový súčiniteľ ventilu pri plnom otvorení [m³/h]
            
        Returns:
            (kv_required, opening_percentage): potrebný kv a % otvorenia ventilu
        """
        if available_pressure <= 0 or valve_kv_100 <= 0:
            raise ValueError("Tlak a Kv musia byť kladné")
        
        # Výpočet potrebného prietokového súčiniteľa
        kv_required = required_flow / math.sqrt(available_pressure)
        
        # Percento otvorenia ventilu
        opening_percentage = (kv_required / valve_kv_100) * 100
        opening_percentage = min(100, max(0, opening_percentage))  # limitovanie na 0-100%
        
        return kv_required, opening_percentage
    
    @staticmethod
    def hydraulic_balancing_analysis(building: Building, 
                                   heating_demand_per_zone: Dict[str, float]) -> Dict[str, Dict]:
        """
        Komplexná analýza hydraulického vyregulovania
        
        Args:
            building: budova
            heating_demand_per_zone: tepelné výkony jednotlivých zón [W]
            
        Returns:
            slovník s výsledkami analýzy pre každú zónu
        """
        results = {}
        
        if not building.heating_system:
            return {"error": "Budova nemá definovaný vykurovací systém"}
        
        supply_temp = building.heating_system.supply_temperature
        return_temp = building.heating_system.return_temperature
        
        for zone in building.zones:
            zone_name = zone.name
            
            if zone_name not in heating_demand_per_zone:
                continue
            
            heating_demand = heating_demand_per_zone[zone_name]
            
            # Výpočet požadovaného prietoku
            flow_rate_kg_s = HydraulicCalculations.calculate_required_flow_rate(
                heating_demand, supply_temp, return_temp
            )
            flow_rate_m3_h = flow_rate_kg_s * 3.6  # konverzia na m³/h
            
            # Odhad parametrov potrubia (zjednodušené)
            estimated_pipe_length = math.sqrt(zone.floor_area) * 2  # odhad dĺžky potrubia
            pipe_diameter = 0.025  # 25mm vnútorný priemer
            
            # Výpočet tlakovej straty
            pressure_loss = HydraulicCalculations.calculate_pressure_loss(
                flow_rate_kg_s, estimated_pipe_length, pipe_diameter
            )
            
            # Nastavenie vyvažovacieho ventilu (príklad s Kv=2.5)
            available_pressure_kPa = pressure_loss / 1000  # konverzia na kPa
            kv_required, valve_opening = HydraulicCalculations.calculate_balancing_valve_setting(
                flow_rate_m3_h, available_pressure_kPa, 2.5
            )
            
            results[zone_name] = {
                'heating_demand_W': heating_demand,
                'required_flow_kg_s': flow_rate_kg_s,
                'required_flow_m3_h': flow_rate_m3_h,
                'estimated_pipe_length_m': estimated_pipe_length,
                'pressure_loss_Pa': pressure_loss,
                'pressure_loss_kPa': pressure_loss / 1000,
                'kv_required': kv_required,
                'valve_opening_percent': valve_opening,
                'temperature_supply': supply_temp,
                'temperature_return': return_temp,
                'temperature_difference': supply_temp - return_temp
            }
        
        return results


class CoolingCalculations:
    """Výpočty chladiacej potreby a parametrov chladiacich systémov"""
    
    @staticmethod
    def calculate_cooling_load_from_people(number_of_people: int, 
                                         activity_level: str = "sedavá_práca") -> float:
        """
        Výpočet tepelných ziskov od osôb [W]
        
        Args:
            number_of_people: počet osôb
            activity_level: úroveň aktivity (sedavá_práca, stredná_aktivita, vysoká_aktivita)
            
        Returns:
            tepelné zisky od osôb [W]
        """
        # Tepelné zisky podľa ASHRAE a STN EN 16798-1
        activity_gains = {
            "sedavá_práca": {"sensible": 70, "latent": 45},  # W/osoba
            "stredná_aktivita": {"sensible": 75, "latent": 55},
            "vysoká_aktivita": {"sensible": 85, "latent": 85}
        }
        
        if activity_level not in activity_gains:
            activity_level = "sedavá_práca"
        
        gains = activity_gains[activity_level]
        total_sensible = gains["sensible"] * number_of_people
        total_latent = gains["latent"] * number_of_people
        
        return total_sensible + total_latent
    
    @staticmethod
    def calculate_cooling_load_from_lighting(lighting_power: float,
                                           lighting_type: str = "LED") -> float:
        """
        Výpočet tepelných ziskov od osvetlenia [W]
        
        Args:
            lighting_power: inštalovaný výkon osvetlenia [W]
            lighting_type: typ osvetlenia (LED, fluorescenčné, žiarovky)
            
        Returns:
            tepelné zisky od osvetlenia [W]
        """
        # Faktor premeny elektrického výkonu na teplo
        conversion_factors = {
            "LED": 0.95,  # 95% sa premení na teplo
            "fluorescenčné": 1.25,  # vrátane predradníkov
            "žiarovky": 0.95,
            "halogénové": 1.0
        }
        
        factor = conversion_factors.get(lighting_type, 1.0)
        return lighting_power * factor
    
    @staticmethod
    def calculate_cooling_load_from_equipment(equipment_power: float,
                                            usage_factor: float = 0.7,
                                            simultaneity_factor: float = 0.8) -> float:
        """
        Výpočet tepelných ziskov od zariadení [W]
        
        Args:
            equipment_power: inštalovaný výkon zariadení [W]
            usage_factor: faktor využitia (0-1)
            simultaneity_factor: faktor súčasnosti prevádzky (0-1)
            
        Returns:
            tepelné zisky od zariadení [W]
        """
        return equipment_power * usage_factor * simultaneity_factor
    
    @staticmethod
    def calculate_solar_gains_through_windows(window_area: float,
                                            solar_radiation: float,
                                            shgc: float,
                                            shading_factor: float = 1.0) -> float:
        """
        Výpočet solárnych tepelných ziskov cez okná [W]
        
        Args:
            window_area: plocha okien [m²]
            solar_radiation: intenzita slnečného žiarenia [W/m²]
            shgc: súčiniteľ prechodu slnečnej energie cez okno (0-1)
            shading_factor: faktor tienenia (0-1)
            
        Returns:
            solárne tepelné zisky [W]
        """
        return window_area * solar_radiation * shgc * shading_factor
    
    @staticmethod
    def calculate_transmission_cooling_load(u_value: float,
                                          area: float,
                                          temp_difference: float) -> float:
        """
        Výpočet tepelných ziskov prechodom tepla cez konštrukcie [W]
        
        Args:
            u_value: súčiniteľ prechodu tepla [W/(m².K)]
            area: plocha konštrukcie [m²]
            temp_difference: teplotný rozdiel interiér-exteriér [K]
            
        Returns:
            tepelné zisky prechodom [W]
        """
        return u_value * area * temp_difference
    
    @staticmethod
    def calculate_ventilation_cooling_load(air_flow_rate: float,
                                         temp_difference: float,
                                         humidity_ratio_difference: float = 0) -> Dict[str, float]:
        """
        Výpočet chladiacej záťaže od vetraného vzduchu [W]
        
        Args:
            air_flow_rate: prietok vzduchu [m³/s]
            temp_difference: teplotný rozdiel [K]
            humidity_ratio_difference: rozdiel absolútnej vlhkosti [kg/kg]
            
        Returns:
            slovník s rozdelením na suchý a vlhký tepelný zisk
        """
        # Fyzikálne vlastnosti vzduchu
        rho_air = 1.2  # kg/m³
        c_air = 1010   # J/(kg.K)
        latent_heat = 2500000  # J/kg (latentné teplo vyparovania vody)
        
        mass_flow = air_flow_rate * rho_air  # kg/s
        
        # Suchý tepelný zisk
        sensible_load = mass_flow * c_air * temp_difference
        
        # Vlhký tepelný zisk
        latent_load = mass_flow * humidity_ratio_difference * latent_heat
        
        return {
            "sensible_cooling_load": sensible_load,
            "latent_cooling_load": latent_load,
            "total_cooling_load": sensible_load + latent_load
        }
    
    @staticmethod
    def calculate_total_cooling_load(building: Building,
                                   climate_data: ClimateData,
                                   occupancy_data: Dict) -> Dict[str, float]:
        """
        Celkový výpočet chladiacej potreby budovy [W]
        
        Args:
            building: budova
            climate_data: klimatické údaje
            occupancy_data: údaje o obsadenosti
            
        Returns:
            slovník s rozdelením chladiacej záťaže
        """
        total_people_load = 0
        total_lighting_load = 0
        total_equipment_load = 0
        total_solar_load = 0
        total_transmission_load = 0
        
        for zone in building.zones:
            # Tepelné zisky od osôb
            people_count = occupancy_data.get(f"{zone.name}_people", 0)
            activity = occupancy_data.get(f"{zone.name}_activity", "sedavá_práca")
            people_load = CoolingCalculations.calculate_cooling_load_from_people(
                people_count, activity
            )
            total_people_load += people_load
            
            # Tepelné zisky od osvetlenia
            lighting_power = occupancy_data.get(f"{zone.name}_lighting", zone.floor_area * 10)  # 10W/m²
            lighting_load = CoolingCalculations.calculate_cooling_load_from_lighting(lighting_power)
            total_lighting_load += lighting_load
            
            # Tepelné zisky od zariadení
            equipment_power = occupancy_data.get(f"{zone.name}_equipment", zone.floor_area * 15)  # 15W/m²
            equipment_load = CoolingCalculations.calculate_cooling_load_from_equipment(equipment_power)
            total_equipment_load += equipment_load
            
            # Solárne zisky cez okná
            for window in zone.windows:
                orientation = window.orientation.upper()
                solar_radiation = climate_data.solar_radiation.get(orientation, 300)  # W/m²
                solar_load = CoolingCalculations.calculate_solar_gains_through_windows(
                    window.area, solar_radiation, window.g_value, window.shading_factor
                )
                total_solar_load += solar_load
            
            # Tepelné zisky prechodom cez konštrukcie
            for construction in zone.constructions:
                if construction.construction_type in [ConstructionType.EXTERNAL_WALL, ConstructionType.ROOF]:
                    temp_diff = climate_data.external_temperature - 24  # vnútorná teplota 24°C
                    if temp_diff > 0:  # len ak je vonku teplejšie
                        transmission_load = CoolingCalculations.calculate_transmission_cooling_load(
                            construction.u_value(), construction.area, temp_diff
                        )
                        total_transmission_load += transmission_load
        
        # Celková chladiaca potreba
        total_cooling_load = (total_people_load + total_lighting_load + 
                            total_equipment_load + total_solar_load + 
                            total_transmission_load)
        
        return {
            "people_load_W": total_people_load,
            "lighting_load_W": total_lighting_load,
            "equipment_load_W": total_equipment_load,
            "solar_load_W": total_solar_load,
            "transmission_load_W": total_transmission_load,
            "total_cooling_load_W": total_cooling_load,
            "specific_cooling_load_W_m2": total_cooling_load / building.total_floor_area()
        }
    
    @staticmethod
    def calculate_cooling_system_cop(evaporator_temp: float,
                                   condenser_temp: float,
                                   efficiency_factor: float = 0.6) -> float:
        """
        Výpočet COP chladiaceho systému na základe Carnotovho cyklu
        
        Args:
            evaporator_temp: teplota výparníka [°C]
            condenser_temp: teplota kondenzátora [°C]
            efficiency_factor: účinnosť vzhľadom na Carnotov cyklus (0-1)
            
        Returns:
            COP chladiaceho systému [-]
        """
        t_evap_k = evaporator_temp + 273.15  # konverzia na Kelvin
        t_cond_k = condenser_temp + 273.15
        
        # Carnotov COP pre chladenie
        cop_carnot = t_evap_k / (t_cond_k - t_evap_k)
        
        # Reálny COP
        cop_real = cop_carnot * efficiency_factor
        
        return cop_real
    
    @staticmethod
    def calculate_cooling_energy_consumption(cooling_load: float,
                                           cop: float,
                                           operating_hours: float) -> Dict[str, float]:
        """
        Výpočet spotreby energie chladiaceho systému
        
        Args:
            cooling_load: chladiaci výkon [W]
            cop: COP systému [-]
            operating_hours: prevádzkové hodiny [h]
            
        Returns:
            slovník s energetickými parametrami
        """
        electrical_power = cooling_load / cop  # W
        annual_energy_consumption = (electrical_power * operating_hours) / 1000  # kWh
        
        return {
            "electrical_power_W": electrical_power,
            "annual_energy_kWh": annual_energy_consumption,
            "specific_energy_kWh_m2": annual_energy_consumption / building.total_floor_area() if 'building' in locals() else 0,
            "cop_system": cop
        }


# STN požiadavky pre tepelno-technické posúdenie
STN_REQUIREMENTS = {
    "vonkajšia_stena": {
        "U_max": 1.40,  # W/(m².K)
        "U_N": 0.46,
        "U_r1": 0.32,
        "U_r2": 0.25
    },
    "strecha": {
        "U_max": 0.70,
        "U_N": 0.34,
        "U_r1": 0.20,
        "U_r2": 0.16
    },
    "podlaha": {
        "U_max": 1.45,
        "U_N": 0.60,
        "U_r1": 0.40,
        "U_r2": 0.30
    },
    "okná": {
        "U_max": 2.80,
        "U_N": 1.70,
        "U_r1": 1.20,
        "U_r2": 0.90
    }
}

# Klimatické údaje pre Slovensko - chladenie
SLOVAK_COOLING_DATA = {
    "bratislava": {
        "design_temp_C": 32,  # návrhová vonkajšia teplota
        "cooling_degree_days": 180,  # chladiace deň-stupne
        "solar_radiation_horizontal_kWh_m2": 1200,
        "relative_humidity_percent": 65,
        "cooling_season_days": 90
    },
    "košice": {
        "design_temp_C": 31,
        "cooling_degree_days": 160,
        "solar_radiation_horizontal_kWh_m2": 1150,
        "relative_humidity_percent": 68,
        "cooling_season_days": 85
    },
    "žilina": {
        "design_temp_C": 29,
        "cooling_degree_days": 120,
        "solar_radiation_horizontal_kWh_m2": 1100,
        "relative_humidity_percent": 70,
        "cooling_season_days": 70
    }
}
