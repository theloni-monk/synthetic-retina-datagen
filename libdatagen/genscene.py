import omni.replicator.core as rep

def loadscene_static(scene_fpath, scale = 1, semantics = None, randrot = False):
    # load usd scene and return the omniverse node
    scene = rep.create.from_usd(scene_fpath, semantics=semantics)
    with scene:
        rep.modify.pose(
                scale=1,
                rotation=rep.distribution.uniform((-90,-45, 0), (-90, 45, 0)) if randrot else None
            )
    return scene, lambda : -1

# returns a scene handle and the registered update scene func
def loadscene_randomized(assets_path, scale_ranges, semantics):
    # recursively crawl an asset folder and scatter the instances on a plane with randomly selected scale
    pass