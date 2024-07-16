import abc
import numpy as np
from omni.replicator.core.writers_default import BasicWriter

class AdaptiveSamplingPolicy(BasicWriter):
    # asbtract adaptive sampling policy
    # __metaclass__ = abc.ABCMeta
    
    def __init__(self, posequeue, camstate, annotators, outdir):
        super().__init__(
            outdir, #FIXME: disk output directory not being written to
            **{anno: True for anno in annotators}
        ) # request all the annotators present in this init
        # self._output_dir = outdir
        self.pose_q = posequeue
        self.camstate = camstate
        self.dump2disk = False

    def activate_diskwriter(self):
        self.dump2disk = True

    def deactivate_diskwriter(self):
        self.dump2disk = False

    # @abc.abstractmethod
    def run_policy(self):
        """to be implemented in derived class, takes self.databuf and updates the self.camstate"""
        return

    def write(self, data):
        if self.dump2disk:
            super().write(data)
        # TODO: prevent data from leaving gpu, only send async cpu copy to disk
        self.databuf = data
        self.run_policy()
        self.pose_q.put(self.camstate)

# use backendgroup to send to both io thread and adaptivesamplerthread
class LookatWalkPolicy(AdaptiveSamplingPolicy):
    def __init__(self, posequeue, camstate, annotators, outdir, walk_sigma):
        super().__init__(posequeue, camstate, annotators,  outdir)
        self.sigma = walk_sigma
        self.walk_history = []

    def run_policy(self):
        delta = self.sigma * np.random.randn(3)
        self.camstate.look_at += delta
        self.walk_history.append(self.camstate.look_at)

    def write_walkpath(self):
        self.backend.write_blob(self._output_dir + "/walkpath.npy", np.vstack(self.walk_history).tobytes())