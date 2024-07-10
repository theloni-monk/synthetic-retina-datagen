from omni.replicator.core import BaseBackend
# ADAPTIVE SAMPLING POLICY
"""
This is a class that takes a function that must take image data and a camera pose and output a new 
"""

class AdaptiveSamplingPolicy(BaseBackend):
    def __init__(self) -> None:
        pass

    
# use backendgroup to send to both io thread and adaptivesamplerthread