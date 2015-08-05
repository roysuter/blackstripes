Blackstripes
============

Blackstripes drawing machines. MK1 v-plotter design, MK2 kinematic-arms design.

MK1: http://www.youtube.com/watch?v=Od8OGbsfzPY

MK2: http://www.youtube.com/watch?v=u11jDH18Qqw

The machines are driven by a Raspberry-Pi running xenomai based rt-linux. We used this pre build image : http://wiki.linuxcnc.org/cgi-bin/wiki.pl?RaspbianXenomaiBuild

Read more here: http://www.blackstripes.nl/?cat=3


There you will find any info/sourcecode you possibly need to build and run these drawing bots yourself.

Clone this url: https://github.com/fullscreennl/blackstripes.git into your desktop (or anywhere else) and you are ready. You need Python version 2.6/2.7 with a working python imaging library installed and additonally NumPy for the Mk2 software to get rolling.

Scripts to run from the command line:
 Mk1 :

bash$ python generate_mk1_drawing.py testies_210_180_120_50.png

This command should generate a folder called generated_data in ‘macine_motion’ and a subdir called ‘filename – level info‘. This folder contains previews of the drawing paths of the machine. The numbers in the filename represent  ‘quantization tresholds’ of the input image grayscale values. The script is also automagically trying to upload the machine data to the raspberry pi that is supposed to drive the machine.

Mk2 :

cd into ‘image_input’ folder first and create a dir named input. Put a preferably square jpg or png file inside it from around 1000 x 1000 px. Run the following command
 bash$ python generate_input_image.py

This will convert any png or jpg inside the input folder and writes output to a new output folder. The output consists of a custom made binary image file (.bsi for the machine/simulator) and a preview image. You are able to encode the levels in the filename of the image by creating a name in this fashion: 180_150_103_73_43_13_.png
 The simpulator.py file creates a really nice high res preview of the machine output, the final line in the module should reald something like this:
Simulator(“spiral.bin”,”../image_input/output/photo.bsi”,8239711)
 where the first argument is the motion data to use (this motionpath data generation code is also included), the second argument is the blaskstripes image to simulate (we created this in the previous python command). The third argument is a total number of instructions this is a prop to give some feedback of the simulation progress in the terminal whilst processing. To run the simulator, run this command in blackstripesMK2/machine_motion:

bash$ python simulator.py
If that worked you should see the progress starting to increase.


