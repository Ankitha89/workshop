from backend.app.models.disaster import DisasterEvent, DisasterType, DisasterSeverity, DisasterStatus, GeoLocation, EnvironmentalImpact
from backend.app.models.resource import EmergencyResource, ResourceType, ResourceStatus

def get_initial_disasters() -> list[DisasterEvent]:
    return [
        DisasterEvent(
            id="DIS-001",
            title="Sierra Foothills Wildfire Complex",
            type=DisasterType.WILDFIRE,
            severity=DisasterSeverity.CRITICAL,
            status=DisasterStatus.ACTIVE,
            location=GeoLocation(
                latitude=38.5816,
                longitude=-121.4944,
                address="Placer & El Dorado Sector",
                region="Northern California"
            ),
            radius_km=28.5,
            risk_score=88.5,
            impact=EnvironmentalImpact(
                estimated_casualties_at_risk=4200,
                structures_threatened=650,
                air_quality_index=340.0,
                wind_speed_kmh=45.0
            ),
            required_capabilities=["aerial_firefighting", "ground_containment", "air_quality_monitoring", "mass_evacuation"],
            assigned_resources=[],
            notes=["High wind gusts spreading ember fronts northward toward suburban perimeters."]
        ),
        DisasterEvent(
            id="DIS-002",
            title="Cascadia Subduction Rift Tremor",
            type=DisasterType.EARTHQUAKE,
            severity=DisasterSeverity.CATASTROPHIC,
            status=DisasterStatus.ACTIVE,
            location=GeoLocation(
                latitude=45.5152,
                longitude=-122.6784,
                address="Willamette Valley Corridor",
                region="Oregon"
            ),
            radius_km=45.0,
            risk_score=94.2,
            impact=EnvironmentalImpact(
                estimated_casualties_at_risk=12500,
                structures_threatened=2100,
                seismic_magnitude=7.3
            ),
            required_capabilities=["urban_search_and_rescue", "emergency_triage", "structural_inspection", "heavy_lifting"],
            assigned_resources=[],
            notes=["Multiple bridge spans compromised; secondary gas leaks reported in commercial districts."]
        ),
        DisasterEvent(
            id="DIS-003",
            title="Gulf Coast Coastal Surge & Flash Flood",
            type=DisasterType.FLOOD,
            severity=DisasterSeverity.HIGH,
            status=DisasterStatus.ACTIVE,
            location=GeoLocation(
                latitude=29.7604,
                longitude=-95.3698,
                address="Bayou Watershed Lowlands",
                region="Texas Gulf Coast"
            ),
            radius_km=32.0,
            risk_score=76.8,
            impact=EnvironmentalImpact(
                estimated_casualties_at_risk=6800,
                structures_threatened=1400,
                flood_depth_meters=2.8,
                wind_speed_kmh=65.0
            ),
            required_capabilities=["swift_water_rescue", "amphibious_transport", "shelter_supply", "drone_surveillance"],
            assigned_resources=[],
            notes=["River levels exceeding 100-year crest; 3 levees at 92% capacity."]
        ),
        DisasterEvent(
            id="DIS-004",
            title="Industrial Chemical Pipeline Rupture",
            type=DisasterType.HAZMAT_SPILL,
            severity=DisasterSeverity.HIGH,
            status=DisasterStatus.ACTIVE,
            location=GeoLocation(
                latitude=41.8781,
                longitude=-87.6298,
                address="Industrial Sector 4 Freight Junction",
                region="Midwest Corridor"
            ),
            radius_km=12.0,
            risk_score=71.4,
            impact=EnvironmentalImpact(
                estimated_casualties_at_risk=2100,
                structures_threatened=320,
                radiation_or_ppm=185.0
            ),
            required_capabilities=["hazmat_containment", "air_purification", "decontamination_triage", "drone_gas_sensing"],
            assigned_resources=[],
            notes=["Chlorine vapor plume drifting southeast; 2 km evacuation zone enforced."]
        )
    ]

def get_initial_resources() -> list[EmergencyResource]:
    return [
        EmergencyResource(
            id="RES-101",
            name="Air-Crane Helitanker Helo-1",
            type=ResourceType.FIREFIGHTING,
            agency="CAL FIRE Tactical Air Support",
            status=ResourceStatus.AVAILABLE,
            location=GeoLocation(latitude=38.5200, longitude=-121.5000, region="Sacramento Base"),
            speed_kmh=180.0,
            capacity_units=3000,
            available_units=3000,
            capabilities=["aerial_firefighting", "thermal_imaging", "water_drop"],
            fuel_or_battery_pct=95.0
        ),
        EmergencyResource(
            id="RES-102",
            name="Strike Team Alpha Hotshots",
            type=ResourceType.FIREFIGHTING,
            agency="US Forest Service",
            status=ResourceStatus.AVAILABLE,
            location=GeoLocation(latitude=38.6500, longitude=-121.3000, region="Auburn Station"),
            speed_kmh=65.0,
            capacity_units=40,
            available_units=40,
            capabilities=["ground_containment", "fireline_construction", "brush_clearing"],
            fuel_or_battery_pct=100.0
        ),
        EmergencyResource(
            id="RES-201",
            name="Urban USAR Task Force 1",
            type=ResourceType.SEARCH_AND_RESCUE,
            agency="FEMA National Urban Search",
            status=ResourceStatus.AVAILABLE,
            location=GeoLocation(latitude=45.5400, longitude=-122.6500, region="Portland Depot"),
            speed_kmh=75.0,
            capacity_units=80,
            available_units=80,
            capabilities=["urban_search_and_rescue", "canine_detection", "structural_inspection", "heavy_lifting"],
            fuel_or_battery_pct=90.0
        ),
        EmergencyResource(
            id="RES-202",
            name="Mobile Trauma Hospital Unit MTH-4",
            type=ResourceType.MEDICAL_EVAC,
            agency="Disaster Medical Assistance Team (DMAT)",
            status=ResourceStatus.AVAILABLE,
            location=GeoLocation(latitude=45.4800, longitude=-122.7000, region="Beaverton Base"),
            speed_kmh=55.0,
            capacity_units=150,
            available_units=150,
            capabilities=["emergency_triage", "advanced_surgical_care", "mass_casualty_intake"],
            fuel_or_battery_pct=88.0
        ),
        EmergencyResource(
            id="RES-301",
            name="Swiftwater Flotilla Unit 9",
            type=ResourceType.WATER_RESCUE,
            agency="State Coast Guard Auxiliary",
            status=ResourceStatus.AVAILABLE,
            location=GeoLocation(latitude=29.7200, longitude=-95.3200, region="Houston Port Depot"),
            speed_kmh=45.0,
            capacity_units=200,
            available_units=200,
            capabilities=["swift_water_rescue", "amphibious_transport", "flood_evacuation"],
            fuel_or_battery_pct=92.0
        ),
        EmergencyResource(
            id="RES-302",
            name="Autonomous Recon Swarm 'AeroSentinel'",
            type=ResourceType.AIRBORNE_DRONE,
            agency="Civil Emergency Drone Corps",
            status=ResourceStatus.AVAILABLE,
            location=GeoLocation(latitude=29.7800, longitude=-95.4000, region="Houston Heights Base"),
            speed_kmh=110.0,
            capacity_units=12,
            available_units=12,
            capabilities=["drone_surveillance", "thermal_mapping", "network_mesh_relay", "air_quality_monitoring"],
            fuel_or_battery_pct=96.0
        ),
        EmergencyResource(
            id="RES-401",
            name="HAZMAT Containment Task Force 5",
            type=ResourceType.HAZMAT_CONTAINMENT,
            agency="Environmental Emergency Rapid Response",
            status=ResourceStatus.AVAILABLE,
            location=GeoLocation(latitude=41.8500, longitude=-87.6500, region="Chicago South Depot"),
            speed_kmh=60.0,
            capacity_units=50,
            available_units=50,
            capabilities=["hazmat_containment", "air_purification", "chemical_neutralization", "decontamination_triage"],
            fuel_or_battery_pct=85.0
        ),
        EmergencyResource(
            id="RES-501",
            name="Emergency Shelter & Logistics Carrier",
            type=ResourceType.SHELTER_SUPPLY,
            agency="American Red Cross Logistics",
            status=ResourceStatus.AVAILABLE,
            location=GeoLocation(latitude=38.6000, longitude=-121.4000, region="Central Valley Hub"),
            speed_kmh=70.0,
            capacity_units=500,
            available_units=500,
            capabilities=["shelter_supply", "clean_water_distribution", "mass_evacuation", "rations"],
            fuel_or_battery_pct=98.0
        )
    ]
