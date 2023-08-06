# partialedge

This library contains algorithms for solving **Maximum Ink Partial Edge Drawing** problems, MaxPED, MaxSPED and MaxSHPED in particular.
The implementation is based on the algorithms presented in the publication from Hummel et al<sup>[1]</sup> while using the htd<sup>[2]</sup> library from Michael Abseher for tree decomposition.

The CrossingResolution algorithm solves MaxSHPED, while the Tree algorithm can solve MaxSPED where the intersection graph forms a tree.
The TreeDecomposition algorithm is applicable to either MaxPED or MaxSPED with no restriction on the intersection graph.
However, depending on the treewidth of the tree decomposition, the execution may require too much runtime or memory space.


Source | PED | SPED | SHPED
:-----:|:---:|:----:|:-----:
![source](https://bitbucket.org/Remvipomed/partialedgedrawing/raw/master/img/source.png) | ![ped](https://bitbucket.org/Remvipomed/partialedgedrawing/raw/master/img/ped.png) | ![sped](https://bitbucket.org/Remvipomed/partialedgedrawing/raw/master/img/sped.png) | ![shped](https://bitbucket.org/Remvipomed/partialedgedrawing/raw/master/img/shped.png)


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install partialedge.

```bash
pip install partialedge
```

## Usage

### Command Line

```bash
python -m partialedge
```

```
positional arguments:
  input                 path to input file or directory depending on mode

optional arguments:
  -h, --help            show this help message and exit
  --mode {single,set,dir}
                        process a single input file, a file containing a set
                        of graph drawings, or a directory of set files
  --symmetric           input will be processed as symmetric PED problem
  --homogeneous         input will be processed as homogeneous PED problem
  --json JSON_DIR, -j JSON_DIR
                        store result data at the given directory
  --image IMAGE_DIR, -i IMAGE_DIR
                        store result image at the given directory
  --include-source, -s  store source graph image with the result image
  --verbose, -v         v count determines logging verbosity level
```


### Development

```python
import logging

from partialedge.graph import graph_window as gw
from partialedge.algorithm import ped_algorithm as alg

logger = logging.getLogger("ped")
logger.setLevel(logging.INFO - 3)

# all high-level features are exposed via an algorithm object
# the positional parameter determines output filenames
# algorithm classes: TreeDecompositionAlgorithm, TreeAlgorithm, CrossingResolutionAlgorithm
algorithm = alg.TreeDecompositionAlgorithm("sample", symmetric=False, logger=logger)

# either create a random graph layout or load an existing one
algorithm.create_graph(15, 20, layout="spring")
# algorithm.load_graph_from_graph_file(file_path="resources/sample/json/source/sample.json")

# start execution
algorithm.perform_algorithm()

# export source and output
algorithm.export_source_graph(dir_path="resources/sample/json/source")
algorithm.export_json_result(dir_path="resources/sample/json/result")
algorithm.export_image_source(dir_path="resources/sample/image/source")
algorithm.export_image_result(dir_path="resources/sample/image/result")

# create plot of source graph
algorithm.set_edges_full()
source = gw.GraphWindow()
source.draw_graph(algorithm.graph)

# create plot of result graph
algorithm.set_edges_partial()
result = gw.GraphWindow()
result.draw_graph(algorithm.graph)

# show matplotlib plots
source.show()

# close matplotlib resources
source.close()
result.close()
```


## File Format

### Input

The input file for a single graph must be in the same format as the example below.
In set mode the json file has to contain a list of named single graphs.
The directory mode requires the path to a directory with set files as input.

```json
{
    "edges": [
        {
            "incident_nodes": [
                0,
                1
            ]
        }
    ],
    "nodes": [
        {
            "coordinates": [
                0.2215272649584424,
                -1.0
            ],
            "index": 0
        },
        {
            "coordinates": [
                -0.2215272649584424,
                1.0
            ],
            "index": 1
        }
    ]
}
```


### Output

The json result file contains a lot of information that can be used for statistical analysis.
In the *graph* field, the number of nodes and edges as well as the ink value is stored, in addition to the full drawing of the source graph.
As it has a large impact on runtime and memory consumption, the intersection graph with details about its size and the number of crossings per node is stored in the *intersection* field.
The *result* field contains all stub values of the maximum ink partial edge drawing in relation to edges of the input graph drawing.
It also stores meta data consisting of the resulting ink value, treewidth of the tree decomposition on the intersection graph, and a boolean about whether the problem had the symmetric constraint.
The *success* field on the highest level is true, if execution of the algorithm completed uninterrupted, and the *time* field contains the runtime in seconds.


```json
{
    "graph": {
        "edge_data": {
            "edge_count": 1,
            "edges": [
                {
                    "incident_nodes": [
                        0,
                        1
                    ]
                }
            ]
        },
        "ink": 2.048486591725675,
        "node_data": {
            "node_count": 2,
            "nodes": [
                {
                    "coordinates": [
                        0.2215272649584424,
                        -1.0
                    ],
                    "index": 0
                },
                {
                    "coordinates": [
                        -0.2215272649584424,
                        1.0
                    ],
                    "index": 1
                }
            ]
        }
    },
    "intersection": {
        "delta_count": {
            "0": 1
        },
        "edge_count": 0,
        "edges": [],
        "node_count": 1,
        "nodes": [
            {
                "delta": 0,
                "index": 0
            }
        ]
    },
    "result": {
        "edges": [
            {
                "incident_nodes": [
                    0,
                    1
                ],
                "stub": [
                    0.5,
                    0.5
                ]
            }
        ],
        "ink": 2.048486591725675,
        "symmetric": false,
        "tree_width": 0
    },
    "success": true,
    "time": {
        "algorithm": 0.00013890000000049696,
        "init_datastructure": 9.380000000014377e-05,
        "tree_decomposition": 0.12066659999999985
    }
}
```


## Contributing

No major updates are planned at the moment. 
Anyone willing to contribute is welcome to create bug reports and pull requests at the [project page](https://bitbucket.org/Remvipomed/partialedgedrawing/src/master/)


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Citations

1. [Maximizing Ink in Partial Edge Drawings of k-plane Graphs](https://doi.org/10.1007/978-3-030-35802-0_25)
2. [htd](https://github.com/mabseher/htd)
