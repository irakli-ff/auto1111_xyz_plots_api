# auto1111_xyz_plots_api
generate a bunch of comparison grids using Automatic1111 API with custom parameters for each grid

Decide where to set up this script and go to that folder. Then run the following commands:

Clone our script by running the following: 

git clone https://github.com/irakli-ff/auto1111_xyz_plots_api.git

That will create a folder called auto1111_xyz_plots_api. go there by:

cd auto1111_xyz_plots_api

Install requirements:

pip install -r requirements.txt

Prepare the inputs file

In the cloned folder, you will have the inputs.csv file. That files will contain all the details about your generation, and thus that’s what you have to modify to define prompts, negative prompts, checkpoints you will be testing, and so on.

You can edit the CSV file with whatever tool (excel, code editor, etc.) you like. In our case, we used Google Sheets for collaborative reasons and are providing the exact template for you. (link).

How to edit it:

Column 1 is Test Name: this doesn’t impact the generation, but this is how your files will be named. Use something intuitive to recall what you generated.

Column 2: prompt. No explanation is needed.

Column 3: negative prompt. You can leave it empty or enter the desired prompt. You can also do the same prompts across different rows and slowly modify negative prompts to watch how it evolves your images

Column 4: Sampler. No explanation is needed, but be careful, as some are slower than others and can greatly impact the overall generation.

Column 5: steps. number of steps for each generation. This can impact the overall time required quite significantly.

Column 6: checkpoints. This will be your Y-axis in the generation. Follow the formatting in the provided template. It’s a comma and space-separated list of checkpoint names. Names include extensions but no hashes. Note that all these checkpoints must exist in your Auto1111 installation. Our example:

'5_vokda_v2_mix.safetensors, neverendingDream.safetensors, dreamshaper_6.safetensors, CounterfeitV30.safetensors, epicrealism_newEra.safetensors, rpg_V4.safetensors'

Column 7: seeds. This will be your X-axis in the generation. Seed numbers - you need at least one and can have as many as possible. Please note that we haven’t tested the -1 value, so be careful.

Column 8: cfg values. Similar to seeds, you will need at least one value. This is used as a Z axis for the generation.

Once done, save the file as “inputs.csv” in our installation folder. 

If you use Google Sheets, copy our template to your drive, edit it, and press File→Download→Comma-separated values (.csv). Rename the downloaded file to inputs.csv and place it in the installation folder.

Launch the Process

Now we are ready to launch everything, sit back, and save some time:

Launch Automatic1111 with API enabled. In our case:

python launch.py --xformers --api

Navigate to the folder where you have the script installed and launch the following command (with cmd, WSL, or whatever you use):

python api_tester.py

If all goes well, your generation will start, and output grids will be individually added to the output folder.

Note that there is the Jupyter Notebook version inside in case you can and prefer to run the script that way
