from dataclasses import dataclass
import json


@dataclass
class SimulationConfig:
    dt: float
    total_time: float
    start_time: float
    starting_leaf_area: float
    nitrogen: float


@dataclass
class PhysiologyConfig:
    PR_base: float
    p: float
    r_leaf: float
    r_root: float
    r_shoot: float
    f_N_leaf: float
    beta: float
    rho: float


@dataclass
class NitrogenConfig:
    SNAR_max: float
    K_m: float


@dataclass
class PhotosynthesisConfig:
    a_PR: float
    b_PR: float
    N_max: float


@dataclass
class LightConfig:
    max_irradiance_area: float
    partial_shade_band_width: float


@dataclass
class LeafRootRatioConfig:
    LR_0: float
    a_LR: float
    b_LR: float
    adjustment_factor: float


@dataclass
class Config:
    simulation: SimulationConfig
    physiology: PhysiologyConfig
    nitrogen: NitrogenConfig
    photosynthesis: PhotosynthesisConfig
    light: LightConfig
    leaf_root_ratio: LeafRootRatioConfig

    @classmethod
    def from_json(cls, path: str) -> "Config":
        with open(path) as f:
            data = json.load(f)
        return cls(
            simulation=SimulationConfig(**data["simulation"]),
            physiology=PhysiologyConfig(**data["physiology"]),
            nitrogen=NitrogenConfig(**data["nitrogen"]),
            photosynthesis=PhotosynthesisConfig(**data["photosynthesis"]),
            light=LightConfig(**data["light"]),
            leaf_root_ratio=LeafRootRatioConfig(**data["leaf_root_ratio"]),
        )
