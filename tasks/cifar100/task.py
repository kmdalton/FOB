from engine.configs import TaskConfig
from optimizers import Optimizer
from tasks import TaskModel, TaskDataModule
from tasks.cifar100.data import CIFAR100DataModule
from tasks.cifar100.model import CIFAR100Model


def get_datamodule(config: TaskConfig) -> TaskDataModule:
    return CIFAR100DataModule(config)


def get_task(optimizer: Optimizer, config: TaskConfig) -> tuple[TaskModel, TaskDataModule]:
    return CIFAR100Model(optimizer, config), get_datamodule(config)
