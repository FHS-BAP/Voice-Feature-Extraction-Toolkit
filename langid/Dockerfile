FROM python:3.10.12-slim-bullseye

WORKDIR /app/

COPY src/. /app/

# TODO: Verify cache directory
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt --mount=type=cache,target=/root/.cache pip install -r /tmp/requirements.txt

# Could replace with Bash brace expansion if sh replaced with Bash
RUN for script in mapping_scripts/datasets/*/*/make_id_mappings.py; do python3 "$script"; done
RUN for script in mapping_scripts/models/*/*/make_id_mappings.py; do python3 "$script"; done
# Fix permissions in repo to remove this line
RUN chmod u+x /app/run.sh

ENTRYPOINT ["/app/run.sh"]