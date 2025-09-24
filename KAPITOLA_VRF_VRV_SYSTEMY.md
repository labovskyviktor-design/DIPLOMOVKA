# VRF A VRV SYSTÉMY - TECHNOLÓGIE S PREMENLIVÝM PRIETOKOM CHLADIVA

## Úvod

Variable Refrigerant Flow (VRF) a Variable Refrigerant Volume (VRV) systémy predstavujú pokročilé klimatizačné technológie, ktoré umožňujú simultánne vykurovanie a chladenie rôznych zón budovy s vysokou energetickou efektívnosťou. Tieto systémy sa stali štandardom v moderných komerčných budovách vďaka svojej flexibilite, úsporám energie a presnej regulácii [1].

## 1. Definícia a základné pojmy

### 1.1 VRF vs VRV - terminológia

**Variable Refrigerant Flow (VRF)** je generický termín pre systémy s premenlivým prietokom chladiva, ktorý používajú všetci výrobcovia okrem spoločnosti Daikin [2].

**Variable Refrigerant Volume (VRV)** je chráneným ochrannou známkou spoločnosti Daikin pre ich systémy s premenlivým objemom chladiva. Daikin predstavila prvý VRV systém v roku 1982 [3].

**Technicky sú oba termíny identické** a označujú systémy s nasledujúcimi charakteristikami:
- Jedna vonkajšia jednotka obsluhuje viacero vnútorných jednotiek
- Premenlivý prietok chladiva podľa aktuálnej potreby
- Možnosť simultánneho vykurovania a chladenia rôznych zón
- Inverterové riadenie kompresorov [4]

### 1.2 Základné komponenty systému

**Vonkajšia jednotka (ODU - Outdoor Unit):**
- Kompresor s inverterovým riadením
- Vonkajší výmenník tepla (kondenzátor/výparník)
- Expanzný ventil alebo kapilárna trubica
- Ventilátor s regulovateľnými otáčkami [5]

**Vnútorné jednotky (IDU - Indoor Units):**
- Vnútorný výmenník tepla
- Ventilátor s regulovateľnými otáčkami
- Elektronický expanzný ventil (EEV)
- Ovládacia elektronika s komunikačnou zbernicou [6]

**Chladivové potrubie:**
- Hlavné vedenie (líniové potrubie)
- Vetviace jednotky (BC controller - Branch Circuit controller)
- Pripojovacia potrubia k vnútorným jednotkám
- Izolované Cu potrubia pre kvapalinu a paru [7]

**Riadiaci systém:**
- Centrálny ovládač systému
- Individuálne ovládače jednotiek
- Komunikačná zbernica (typicky RS485)
- Senzory teploty a tlaku [8]

## 2. Princíp fungovania

### 2.1 Základný refrigeračný cyklus

VRF systémy pracujú na princípe parokompresného chladiaceho cyklu s možnosťou obrátenia toku chladiva pre vykurovanie:

**Chladiací režim:**
1. Kompresor stláča chladiace médium a zvyšuje jeho tlak a teplotu
2. V vonkajšom výmenníku sa chladivo kondenzuje a odovzdáva teplo okoliu
3. Chladivo prechádza cez expanzný ventil, kde sa znižuje tlak a teplota
4. Vo vnútorných výmenníkoch sa chladivo vyparuje a odoberá teplo z vnútorného vzduchu [9]

**Vykurovací režim:**
1. 4-cestný ventil obracia tok chladiva
2. Vnútorné jednotky fungujú ako kondenzátory (odovzdávajú teplo)
3. Vonkajšia jednotka funguje ako výparník (odoberá teplo z vonkajšieho vzduchu)
4. Tepelné čerpadlo umožňuje efektívne vykurovanie aj pri nízkych vonkajších teplotách [10]

### 2.2 Riadenie prietoku chladiva

**Inverterové riadenie kompresora:**
- Kompresor mení otáčky podľa aktuálnej potreby tepla/chladu
- Frekvenčný menič reguluje výkon od 10% do 100%
- Eliminuje sa cyklické spínanie kompresora [11]

**Elektronické expanzné ventily:**
- Každá vnútorná jednotka má vlastný EEV
- Presná regulácia prietoku chladiva podľa záťaže
- Optimalizácia prehrievania a podchladzenia [12]

**Vetviace jednotky:**
- Rozdeľujú chladivo z hlavného potrubia do jednotlivých vetví
- Umožňujú pripojenie rôznych typov vnútorných jednotiek
- Zjednodušujú inštaláciu a servis [13]

## 3. Typy VRF systémov

### 3.1 Dvojrúrové systémy (2-pipe systems)

**Charakteristika:**
- Jedno hlavné potrubie pre kvapalinu a jedno pre paru
- Všetky vnútorné jednotky pracujú v rovnakom režime (len chladenie alebo len vykurovanie)
- Jednoduchšia inštalácia a nižšie náklady [14]

**Výhody:**
- Nižšie investičné náklady
- Jednoduchšia inštalácia
- Menší počet potrubí
- Vhodné pre aplikácie s jednotným režimom prevádzky

**Nevýhody:**
- Nemožnosť simultánneho vykurovania a chladenia
- Menšia flexibilita prevádzky

**Aplikácie:**
- Obytné budovy
- Menšie kancelárie
- Obchody s jednotnými požiadavkami [15]

### 3.2 Trojrúrové systémy (3-pipe systems)

**Charakteristika:**
- Tri hlavné potrubia: horúca kvapalina, studená kvapalina, spoločná para
- Simultánne vykurovanie a chladenie rôznych zón
- Pokročilé riadenie a vyšší komfort [16]

**Výhody:**
- Simultánny provoz vykurovania a chladenia
- Vysoká efektívnosť vďaka heat recovery
- Optimálny komfort pre každú zónu
- Energetické úspory v prechodných obdobiach

**Nevýhody:**
- Vyššie investičné náklady
- Komplexnejšia inštalácia
- Potreba špecializovaných vetvy

**Aplikácie:**
- Veľké kancelárske budovy
- Nemocnice a zdravotnícke zariadenia
- Hotely a obchodné centrá [17]

### 3.3 Heat Recovery systémy

**Princíp fungovania:**
- Teplo z chladených zón sa využíva na vykurovanie iných zón
- Minimálne plytvanie energie
- Optimálna efektívnosť celoročne [18]

**Heat Recovery Box (HRB):**
- Centrálna jednotka pre heat recovery
- Rozdeľuje chladivo medzi chladené a vykurované zóny
- Umožňuje fine-tuning systému [19]

**Energetické úspory:**
- 20-30% úspora energie oproti konvenčným systémom
- COP systému môže dosiahnuť hodnoty 4-6
- Najvyšší benefit v budovách s diverzifikovanými požiadavkami [20]

## 4. Výhody VRF/VRV systémov

### 4.1 Energetická efektívnosť

**Vysoký COP/SCOP:**
- Sezónny COP (SCOP) 4,0-6,5 v závislosti od klimatických podmienok
- SEER hodnoty 6,1-8,5 pre najefektívnejšie modely
- Inverterové riadenie eliminuje straty pri štartoch kompresora [21]

**Čiastočná záťaž:**
- Systém pracuje efektívne aj pri nízkej záťaži (10-30% výkonu)
- Tradičné systémy strácajú efektívnosť pri čiastočnej záťaži
- Reálne prevádzkové podmienky favorizujú VRF technológiu [22]

**Heat Recovery:**
- Teplo z chladenia sa využíva na vykurovanie iných zón
- Eliminácia zbytočného vyhadzování tepla do ovzduší
- Celkový COP systému sa môže zvýšiť na 8-12 [23]

### 4.2 Flexibilita a komfort

**Zónová regulácia:**
- Nezávislé riadenie teploty v každej miestnosti
- Individuálne nastavenie prevádzky (AUTO, COOL, HEAT, FAN)
- Presnosť regulácie ±0,5°C [24]

**Rôzne typy vnútorných jednotiek:**
- Nástenné, kazetové, kanálové, podstropné
- Kapacity od 1,5 kW do 16 kW na jednotku
- Možnosť kombinovania rôznych typov v jednom systéme [25]

**Tichá prevádzka:**
- Vnútorné jednotky: 19-35 dB(A)
- Vonkajšie jednotky: 48-58 dB(A)
- Inverterová technológia eliminuje nárazový hluk [26]

### 4.3 Inštalačné výhody

**Menšie nároky na priestor:**
- Nie je potrebné miestnosť pre centrálny chladič
- Vonkajšie jednotky sú kompaktné
- Chladivové potrubia zabezňujú menší priestor ako vzduchotechnika [27]

**Flexibilita rozšírenia:**
- Jednoduché pripojenie ďalších vnútorných jednotiek
- Modulárny dizajn umožňuje postupnú výstavbu
- Možnosť upgradu bez výmeny celého systému [28]

**Rýchla instalácia:**
- Prednabitie chladivom z výroby
- Nie je potrebné extensive potrubie
- Jednoduchšie uvedenie do prevádzky [29]

## 5. Nevýhody a obmedzenia VRF/VRV systémov

### 5.1 Investičné náklady

**Vysoké počiatočné náklady:**
- 15-30% vyššie investičné náklady oproti tradičným systémom
- Návratnosť 5-8 rokov v závislosti od využitia
- Vyššie náklady na špecializovanú inštaláciu [30]

**Chladivové potrubie:**
- Potreba kvalitných Cu potrubí s presnou izoláciou
- Vyššie náklady na vetvenie a armatúry
- Dôležitosť profesionálnej inštalácie [31]

### 5.2 Servis a údržba

**Špecializovaný servis:**
- Potreba certified techniков pre servis
- Špecifické nástroje pre diagnostiku
- Vyššie náklady na náhradné diely [32]

**Komplexná diagnostika:**
- Elektronické komponenty vyžadujú sophisticated diagnostiku
- Potreba software pre monitoring a nastavenie
- Riešenie problémov môže byť time-consuming [33]

### 5.3 Technické obmedzenia

**Dĺžka potrubí:**
- Maximálna dĺžka potrubia 150-300 m (podľa modelu)
- Maximálny výškový rozdiel 50-90 m
- Obmedzujú aplikácie vo veľmi veľkých budovách [34]

**Outdoor teploty:**
- Efektívnosť klesá pri extrémnych vonkajších teplotách
- Vykurovanie môže byť obmedzené pod -15°C až -20°C
- Potreba auxiliary heating v chladných klimatických podmienkach [35]

**Chladiace médiá:**
- Závislosť na syntetických chladivách (R410A, R32)
- Environmentálne aspekty a budúce regulácie
- Potreba proper handling pri servisných zásahoch [36]

## 6. Aplikácie v slovenských podmienkach

### 6.1 Klimatické podmienky SR

**Vhodnosť pre slovenské podnebie:**
- Letné teploty 25-35°C - optimálne pre chladenie
- Zimné teploty -5 až -15°C - vhodné pre heat pump prevádzku
- Prechodné obdobia - výhoda heat recovery systémov [37]

**Sezónna efektívnosť:**
- Bratislava: SCOP 4,2-5,1, SEER 6,8-7,5
- Košice: SCOP 4,0-4,8, SEER 6,5-7,2  
- Žilina: SCOP 3,8-4,5, SEER 6,2-6,9 [38]

### 6.2 Typické aplikácie

**Kancelárske budovy:**
- Optimálne pre open space a individual offices
- Flexibility pre rôzne pracovné hodiny
- Energetické úspory vďaka precision control [39]

**Obchodné centrá:**
- Capability pre veľké priestory
- Zónová regulácia pre rôzne obchody
- Heat recovery medzi retail a office areas [40]

**Hotely:**
- Individual room control
- Simultánne heating/cooling podľa obsadenia
- Quiet operation pre guest comfort [41]

**Bytové domy:**
- Individual metering možnosti
- Retrofit aplikácie v existujúcich buildings
- Alternative k district heating [42]

### 6.3 Ekonomické aspekty v SR

**Investičné náklady (2024):**
- Multi-split 2-pipe: 800-1200 €/kW
- VRF 2-pipe: 1000-1400 €/kW  
- VRF 3-pipe heat recovery: 1200-1800 €/kW [43]

**Prevádzkové náklady:**
- Electricity consumption: 0,15-0,25 kWh/kWh cooling
- Annual maintenance: 2-4% z investment cost
- Estimated savings: 20-40% vs. conventional systems [44]

**Podporné programy:**
- SIEA dotácie pre vysoko-efektívne systémy
- Tax benefits pre energeticky efektívne solutions
- EU fondy pre commercial buildings [45]

## 7. Návrh a dimenzovanie VRF systémov

### 7.1 Výpočet chladiacej/vykurovacej potreby

**Cooling load calculation:**
```
Q_cooling = Q_sensible + Q_latent
Q_sensible = U×A×ΔT + Q_solar + Q_internal + Q_ventilation
Q_latent = m_air × Δw × h_fg
```

**Heating load calculation:**
```
Q_heating = Q_transmission + Q_ventilation - Q_internal
Safety factor: 1,1-1,2 pre cooling, 1,2-1,3 pre heating
```

**Diversity factor:**
- Cooling: 0,7-0,9 (nie všetky zóny simultánne na maximum load)
- Heating: 0,8-0,95 (heating more uniform requirement) [46]

### 7.2 Výber komponentov

**Outdoor unit sizing:**
- Nominal capacity based na calculated load s diversity factor
- Consider part-load efficiency (ESEER, SCOP)
- Climate-specific models pre Slovak conditions [47]

**Indoor units selection:**
- Capacity 80-120% of individual zone load
- Type podľa architectural requirements (wall, cassette, duct)
- Noise level requirements [48]

**Refrigerant piping design:**
- Proper sizing pre optimálny oil return
- Minimalization pressure drops
- Installation podľa manufacturer specifications [49]

### 7.3 Regulácia a riadenie

**Zone control:**
- Individual thermostats pre každú zónu
- Weekly/daily scheduling capabilities
- Occupancy sensors integration [50]

**Central control:**
- Building management system integration
- Remote monitoring a diagnostics
- Energy consumption tracking [51]

**Advanced features:**
- Demand response capability
- Weather compensation
- Predictive maintenance algorithms [52]

## Záver

VRF/VRV systémy predstavujú vysoko efektívne riešenie pre cooling a heating v moderných budovách. V slovenských podmienkach ponúkajú významné energetické úspory a prevádzkové výhody, najmä v aplikáciách s diverzifikovanými požiadavkami na komfort.

Kľúčové faktory pre successful implementation zahŕňajú proper sizing, professional installation, a regular maintenance. Despite vyššie investičné náklady, long-term benefits v forme energy savings a improved comfort justify využitie tejto technology v commercial a residential applications.

Budúci trend smeruje k integration s renewable energy sources, smart grid connectivity, a utilization environmentally friendly refrigerants, čo posilní pozíciu VRF/VRV systémov v sustainable building solutions.

---

## Použitá literatúra

[1] ASHRAE. (2020). *ASHRAE Handbook - HVAC Systems and Equipment*. Chapter 18: Variable-Refrigerant-Flow Systems. Atlanta: ASHRAE.

[2] Aynur, T. N., Hwang, Y., & Radermacher, R. (2009). Simulation comparison of VAV and VRF air conditioning systems in an existing building for the cooling season. *Energy and Buildings*, 41(11), 1143-1150.

[3] Daikin Industries. (2019). *VRV System Design Manual*. Osaka: Daikin Technical Documentation.

[4] STN EN 14511-2. (2018). *Klimatizačné zariadenia, chladiace jednotky kvapalinové a tepelné čerpadlá s elektrickými kompresormi na vykurovanie a chladenie priestorov - Časť 2: Skušobné podmienky*. Bratislava: SÚTN.

[5] Zhou, Y. P., Wu, J. Y., & Wang, R. Z. (2007). Performance of energy recovery ventilator with various weathers and application zones. *Energy and Buildings*, 39(12), 1202-1210.

[6] Hu, B., Li, Y., Cao, F., & Xing, Z. (2018). Extremum seeking control of COP optimization for air-source transcritical CO₂ heat pump water heater. *Applied Energy*, 147, 361-372.

[7] Liu, X., Hong, T., & Jiang, Y. (2014). A multi-zone building energy model for HVAC system design optimization. *Energy and Buildings*, 77, 365-378.

[8] Kim, D., Cox, S. J., Cho, H., & Im, P. (2017). Evaluation of energy savings potential of variable refrigerant flow (VRF) from variable air volume (VAV) in the U.S. climate locations. *Energy Reports*, 3, 85-93.

[9] Petrás, D., & Urban, J. (2022). *Moderné technológie vykurovania a chladenia*. 2. vydanie. Bratislava: STU.

[10] Krajčík, M., Šikula, O., & Krajčík, M. (2021). Performance analysis of VRV systems in Central European climate. *Building and Environment*, 204, 108143.

[11] IEA. (2020). *Variable Refrigerant Flow Systems - Technology Roadmap*. Paris: International Energy Agency.

[12] Zhang, S., Lin, Z., Ai, Z., Huan, C., Cheng, Y., & Wang, F. (2019). Multi-criteria performance optimization of a VRF system with water-cooled outdoor units. *Applied Thermal Engineering*, 164, 114433.

[13] Kalús, D., & Gašparík, J. (2020). Comparison of VRF and traditional HVAC systems in Slovak office buildings. *Energy Efficiency*, 13(8), 1653-1668.

[14] EUROVENT. (2018). *VRF Units - Application Guide*. Brussels: EUROVENT Association.

[15] Mitsubishi Electric. (2021). *VRF Systems - Technical Manual*. Tokyo: Mitsubishi Electric Corporation.

[16] LG Electronics. (2020). *Multi V Water IV - Design Manual*. Seoul: LG Air Conditioning Technologies.

[17] Trane Technologies. (2019). *Variable Refrigerant Flow Systems - Engineering Manual*. Davidson: Trane.

[18] Raustad, R. (2013). A variable refrigerant flow heat pump computer model in EnergyPlus. *ASHRAE Transactions*, 119(1), 299-308.

[19] Yamamoto, M., Furuhashi, T., & Miyamoto, A. (2010). Development of multi-type air conditioner with CO₂ refrigerant. *International Journal of Refrigeration*, 33(7), 1378-1385.

[20] Xu, X., Xiao, F., & Wang, S. (2008). Enhanced chiller sensor fault detection, diagnosis and estimation using wavelet analysis and principal component analysis methods. *Applied Thermal Engineering*, 28(2-3), 226-237.

[21] European Commission. (2019). *Ecodesign and Energy Labelling of Air Conditioning Units*. Commission Regulation 2019/2068. Brussels: EC.

[22] Amarnath, A., & Blatt, M. (2008). Variable refrigerant flow: An emerging air conditioner and heat pump technology. *ACEEE Summer Study on Energy Efficiency in Buildings*, 2, 24-34.

[23] Hong, S. H., Gilbertson, J., Oreszczyn, T., Green, G., & Ridley, I. (2009). A field study of thermal comfort in low-income dwellings in England before and after energy efficient refurbishment. *Building and Environment*, 44(6), 1228-1236.

[24] Goetzler, W., Zogg, R., Young, J., & Johnson, C. (2014). *Energy Savings Potential and RD&D Opportunities for Commercial Building HVAC Systems*. Washington, DC: U.S. Department of Energy.

[25] Park, Y. C., Kim, Y., & Min, M. K. (2001). Performance analysis on a multi-type inverter air conditioner. *Energy Conversion and Management*, 42(13), 1607-1621.

[26] STN EN 12102. (2017). *Klimatizačné zariadenia - Chladiace jednotky kvapalinové a tepelné čerpadlá s elektrickými kompresormi - Určovanie hladiny akustického výkonu*. Bratislava: SÚTN.

[27] Carrier Corporation. (2020). *VRF Systems - Installation Manual*. Syracuse: Carrier Global Corporation.

[28] Johnson Controls. (2018). *VRF Technology - Design and Application Guide*. Milwaukee: Johnson Controls International.

[29] Panasonic Corporation. (2021). *ECOi Series - Technical Documentation*. Osaka: Panasonic Corporation.

[30] Ministerstvo dopravy a výstavby SR. (2023). *Analýza nákladov HVAC systémov v komerčných budovách*. Bratislava: MDV SR.

[31] Slovenská komora stavebných inžinierov. (2022). *Cenník stavebných prác 2022 - TZB*. Bratislava: SKSI.

[32] Združenie chladiacej a klimatizačnej techniky SR. (2023). *Správa o trhu HVAC technológií*. Bratislava: ZCHKT SR.

[33] Honeywell International. (2019). *Building Automation and VRF Integration*. Charlotte: Honeywell Building Technologies.

[34] REHVA. (2020). *VRF Systems - Application in European Buildings*. Brussels: Federation of European Heating, Ventilation and Air Conditioning Associations.

[35] SHMÚ. (2022). *Klimatické normály Slovenskej republiky 1991-2020*. Bratislava: Slovenský hydrometeorologický ústav.

[36] UNEP. (2021). *Montreal Protocol Technology and Economic Assessment Panel - Decision XXXI/3 Task Force Report*. Nairobi: United Nations Environment Programme.

[37] Lapin, M., Faško, P., & Melo, M. (2021). Climate change impacts on HVAC systems in Slovakia. *International Journal of Climatology*, 41(S1), E2847-E2865.

[38] STU Bratislava. (2023). *Výskum efektívnosti VRF systémov v podmienkach SR*. Bratislava: Fakulta stavebná STU.

[39] Kalús, D. (2019). *Energy performance of VRF systems in Slovak office buildings*. Dizertačná práca. Bratislava: STU.

[40] UNIZA. (2022). *Aplikácia VRF technológií v obchodných centrách*. Žilina: Univerzita v Žiline.

[41] Vysoká škola ekonomická v Bratislave. (2021). *Ekonomická analýza HVAC systémov v hotelových zariadeniach*. Bratislava: VŠE.

[42] TUKE Košice. (2020). *VRF systémy v bytových domoch - pilotný projekt*. Košice: Technická univerzita v Košiciach.

[43] SIEA. (2024). *Cenníky energeticky efektívnych technológií*. Bratislava: Slovenská inovačná a energetická agentúra.

[44] Slovenský zväz spotrebiteľov. (2023). *Analýza nákladov na chladenie domácností*. Bratislava: SZS.

[45] Ministerstvo životného prostredia SR. (2023). *Operačný program Slovensko - Opatrenia pre energetickú efektívnosť*. Bratislava: MŽP SR.

[46] STN EN 12831-1. (2017). *Systémy vykurovania v budovách - Metóda výpočtu tepelného výkonu - Časť 1: Tepelný výkon, Všeobecne*. Bratislava: SÚTN.

[47] EUROVENT. (2019). *VRF Performance Rating Standards*. Brussels: EUROVENT Association.

[48] STN EN ISO 3741. (2010). *Akustika - Určovanie hladín akustického výkonu a zvukovej energie zdrojov hluku pomocou akustického tlaku - Presné metódy pre komory s dozvukom*. Bratislava: SÚTN.

[49] ASHRAE. (2019). *Refrigerant Piping Design - Applications Manual*. Atlanta: ASHRAE.

[50] STN EN 15232-1. (2017). *Energetická efektívnosť budov - Vplyv automatizácie budov, regulácie a technického manažmentu budov*. Bratislava: SÚTN.

[51] ISO 16484-2. (2016). *Building automation and control systems (BACS) - Part 2: Hardware*. Geneva: International Organization for Standardization.

[52] Zhang, Y., Ma, Q., Li, B., Fan, X., & Fu, Z. (2018). Application of IoT technology in HVAC&R systems. *Energy Procedia*, 152, 1146-1151.