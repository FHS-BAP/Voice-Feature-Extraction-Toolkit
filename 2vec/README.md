# 2vec

## Prerequisites

Ensure you have the following installed:
    Docker Compose

## Step-by-Step Guide

### Step 1: Build the Containers

    Make the build script executable (if not already):

    ```sh
    chmod +x build.sh
    ```

    Run the build script:

    ```sh
    ./build.sh
    ```

    This script will start building the Docker containers required for the project.

### Step 2: Start the Containers with Docker Compose

    Start the containers in detached mode:

    ```sh
    docker-compose up -d
    ```

    This command uses Docker Compose to start all the containers defined in the `docker-compose.yml` file. Running in detached mode means the containers will run in the background.

### Step 3: Monitor and Check Outputs

    The containers will continue to run until they complete their tasks.
    Output files will be sent to the designated output folders as specified in the Docker compose.

### Additional Information

    If you need to stop the containers, you can use:

    ```sh
    docker-compose down
    ```

    Checking Logs: To view the logs of a specific container, you can use:

    ```sh
    docker-compose logs <container_name>
    ```

    Accessing Containers: To access a running container, use:

    ```sh
    docker exec -it <container_name> /bin/bash
    ```

## Acknowledgement
- [transformers](https://github.com/huggingface/transformers/tree/main): State-of-the-art Machine Learning for JAX, PyTorch and TensorFlow (License Apache)

## Citations
If you use this in your research, please cite this repo:
```bibtex
@misc{fhsbap2024vfet2vec,
  title={Voice-Feature-Extraction-Toolkit/2vec},
  author={Searls, Ned},
  journal={GitHub repository},
  year={2024},
  publisher={GitHub},
  howpublished = {\url{https://github.com/FHS-BAP/Voice-Feature-Extraction-Toolkit/tree/main/2vec}}
}
```
and these papers
```bibtex
@inproceedings{wolf-etal-2020-transformers,
    title = "Transformers: State-of-the-Art Natural Language Processing",
    author = "Thomas Wolf and Lysandre Debut and Victor Sanh and Julien Chaumond and Clement Delangue and Anthony Moi and Pierric Cistac and Tim Rault and Rémi Louf and Morgan Funtowicz and Joe Davison and Sam Shleifer and Patrick von Platen and Clara Ma and Yacine Jernite and Julien Plu and Canwen Xu and Teven Le Scao and Sylvain Gugger and Mariama Drame and Quentin Lhoest and Alexander M. Rush",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
    month = oct,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-demos.6",
    pages = "38--45"
}
```
```bibtex
@article{baevski2020wav2vec,
  title={wav2vec 2.0: A framework for self-supervised learning of speech representations},
  author={Baevski, Alexei and Zhou, Yuhao and Mohamed, Abdelrahman and Auli, Michael},
  journal={Advances in Neural Information Processing Systems},
  volume={33},
  pages={12449-12460},
  year={2020}
}
```
```bibtex
@article{baevski2022data2vec,
  title={data2vec: A General Framework for Self-supervised Learning in Speech, Vision and Language},
  author={Baevski, Alexei and Hsu, Wei-Ning and Xu, Qiantong and Babu, Arun and Gu, Jiatao and Auli, Michael},
  journal={arXiv preprint arXiv:2202.03555},
  year={2022}
}
```