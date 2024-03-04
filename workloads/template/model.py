import torch
from workloads import WorkloadModel
from runtime.configs import WorkloadConfig
from submissions import Submission


class TemplateModel(WorkloadModel):
    def __init__(self, submission: Submission, workload_config: WorkloadConfig):
        model = torch.nn.Sequential(
            torch.nn.Linear(1, 10),
            torch.nn.ReLU(),
            torch.nn.Linear(10, 1),
            torch.nn.ReLU(),
        )
        self.loss = torch.nn.functional.mse_loss
        super().__init__(model, submission, workload_config)

    def training_step(self, batch, batch_idx):
        # training_step defines the train loop.
        # it is independent of forward
        x = y = batch
        y_hat = self.model(x)
        loss = self.loss(y_hat, y)
        # Logging to TensorBoard (if installed) by default
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        self.compute_and_log_loss(batch, "val_loss")

    def test_step(self, batch, batch_idx):
        self.compute_and_log_loss(batch, "test_loss")

    def compute_and_log_loss(self, batch, log_name: str):
        x = y = batch
        batch_size = x.size(0)
        x = x.view(batch_size, -1)
        y_hat = self.model(x)
        loss = self.loss(y_hat, y)
        self.log(log_name, loss)
