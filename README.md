# renderdoc-csv-to-obj
Python 3 RenderDoc CSV to Wavefront (OBJ) converter. Note that this was written for Vulkan models, but with some tweaking you can get this to read OpenGL and DirectX stuff as well.

## TO USE
``python3 renderdoc_csv_to_obj.py input.csv [input] [options]``  

Options are:  
* --mode {triangles,strips}: Draw mode for face generation.  
	* triangles: Assumes every 3 indices form a triangle (TRIANGLE_LIST).  
	* strips: Assumes overlapping triangles for strips (TRIANGLE_STRIP). Default is strips.  
* --flip-winding: Flips the winding order of faces (useful for Vulkan's front-face convention).  
  
Example (Vulkan):
``python3 renderdoc_csv_to_obj.py input.csv --mode strips --flip-winding``  
  
The output OBJ will have the same name as the input CSV.  