model_id="$1"
dataset_id="$2"
operation="$3"

case "$operation" in
evaluate)
    python3 evaluate_using_mapping_scripts.py "$model_id" "$dataset_id"
    ;;
report)
    python3 evaluate_using_mapping_scripts.py "$model_id" "$dataset_id"
    ;;
both)
    python3 evaluate_using_mapping_scripts.py "$model_id" "$dataset_id"
    python3 create_excel_report_of_single_evaluation.py "$model_id" "$dataset_id"
    ;;
