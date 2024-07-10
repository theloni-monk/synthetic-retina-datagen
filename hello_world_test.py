import omni.graph.core as og
import omni.replicator.core as rep

camera_pos = [(0, 10, 50),(10, 50, 50),(-50, 10, 50),]

with rep.new_layer():

    # Add Default Light
    distance_light = rep.create.light(rotation=(315,0,0), intensity=3000, light_type="distant")

    stereo_camera_pair = rep.create.stereo_camera(
        stereo_baseline=10,
        position=camera_pos[0],
        look_at=(0,0,0),
        # focus_distance=rep.distribution.normal(400.0, 100),
        # f_stop=1.8
    )
    # create a plane to sample on
    plane_samp = rep.create.plane(scale=1)#, rotation=(20, 0, 0))

    # def randomize_spheres():
    #     # create small spheres to sample inside the plane
    #     spheres = rep.create.sphere(scale=0.4, count=30)

    #     # randomize
    #     with spheres:
    #         rep.randomizer.scatter_2d(plane_samp, check_for_collisions=True)
    #         # Add color to small spheres
    #         rep.randomizer.color(colors=rep.distribution.uniform((0.2, 0.2, 0.2), (1, 1, 1)))
    #     return spheres.node

    # rep.randomizer.register(randomize_spheres)
    def forest():
        forest = rep.create.from_usd('/home/ubuntu/synthetic-retina-datagen/assets/Forest_Scene.usda', semantics=[('class', 'forest')])

        with forest:
            rep.modify.pose(
                scale=10,
                rotation=rep.distribution.uniform((-90,-45, 0), (-90, 45, 0)),
            )
        return forest

    rep.randomizer.register(forest)
    
    # Will render 512x512 images and 320x240 images
    render_product = rep.create.render_product(stereo_camera_pair, resolution=(1024, 1024))
    # render_product2 = rep.create.render_product(camera2, (320, 240))

    basic_writer = rep.WriterRegistry.get("BasicWriter")
    basic_writer.initialize(
        output_dir=f"/home/ubuntu/synthetic-retina-datagen/output",
        rgb=True,
        # bounding_box_2d_loose=True,
        # bounding_box_2d_tight=True,
        # bounding_box_3d=True,
        # distance_to_camera=True,
        # colorize_depth=True,
        # distance_to_image_plane=True,
        # instance_segmentation=True,
        # normals=True,
        semantic_segmentation=True,
    )
    # Attach render_product to the writer
    basic_writer.attach(render_product)

    with rep.trigger.on_frame(num_frames=3):
        # rep.randomizer.randomize_spheres()
        rep.randomizer.forest()
        with stereo_camera_pair:
            rep.modify.pose(look_at=(0,0,0), position=rep.distribution.sequence(camera_pos))


# Run the simulation graph
rep.orchestrator.run()
