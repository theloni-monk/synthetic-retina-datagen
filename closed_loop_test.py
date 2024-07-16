import asyncio
import logging
logger = logging.getLogger(__name__)

import numpy as np

from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": True})

import omni
import omni.kit.app
import omni.replicator.core as rep
from pxr import Usd, Sdf, UsdGeom

from libdatagen.renderplan import RenderPlan
from libdatagen.adaptivesampler import LookatWalkPolicy
from libdatagen.human import HumanOcularSys

# Remove the default light
default_light = rep.get.prims(path_pattern="/Environment/defaultLight")
with default_light:
    rep.modify.visibility(False)

# Create the lights
distance_light = rep.create.light(rotation=(400,-23,-94), intensity=10000, temperature=6500, light_type="distant")
cylinder_light = rep.create.light(position=(0,0,0),rotation=(0,-180,-180), light_type="disk")
# Create the environment
cone = rep.create.cone(position=(0,100,0), scale=2)
floor = rep.create.cube(position=(0,0,0), scale=(10,0.1,10))
wall1 = rep.create.cube(position=(-450,250,0), scale=(1,5,10))
wall2 = rep.create.cube(position=(0,250,-450), scale=(10,5,1))
#TODO: make scene more basic
#FIXME: load external scene, start with procedural scene
# scene = stage.Open("./assets/Forest_Scene.usda")

policy_params = {
    "annotators": ["rgb", "motion_vectors", "semantic_segmentation"],
    "outdir": "/isaac-sim/synthetic-retina-datagen/output",
    "walk_sigma": 0.005
}

osys = HumanOcularSys((1347.0,825.0,1440.0), (0.0, 0.0, 0.0), 0.1)
plan = RenderPlan((1920, 1080), osys,
                  lambda : -1, # no stage update function for now
                  LookatWalkPolicy, policy_params,
                  )

logging.warn("########## starting application - THELONI ###########")
plan.run(25)
logging.warn("########### Exiting application - THELONI ############")
plan.writer.write_walkpath()
simulation_app.close()