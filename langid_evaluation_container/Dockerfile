FROM python:3.9

WORKDIR /app/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run.sh /app/
COPY src/ /app/

RUN for script in mapping_scripts/{datasets,models}/*/*/make_id_mappings.py; do python3 $script; done

ENTRYPOINT ["python3", "evaluate_using_mapping_scripts.py"]