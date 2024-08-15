set -eu -o pipefail

operation="$1"
model_id="$2"
dataset_id="$3"
dataset_config_name="${4:-}"
dataset_split="${5:-}"

case "$operation" in
evaluate)
    python3 evaluate_using_mapping_scripts.py "$model_id" "$dataset_id" "$dataset_config_name" "$dataset_split"
    ;;
report)
    python3 create_excel_report_of_single_evaluation.py "$model_id" "$dataset_id"
    ;;
both)
    python3 evaluate_using_mapping_scripts.py "$model_id" "$dataset_id" "$dataset_config_name" "$dataset_split"
    python3 create_excel_report_of_single_evaluation.py "$model_id" "$dataset_id"
    ;;
esac