# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sumo_docker_pipeline']

package_data = \
{'': ['*']}

install_requires = \
['bs4', 'docker', 'lxml', 'pandas']

setup_kwargs = {
    'name': 'sumo-docker-pipeline',
    'version': '1.6',
    'description': 'A pipeline to call a traffic simulator: SUMO',
    'long_description': '# sumo_docker_pipeline\n- - -\n\nThe package `sumo_docker_pipeline` enables you to run a traffic simulator [SUMO](https://sumo.dlr.de/docs/index.html) efficiently \nand to interact with Python easily. \nThe package is valid when you need to run SUMO iteratively.\n\nSUMO is often tricky to install locally because of its dependencies. \nThus, it\'s a straightforward idea to run SUMO in a docker container.\n\nHowever, another issue arises when we run SUMO in a docker container. \nIt is challenging to construct a pipeline between SUMO and API.\n\nThe package provides an easy-to-use API; \nat the same time, \nSUMO runs in a docker container.\n\n# Requirement\n\n- python > 3.5\n- docker \n- docker-compose\n\n# Install\n\n## Pull the image (or build of a docker image with SUMO)\n\nThe existing image is on the [Dockerhub](https://hub.docker.com/repository/docker/kensukemi/sumo-ubuntu18).\n\n```shell\ndocker pull kensukemi/sumo-ubuntu18\n```\n\nIf you prefer to build with yourself, you run the following command.\n\n```shell\ndocker-compose build \n```\n\n## Install a python package\n\n```shell\nmake install\n```\n\n# Example case: iterative run with parameter updates\n\nLet\'s say that you want to run SUMO iteratively.\nAt the same time, you want to change input parameters depending on the results of a simulation. \n\nIn that case, you need to check the output of SUMO and update the parameters.\n`sumo_docker_pipeline` package enables you to make the process automatic.\n\n[![](https://user-images.githubusercontent.com/1772712/119264146-34563500-bbe2-11eb-9288-2e4e841ff803.png)]()\n\n## Setups\n\n1. creation of a directory where you save SUMO\'s configuration.\n2. creation of template-files of SUMO\'s configuration.\n3. running the pipeline.\n\n## 1. creation of a directory\n\nIt is a directory that SUMO accesses.\nLet\'s say that we create `test/resources/config_template`\n\n## 2. creation of SUMO\'s configuration\n\nYou prepare configuration files which SUMO requires.\nThe format of the conf. files are totally same as SUMO\'s requirements.\n\nThe only difference is that you write wildcard `?` at the place where you wanna replace during pipeline.\n\nFor example, `tests/resources/config_template/grid.flows.xml` has the following element,\n\n```xml\n<vType vClass="passenger" id="passenger"  tau="0.5" speedDev="0.1" maxSpeed="?" minGap="?" accel="?" decel="?" latAlignment="center" />\n```\n\nWith the `sumo_docker_pipeline` package, you can replace the attributes with the wildcards `?`.\n\n## 3. running the pipeline\n\n```python\nfrom sumo_docker_pipeline import DockerPipeline\nfrom pathlib import Path\n# values to replace the wildcard in the template files.\nvalues_target = {\n    # a file-name to update\n    \'grid.flows.xml\': {\n        # a XPath to update\n        \'/routes/flows/vType[1]\': {\n            # key and value to update\n            \'maxSpeed\': 15,\n            \'minGap\': 1.0,\n            \'accel\': 10,\n            \'decel\': 5\n        },\n        \'/routes/flows/vType[2]\': {\n            \'maxSpeed\': 10,\n            \'minGap\': 0.5,\n            \'accel\': 5,\n            \'decel\': 5\n        }\n    }\n}\n# execution of SUMO in a docker container\npipeline_obj = DockerPipeline(\n    path_config_file=Path(\'[a path to sumo.cfg]\'),\n    scenario_name=\'test-scenario\')\nresult_obj = pipeline_obj.run_simulation(values_target)\n```\n\n# Example\n\nSee `examples` directory.\n\n# For developer\n\n```shell\npytest tests\n```\n\n# license and credit\n\nThe source code is licensed MIT. The website content is licensed CC BY 4.0.\n\n\n```\n@misc{sumo-docker-pipeline,\n  author = {Kensuke Mitsuzawa},\n  title = {sumo-docker-pipeline},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/Kensuke-Mitsuzawa/sumo_docker_pipeline}},\n}\n```',
    'author': 'Kensuke Mitsuzawa',
    'author_email': 'kensuke.mit@gmail.com',
    'maintainer': 'Kensuke Mitsuzawa',
    'maintainer_email': 'kensuke.mit@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
