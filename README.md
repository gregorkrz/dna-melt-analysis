## DNA-melt-analysis


### Introduction

This software helps to automate analysis of UV melting curves. It currently has the following functionalities:
* Easy pooling of data from different files and querying data by name
* Automatic or manual baseline correction
* Primer melting temperature (Tm) determination
* Rendering of Absorbance and Fraction Folded plots, with custom experiment labels, colors and markers
* Export to Excel workbook

### Setup

`pip3 install -r requirements.txt`

#### Data

The csv data should be in the following format:

```
Sample1Name,,Sample2Name,,Sample3Name,
Temperature,Abs,Temperature,Abs,Temperature,Abs
10.0,0.45,10.0,0.55,10.0,0.45
...
```

See example data.


#### How to run

The following command will run the example configuration:
`python3 src/main.py config.txt.example`

When prompted (e. g. when a plotting operation was selected) to select experiments, a list of experiments prefixed with their IDs will appear. The following select queries are supported:
* comma separated list of experiment IDs to plot
* an ID range to plot, e. g. `0-5`
* searching by experiment name: query `f=text1,text2` will select all experiments that contain string `text1` AND string `text2`
