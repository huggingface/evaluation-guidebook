import lighteval
from lighteval.logging.evaluation_tracker import EvaluationTracker
from lighteval.models.model_config import VLLMModelConfig
from lighteval.pipeline import ParallelismManager, Pipeline, PipelineParameters


def main():
    evaluation_tracker = EvaluationTracker(
        output_dir="./results",
        save_details=True,
    )

    pipeline_params = PipelineParameters(
        launcher_type=ParallelismManager.ACCELERATE,
    )

    model_config = VLLMModelConfig(
            pretrained="HuggingFaceH4/zephyr-7b-beta",
            dtype="float16",
            use_chat_template=True,
    )

    task = "helm|mmlu|5|1"

    pipeline = Pipeline(
        tasks=task,
        pipeline_parameters=pipeline_params,
        evaluation_tracker=evaluation_tracker,
        model_config=model_config,
    )

    pipeline.evaluate()
    pipeline.save_and_push_results()
    pipeline.show_results()

if __name__ == "__main__":
    main()
