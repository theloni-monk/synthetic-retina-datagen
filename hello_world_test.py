"""Launch Isaac Sim Simulator first."""

from omni.isaac.lab.app import AppLauncher

# launch omniverse app
app_launcher = AppLauncher(headless=False)
simulation_app = app_launcher.app


"""Rest everything follows."""

from omni.isaac.lab.sim import SimulationContext

if __name__ == "__main__":
   # get simulation context
   simulation_context = SimulationContext()
   # reset and play simulation
   simulation_context.reset()
   # step simulation
   simulation_context.step()
   # stop simulation
   simulation_context.stop()

   # close the simulation
   simulation_app.close()