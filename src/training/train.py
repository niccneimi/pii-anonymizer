from gliner import GLiNER
from src.training.data_preparation import convert_to_gliner_data

if __name__ == "__main__":
    model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
    target_labels = ["PERSON", "EMAIL", "PHONE_NUMBER", "ADDRESS"]

    train_data = convert_to_gliner_data("data/processed/train.jsonl")
    val_data = convert_to_gliner_data("data/processed/val.jsonl")

    trainer = model.train_model(
        train_dataset=train_data,
        eval_dataset=val_data,
        output_dir="models/gliner_pii",
        max_steps=1000,
        learning_rate=5e-5,
        per_device_train_batch_size=8,
    )

    trainer.save_model()