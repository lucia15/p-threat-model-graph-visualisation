## Steps to use Visjs in jupyter-notebook:

1. Install Anaconda

2. Download [vis.ja](https://github.com/almende/vis/archive/v4.19.1.zip) and unzip it in the desired location

3. Add the following line to *.jupyter/jupyter_notebook_config.py* 

```
    c.NotebookApp.extra_static_paths = ["/home/lucia/vis-4.19.1/dist"]
```

Replace the path with the path to the folder where you unziped vis.ja,
    
dist is the location of the distribution folder of vis.js libraries

4. Next time you start jupyter-notebook it should work

Further details in this 
[article](https://www.codementor.io/@isaib.cicourel/visjs-visualization-in-jupyter-notebook-phgb3fjv0) 