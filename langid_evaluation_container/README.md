# Usage
1. Mount a writable volume to `/output`
2. Start the container
```bash
docker run <this container's image> model_id dataset_id (evaluate|report|both)
```
3. View prediction output and/or generated report in the volume mounted to `/output`