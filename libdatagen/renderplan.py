import omni.replicator.core as rep


class RenderPlan:
# class implements the multi-process spinup for an adaptive sampling render job

    def __init__(self, n_frames, decision_func, outputdir) -> None:
        pass
        # init camera
        # init sampler backend with decision func
        # init diskbackend with the outputdir
    
    def run():
        # wait for textures to fully load
        # loop:
            # step frame
            # dispatch to backendgroup
            # custom - adaptivesample backend sends back a new camera pose via a queue
            # diskbackend sends writes to io thread queue which then sends data to disk
            # custom - vizbackend sends rgb data to socket which can be read on a client to monitor the adaptive sampler
        pass