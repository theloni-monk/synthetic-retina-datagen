from multiprocessing import Queue
import logging

import numpy as np
import omni
import omni.replicator.core as rep

from .human import HumanOcularSys

class RenderPlan:
# class implements the spinup for an adaptive sampling render job

    #TODO: support hooking arbitrary event hooks into policy
    def __init__(self, resolution, ocsys, randomize_scene, policy, policy_params):
        self._pose_q = Queue()

        self.ocsys = ocsys
        self.render_product = rep.create.render_product(self.ocsys.vcam, resolution=resolution)

        self.writer = policy(self._pose_q, self.ocsys.state, **policy_params)
        self.writer.attach([self.render_product])
        
        rep.orchestrator.set_capture_on_play(False)

        self.randomize = randomize_scene
    
    #TODO: support async physx scene stepping
    def run(self, n_frames):
         # randomize the scene
        self.randomize()
        
        logger = logging.getLogger(__name__)
        logger.warn(f"########## Loading Assets - THELONI ###########")
        self.writer.deactivate_diskwriter()            
        # Run a few updates without rendering to make sure all materials are fully loaded for capture
        for _ in range(5):
            rep.orchestrator.preview()
        self.writer.activate_diskwriter()

        for frame in range(n_frames):
            logger.warn(f"########## Stepping through frame {frame} of {n_frames} - THELONI ###########") 
            if not self._pose_q.empty():
                pq = self._pose_q.get()
                logger.warn(f"######## popped {pq} - THELONI #############")
                self.ocsys.update_state(pq)
            rep.orchestrator.step()
        rep.orchestrator.wait_until_complete()