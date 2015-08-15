
import simulator


print "dies sollte  SIMULATOR for rolf.jpg starten"
# run() is  for the real simulated output with all printer paths visialized in light magenta, saved in rolf_realoutput.png

# simulate() is generating layer previels in rolf_sep_0.png and rolf_poster.png



simulator.SimuDriver("generated_data/rolf/rolf").simulate()
simulator.SimuDriver("generated_data/rolf/rolf").run()
