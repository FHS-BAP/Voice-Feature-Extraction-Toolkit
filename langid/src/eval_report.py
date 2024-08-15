import json
from pathlib import Path
from dataclasses import dataclass

import sklearn
import numpy as np
import matplotlib.pyplot as plt

import global_id_utils

@dataclass
class DatasetConfig:
  dataset_id: str
  dataset_config: str
  dataset_split: str
  dataset_load_command: str

def make_evaluation_outputs(prediction_output, output_dir: Path, model_id_to_global_id: dict, model_id2label: dict, dataset_id_to_global_id: dict, model_id: str, dataset_config: DatasetConfig, comments: str):
    """
    Runs all evaluations on the model's predictions, saving output in output_dir.
    Evaluations are:
        - Classification report for accuracy, recacll, f1 across all true classes
        - Accuracy bar plot across true classes
        - Confusion Matrices (Counts, normalized over true)
    """
    prediction_model_ids = np.argmax(prediction_output.predictions, axis=-1)
    label_model_ids = prediction_output.label_ids

    prediction_global_ids = [model_id_to_global_id[id] for id in prediction_model_ids]
    label_global_ids = [model_id_to_global_id[id] for id in label_model_ids]

    def model_id_to_global_name(model_id):
        global_id = model_id_to_global_id[model_id]
        lang = global_id_utils.global_id_to_lang(global_id)
        name = lang.name
        return name

    unique_prediction_model_ids, unique_prediction_names = unique_ids_and_names_func(prediction_model_ids, model_id_to_global_name)
    unique_label_model_ids, unique_label_names = unique_ids_and_names_func(label_model_ids, model_id_to_global_name)

    _, report_text = save_report(output_dir, prediction_model_ids, label_model_ids, unique_label_model_ids, unique_label_names)
    print(report_text)

    all_unique_ids = np.unique(np.concatenate((label_model_ids, prediction_model_ids)))
    all_unique_names = list(map(model_id_to_global_name, all_unique_ids))

    create_and_save_visualizations(output_dir, prediction_model_ids, label_model_ids, all_unique_ids, all_unique_names)

    save_predictions(output_dir, prediction_model_ids, label_model_ids, prediction_global_ids, label_global_ids)

    save_inference_metrics(output_dir, prediction_output)

    save_metadata(output_dir, dataset_config, model_id, comments)

def unique_ids_and_names(ids: list[int], id_to_name):
    """
    Args:
        - ids: list/array of ids
        - id_to_name: Mapping of integer ids to string names
    """
    unique_ids = np.unique(ids)
    unique_names = [id_to_name[id] for id in unique_ids]
    
    return unique_ids, unique_names

def unique_ids_and_names_func(ids: list[int], id_to_name):
    """
    Args:
        - ids: list/array of ids
        - id_to_name: Function mapping of integer ids to string names
    """
    unique_ids = np.unique(ids)
    unique_names = list(map(id_to_name, unique_ids))
    
    return unique_ids, unique_names


def create_and_save_visualizations(output_dir: Path, prediction_model_ids, label_model_ids, all_unique_ids, all_unique_names):
    #################
    # Confusion matrix of counts
    #################

    cm = sklearn.metrics.confusion_matrix(
        y_true=label_model_ids,
        y_pred=prediction_model_ids,
        labels=all_unique_ids,
    )
    disp = sklearn.metrics.ConfusionMatrixDisplay(confusion_matrix=cm,
                                                  display_labels=all_unique_names)

    counts_cm_fig, counts_cm_ax = plt.subplots(figsize=(10,10))

    disp.plot(ax=counts_cm_ax)
    counts_cm_ax.set_title("Confusion Matrix (counts)")
    counts_cm_ax.tick_params(axis="x", labelrotation=90)

    # Prevent labels from getting cut off when saving image
    counts_cm_fig.tight_layout()
    counts_cm_fig.savefig(output_dir / "confusion matrix.png")
    counts_cm_fig.savefig(output_dir / "confusion matrix.svg")
    counts_cm_fig.show()
    
    # TPR of languages evaluated (only languages in the true labels)
    true_positive_rate = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    true_positive_rate = true_positive_rate.diagonal()

    not_nans = ~np.isnan(true_positive_rate)
    true_positive_rate = true_positive_rate[not_nans]
    labels = np.array(all_unique_names)[not_nans]

    true_positive_rate_fig, true_positive_rate_ax = plt.subplots()

    true_positive_rate_ax.bar(np.arange(len(true_positive_rate)), true_positive_rate, label=labels)
    true_positive_rate_ax.set_title("true_positive_rate per language")
    true_positive_rate_ax.set_ylabel("true_positive_rate")
    true_positive_rate_ax.set_xlabel("Language")
    true_positive_rate_ax.set_yticks(np.linspace(0, 1, num=6))
    true_positive_rate_ax.set_xticks(np.arange(len(true_positive_rate)), labels, rotation=45, horizontalalignment="right")
    # Prevent labels from getting cut off when saving image
    true_positive_rate_fig.tight_layout()

    true_positive_rate_fig.savefig(output_dir / "true_positive_rate bar plot.png")
    true_positive_rate_fig.savefig(output_dir / "true_positive_rate bar plot.svg")
    true_positive_rate_fig.show()
    
    #################
    # Confusion matrix normalized over true labels
    #################

    cm = sklearn.metrics.confusion_matrix(
        y_true=label_model_ids,
        y_pred=prediction_model_ids,
        labels=all_unique_ids,
        normalize="true",
    )
    disp = sklearn.metrics.ConfusionMatrixDisplay(confusion_matrix=cm,
                                                  display_labels=all_unique_names)

    fig, ax = plt.subplots(figsize=(15,15))
    ax.set_title("Confusion matrix (normalized over true rows)")

    disp.plot(ax=ax)
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment="right")
    ax.tick_params(axis="x", labelrotation=90)
    # Prevent labels from getting cut off when saving image
    fig.tight_layout()

    fig.savefig(output_dir / "confusion matrix normalized over true.png")
    fig.savefig(output_dir / "confusion matrix normalized over true.svg")
    fig.show()

    fig, ax = plt.subplots(figsize=(15,15))
    ax.set_title("Confusion matrix normalized over true labels")
    
    # Confusion matrix normalized over true labels (small font)

    sklearn.metrics.ConfusionMatrixDisplay.from_predictions(
        y_true=label_model_ids,
        y_pred=prediction_model_ids,
        labels=all_unique_ids,
        display_labels=all_unique_names,
        normalize="true",
        include_values=True,
        xticks_rotation="vertical",
        ax=ax,
        text_kw={"size": 6},
        values_format=".2g",
    )
    # Prevent labels from getting cut off when saving image
    fig.tight_layout()
    fig.savefig(output_dir / "confusion matrix normalized over true small font.png")
    fig.savefig(output_dir / "confusion matrix normalized over true small font.svg")
    fig.show()

    # Small confusion matrix
    fig, ax = plt.subplots(figsize=(5,5))
    ax.set_title("Confusion matrix (normalized over true)")
    sklearn.metrics.ConfusionMatrixDisplay.from_predictions(
        y_true=label_model_ids,
        y_pred=prediction_model_ids,
        labels=all_unique_ids,
        display_labels=all_unique_names,
        normalize="true",
        include_values=True,
        xticks_rotation="vertical",
        ax=ax,
        text_kw={"size": 6},
        values_format=".2g",
    )
    # Prevent labels from getting cut off when saving image
    fig.tight_layout()
    fig.savefig(output_dir / "confusion matrix normalized over true small font.png")
    fig.savefig(output_dir / "confusion matrix normalized over true small font.svg")
    fig.show()
    
def save_report(output_dir: Path, prediction_model_ids, label_model_ids, unique_label_ids, unique_label_names):
    classification_report_args = dict(
        y_true=label_model_ids,
        y_pred=prediction_model_ids,
        labels=unique_label_ids,
        target_names=unique_label_names,
        zero_division=0,
    )
    
    classification_report = sklearn.metrics.classification_report(**classification_report_args, output_dict=True)
    
    with open(output_dir / "classification_report.json", "w") as out_file:
        json.dump(classification_report, out_file)
    classification_report_text = sklearn.metrics.classification_report(**classification_report_args, output_dict=False)
    with open(output_dir / "classification_report.txt", "w") as out_file:
        out_file.write(classification_report_text)

    return classification_report, classification_report_text

def save_predictions(output_dir: Path, prediction_model_ids, label_model_ids, prediction_global_ids, label_global_ids):
    results = {
        "predictions": prediction_global_ids,
        "labels": label_global_ids
    }
    with open(output_dir / "predictions.json", "w") as out_file:
        json.dump(results, out_file)

    predictions_readable = [global_id_utils.global_id_to_iso639_part3(id) for id in prediction_global_ids]
    labels_readable = [global_id_utils.global_id_to_iso639_part3(id) for id in label_global_ids]
    results_readable = {
        "predictions": predictions_readable,
        "labels": labels_readable
    }
    with open(output_dir / "predictions_readable.json", "w") as out_file:
        json.dump(results_readable, out_file)

def save_inference_metrics(output_dir: Path, prediction_output):
  with open(output_dir / "inference_metrics.json", "w") as out_file:
    json.dump(prediction_output.metrics, out_file)

def save_metadata(output_dir: Path, dataset_config: DatasetConfig, model_id: str, comments: str):
  with open(output_dir / "metadata.json", "w") as out_file:
    json.dump({
      "dataset_id": dataset_config.dataset_id,
      "dataset_config": dataset_config.dataset_config,
      "dataset_split": dataset_config.dataset_split,
      "dataset_load_command": dataset_config.dataset_load_command,
      "model_id": model_id,
      "comments": comments,
    }, out_file)