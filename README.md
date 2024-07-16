# synthetic-retina-datagen
Pipeline to generate synthetic data retina signals for training brain-like neural networks via nvidia omniverse replicator

## Library structure
 - renderplan.py
    - `RenderPlan` implements job process bringup and lifecycle management
 - genscene.py
    -  `loadscene_static` implements basic static usd scene loading
    - `loadscene_randomized` in the future will implement dynamic random scene generation 
        - in the further future will register animated agents for object-motion simulation
 - humancam.py
    - `HumanOcularSys` implements camera structure which mimics binocular vision and computes the transforms for the stero camera baseclass based on 12dof tracks
 - adaptivesampler.py
    - `AdaptiveSampleBackend` implements a backend which recieves data from the omniverse instance and then decides on the next location and pose of the camera
 - adaptivelearner.py
    - pipes adaptive sampler to learning process which chooses when to query for groundtruth

## Example Script
 ```python
def adaptivesample(rgb_img):
   return torch.rand(12) # next pose

plan = RenderPlan(1000, adaptivesample, "./static_scene.usdz", "./_output", shaders = ["retina.frag"], stream_viz = False)

plan.run()
 ```