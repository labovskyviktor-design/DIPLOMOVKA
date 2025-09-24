"""
Dátové modely pre energetický audit budov
Implementované podľa STN noriem z skrípt Krajčík, Petráš, Skalíková
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import json


class BuildingCategory(Enum):
    """Kategórie budov podľa STN"""
    FAMILY_HOUSE = "rodinný_dom"
    APARTMENT_BUILDING = "bytový_dom" 
    OFFICE_BUILDING = "administratívna_budova"
    SCHOOL = "škola"
    OTHER = "iné"


class ConstructionType(Enum):
    """Typy konštrukcií"""
    EXTERNAL_WALL = "vonkajšia_stena"
    ROOF = "strecha"
    FLOOR_ON_GROUND = "podlaha_na_teréne"
    FLOOR_ABOVE_UNHEATED = "strop_nad_nevykurovaným"
    INTERNAL_WALL = "vnútorná_stena"
    WINDOW = "okno"
    DOOR = "dvere"


class HeatingSystemType(Enum):
    """Typy vykurovacích systémov"""
    RADIATOR = "radiátorový"
    FLOOR_HEATING = "podlahový"
    WALL_HEATING = "stenový"
    CEILING_HEATING = "stropný"


@dataclass
class Material:
    """Stavebný materiál s tepelno-technickými vlastnosťami"""
    name: str
    thermal_conductivity: float  # λ [W/(m.K)]
    density: float = 0.0  # ρ [kg/m³]
    specific_heat: float = 0.0  # c [J/(kg.K)]
    category: str = ""
    
    def thermal_resistance(self, thickness: float) -> float:
        """Tepelný odpor vrstvy R = d/λ [(m².K)/W]"""
        if self.thermal_conductivity <= 0:
            raise ValueError("Tepelná vodivosť musí byť kladná")
        return thickness / self.thermal_conductivity


@dataclass 
class Layer:
    """Vrstva v konštrukcii"""
    material: Material
    thickness: float  # hrúbka [m]
    
    def thermal_resistance(self) -> float:
        """Tepelný odpor vrstvy"""
        return self.material.thermal_resistance(self.thickness)


@dataclass
class Construction:
    """Stavebná konštrukcia zložená z vrstiev"""
    name: str
    construction_type: ConstructionType
    layers: List[Layer] = field(default_factory=list)
    area: float = 0.0  # plocha [m²]
    orientation: str = ""  # orientácia (S, V, J, Z)
    
    # Prestupy tepla na povrchoch [(m².K)/W]
    rsi: float = 0.13  # vnútorný povrch (horizontálny tok)
    rse: float = 0.04  # vonkajší povrch
    
    def total_thermal_resistance(self) -> float:
        """Celkový tepelný odpor R = Rsi + ΣRi + Rse"""
        layer_resistance = sum(layer.thermal_resistance() for layer in self.layers)
        return self.rsi + layer_resistance + self.rse
    
    def u_value(self) -> float:
        """Súčiniteľ prechodu tepla U = 1/R [W/(m².K)]"""
        r_total = self.total_thermal_resistance()
        if r_total <= 0:
            raise ValueError("Celkový tepelný odpor musí byť kladný")
        return 1.0 / r_total
    
    def add_layer(self, material: Material, thickness: float):
        """Pridanie vrstvy do konštrukcie"""
        self.layers.append(Layer(material, thickness))


@dataclass
class Window:
    """Okno alebo dvere"""
    name: str
    area: float  # plocha [m²]
    u_value: float  # súčiniteľ prechodu tepla [W/(m².K)]
    g_value: float = 0.6  # celková priepustnosť slnečnej energie [-]
    orientation: str = ""  # orientácia (S, V, J, Z)
    shading_factor: float = 0.8  # tieniaci faktor [-]


@dataclass
class ThermalBridge:
    """Tepelný most"""
    name: str
    psi_value: float  # lineárny súčiniteľ tepelného mosta [W/(m.K)]
    length: float  # dĺžka [m]


@dataclass
class Zone:
    """Zóna budovy"""
    name: str
    floor_area: float  # podlahová plocha [m²]
    volume: float  # objem [m³]
    internal_temperature: float = 20.0  # vnútorná teplota [°C]
    constructions: List[Construction] = field(default_factory=list)
    windows: List[Window] = field(default_factory=list)
    thermal_bridges: List[ThermalBridge] = field(default_factory=list)


@dataclass
class HeatingSystem:
    """Vykurovací systém"""
    system_type: HeatingSystemType
    supply_temperature: float = 90.0  # teplota prívodnej vody [°C]
    return_temperature: float = 70.0  # teplota vratnej vody [°C]
    efficiency: float = 0.85  # účinnosť [-]
    hydraulic_adjustment: bool = False  # hydraulické vyregulovanie
    temperature_control: str = "centrálna"  # typ regulácie
    
    def temperature_difference(self) -> float:
        """Teplotný spád"""
        return self.supply_temperature - self.return_temperature


@dataclass
class HotWaterSystem:
    """Systém prípravy teplej vody"""
    hot_water_temperature: float = 60.0  # teplota TV [°C]
    cold_water_temperature: float = 10.0  # teplota studenej vody [°C]
    circulation: bool = True  # cirkulácia
    storage_volume: float = 0.0  # objem zásobníka [l]
    efficiency: float = 0.85  # účinnosť [-]


@dataclass
class ClimateData:
    """Klimatické údaje pre lokalitu"""
    external_temperature: float = 3.86  # priemerná vonkajšia teplota [°C]
    heating_days: int = 212  # počet vykurovacích dní
    degree_days: float = 3422.0  # dennostupne [K.deň]
    solar_radiation: Dict[str, float] = field(default_factory=lambda: {
        'S': 320, 'V': 200, 'Z': 200, 'J': 320,
        'SV': 130, 'SZ': 130, 'JV': 260, 'JZ': 260
    })  # intenzita slnečného žiarenia [kWh/m²]


@dataclass 
class Building:
    """Budova"""
    name: str
    category: BuildingCategory
    zones: List[Zone] = field(default_factory=list)
    heating_system: Optional[HeatingSystem] = None
    hot_water_system: Optional[HotWaterSystem] = None
    climate_data: ClimateData = field(default_factory=ClimateData)
    
    # Geometrické charakteristiky
    length: float = 0.0  # [m]
    width: float = 0.0  # [m] 
    height: float = 0.0  # [m]
    floors_count: int = 1
    
    def total_floor_area(self) -> float:
        """Celková podlahová plocha"""
        return sum(zone.floor_area for zone in self.zones)
    
    def total_volume(self) -> float:
        """Celkový objem"""
        return sum(zone.volume for zone in self.zones)
    
    def envelope_area(self) -> float:
        """Plocha teplovýmenného obalu"""
        total_area = 0.0
        for zone in self.zones:
            for construction in zone.constructions:
                total_area += construction.area
            for window in zone.windows:
                total_area += window.area
        return total_area
    
    def shape_factor(self) -> float:
        """Faktor tvaru A/V [1/m]"""
        envelope = self.envelope_area()
        volume = self.total_volume()
        if volume <= 0:
            raise ValueError("Objem budovy musí byť kladný")
        return envelope / volume
    
    def add_zone(self, zone: Zone):
        """Pridanie zóny do budovy"""
        self.zones.append(zone)
    
    def to_dict(self) -> Dict:
        """Konverzia do slovníka pre JSON"""
        # Implementácia pre export/import údajov
        pass
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Building':
        """Vytvorenie z slovníka"""
        # Implementácia pre import údajov
        pass


# Predpripravené materiály podľa STN 73 0540-3
STANDARD_MATERIALS = {
    # Muriva a betóny
    'železobetón': Material('Železobetón', 1.58),
    'pórobetón': Material('Pórobetón', 0.19),
    'tehla_plná': Material('Tehla plná', 0.80),
    'tehla_dierovaná': Material('Tehla dierovaná', 0.35),
    
    # Tepelné izolácie
    'polystyrén_exp': Material('Polystyrén expandovaný', 0.044),
    'polystyrén_extrud': Material('Polystyrén extrudovaný', 0.035),
    'minerálna_vlna': Material('Minerálna vlna', 0.044),
    'polyuretán': Material('Polyuretán', 0.030),
    
    # Omietky
    'omietka_vnútorná': Material('Omietka vnútorná', 0.88),
    'omietka_vonkajšia': Material('Omietka vonkajšia', 1.16),
    
    # Ostatné
    'vzduch': Material('Vzduchová medzera', 0.025),
    'drevo_ihličnan': Material('Drevo ihličnaté', 0.18),
    'oceľ': Material('Oceľ', 50.0),
}

@dataclass
class EnergyAuditResults:
    """Výsledky energetického auditu"""
    building_name: str
    audit_date: str
    
    # Tepelno-technické vlastnosti
    envelope_u_values: Dict[str, float] = field(default_factory=dict)
    stn_compliance: Dict[str, bool] = field(default_factory=dict)
    
    # Energetické potreby
    heating_demand_kwh: float = 0.0
    hot_water_demand_kwh: float = 0.0
    total_energy_demand_kwh: float = 0.0
    specific_energy_demand_kwh_m2: float = 0.0
    
    # Hydraulické vyregulovanie
    hydraulic_balancing_results: Dict[str, Dict] = field(default_factory=dict)
    current_hydraulic_state: str = "nevyregulované"
    
    # Odporúčané opatrenia
    recommended_measures: List[str] = field(default_factory=list)
    estimated_savings_kwh: float = 0.0
    estimated_cost_eur: float = 0.0
    payback_period_years: float = 0.0
    
    def add_measure(self, measure: str, savings: float, cost: float):
        """Pridanie odporúčaného opatrenia"""
        self.recommended_measures.append(measure)
        self.estimated_savings_kwh += savings
        self.estimated_cost_eur += cost
        
        # Prepočítanie návratnosti
        if self.estimated_savings_kwh > 0:
            # Predpokladáme cenu energie 0.15 EUR/kWh
            annual_savings_eur = self.estimated_savings_kwh * 0.15
            if annual_savings_eur > 0:
                self.payback_period_years = self.estimated_cost_eur / annual_savings_eur
    
    def export_to_dict(self) -> Dict:
        """Export výsledkov do slovníka pre JSON"""
        return {
            'building_name': self.building_name,
            'audit_date': self.audit_date,
            'envelope_u_values': self.envelope_u_values,
            'stn_compliance': self.stn_compliance,
            'energy_demands': {
                'heating_kwh': self.heating_demand_kwh,
                'hot_water_kwh': self.hot_water_demand_kwh,
                'total_kwh': self.total_energy_demand_kwh,
                'specific_kwh_m2': self.specific_energy_demand_kwh_m2
            },
            'hydraulic_balancing': {
                'current_state': self.current_hydraulic_state,
                'zone_results': self.hydraulic_balancing_results
            },
            'recommendations': {
                'measures': self.recommended_measures,
                'estimated_savings_kwh': self.estimated_savings_kwh,
                'estimated_cost_eur': self.estimated_cost_eur,
                'payback_period_years': self.payback_period_years
            }
        }


# Typické konštrukcie pre energetické audity
TYPICAL_CONSTRUCTIONS = {
    'externá_stena_70_80': {
        'name': 'Vonkajšia stena 70-80te roky',
        'layers': [
            ('omietka_vnútorná', 0.015),  # 1.5cm vnútorná omietka
            ('tehla_plná', 0.380),         # 38cm tehla plná
            ('omietka_vonkajšia', 0.020)   # 2cm vonkajšia omietka
        ],
        'u_value_estimate': 1.45  # W/(m².K)
    },
    'externá_stena_panelák': {
        'name': 'Vonkajšia stena panelového domu',
        'layers': [
            ('omietka_vnútorná', 0.015),
            ('železobetón', 0.150),
            ('polystyrén_exp', 0.040),
            ('omietka_vonkajšia', 0.010)
        ],
        'u_value_estimate': 0.75  # W/(m².K)
    },
    'strecha_nevyregulovaná': {
        'name': 'Strecha bez izolácie',
        'layers': [
            ('omietka_vnútorná', 0.015),
            ('železobetón', 0.120),
            ('hydroizolacia', 0.005)
        ],
        'u_value_estimate': 4.2  # W/(m².K)
    },
    'podlaha_na_teréne': {
        'name': 'Podlaha na teréne',
        'layers': [
            ('betón', 0.050),
            ('železobetón', 0.120)
        ],
        'u_value_estimate': 2.8  # W/(m².K)
    }
}


# Požiadavky STN 73 0540-2/Z1 (aktualizované hodnoty)
STN_REQUIREMENTS = {
    'vonkajšia_stena': {
        'U_max': 1.40,  # maximálna prípustná hodnota
        'U_N': 0.46,   # normová hodnota
        'U_r1': 0.32,  # odporúčaná hodnota 1
        'U_r2': 0.25   # odporúčaná hodnota 2 (nízkoenergetické)
    },
    'strecha': {
        'U_max': 0.70,
        'U_N': 0.34,
        'U_r1': 0.20,
        'U_r2': 0.16
    },
    'podlaha': {
        'U_max': 1.45,
        'U_N': 0.60,
        'U_r1': 0.40,
        'U_r2': 0.30
    },
    'okná': {
        'U_max': 2.80,
        'U_N': 1.70,
        'U_r1': 1.20,
        'U_r2': 0.90
    }
}


# Predpripravené príklady budov pre demo
DEMO_BUILDINGS = {
    'rodinny_dom_70': {
        'name': 'Rodinný dom z 70. rokov',
        'category': BuildingCategory.FAMILY_HOUSE,
        'dimensions': {'length': 12.0, 'width': 8.0, 'height': 3.0},
        'constructions': ['externá_stena_70_80', 'strecha_nevyregulovaná', 'podlaha_na_teréne'],
        'heating_system': {
            'type': HeatingSystemType.RADIATOR,
            'supply_temp': 90.0,
            'return_temp': 70.0,
            'efficiency': 0.75,
            'hydraulic_adjustment': False
        }
    },
    'panelovy_dom_80': {
        'name': 'Panelový bytový dom z 80. rokov',
        'category': BuildingCategory.APARTMENT_BUILDING,
        'dimensions': {'length': 48.0, 'width': 12.0, 'height': 30.0},
        'constructions': ['externá_stena_panelák'],
        'heating_system': {
            'type': HeatingSystemType.RADIATOR,
            'supply_temp': 90.0,
            'return_temp': 70.0,
            'efficiency': 0.85,
            'hydraulic_adjustment': False
        }
    }
}
