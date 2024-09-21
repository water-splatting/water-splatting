from nerfstudio.engine.trainer import TrainerConfig
from nerfstudio.plugins.types import MethodSpecification
from nerfstudio.pipelines.base_pipeline import VanillaPipelineConfig
from nerfstudio.data.datamanagers.full_images_datamanager import FullImageDatamanagerConfig
from nerfstudio.data.dataparsers.nerfstudio_dataparser import NerfstudioDataParserConfig
from nerfstudio.engine.schedulers import ExponentialDecaySchedulerConfig
from nerfstudio.engine.optimizers import AdamOptimizerConfig
from nerfstudio.configs.base_config import ViewerConfig
from water_splatting.water_splatting import WaterSplattingModelConfig

NUM_STEPS = 15000
# Base method configuration
water_splatting_method = MethodSpecification(
    config=TrainerConfig(
        method_name="water-splatting",
        steps_per_eval_image=1000,
        steps_per_eval_batch=0,
        steps_per_save=2000,
        steps_per_eval_all_images=1000,
        max_num_iterations=NUM_STEPS,
        mixed_precision=False,
        pipeline=VanillaPipelineConfig(
            datamanager=FullImageDatamanagerConfig(
                dataparser=NerfstudioDataParserConfig(load_3D_points=True),
            ),
            model=WaterSplattingModelConfig(
                num_steps=NUM_STEPS,
                main_loss="reg_l1",
                ssim_loss="reg_ssim",
                zero_medium=False,
                                          ),
        ),
        optimizers={
            "means": {
                "optimizer": AdamOptimizerConfig(lr=1.6e-4, eps=1e-15),
                "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=5e-5,
                    max_steps=NUM_STEPS,
                ),
            },
            "features_dc": {
                "optimizer": AdamOptimizerConfig(lr=0.0025, eps=1e-15),
                "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=0.0025,
                    max_steps=NUM_STEPS,
                ),
            },
            "features_rest": {
                "optimizer": AdamOptimizerConfig(lr=0.0025 / 20, eps=1e-15),
                "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=0.0025 / 20,
                    max_steps=NUM_STEPS,
                ),
            },
            "opacities": {
                "optimizer": AdamOptimizerConfig(lr=0.05, eps=1e-15),
                "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=0.05,
                    max_steps=NUM_STEPS,
                ),
            },
            "scales": {
                "optimizer": AdamOptimizerConfig(lr=0.005, eps=1e-15),
                "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=0.005,
                    max_steps=NUM_STEPS,
                ),
            },
            "quats": {"optimizer": AdamOptimizerConfig(lr=0.001, eps=1e-15), 
                      "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=0.001,
                    max_steps=NUM_STEPS,
                ),
            },
            "camera_opt": {
                "optimizer": AdamOptimizerConfig(lr=1e-3, eps=1e-15),
                "scheduler": ExponentialDecaySchedulerConfig(lr_final=5e-5, max_steps=NUM_STEPS),
            },
            "medium_mlp": {
                "optimizer": AdamOptimizerConfig(lr=1e-3, eps=1e-15, max_norm=0.001),
                "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=1.5e-4, max_steps=NUM_STEPS, 
                ),
            },
            "direction_encoding": {
                "optimizer": AdamOptimizerConfig(lr=1e-3, eps=1e-15, max_norm=0.001),
                "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=1.5e-4, max_steps=NUM_STEPS, 
                ),
            },
        },
        viewer=ViewerConfig(num_rays_per_chunk=1 << 15),
        vis="viewer",
    ),
    description="Water-Splatting for underwater scenes.",
)

water_splatting_method_big = MethodSpecification(
    config=TrainerConfig(
        method_name="water-splatting-big",
        steps_per_eval_image=100,
        steps_per_eval_batch=0,
        steps_per_save=2000,
        steps_per_eval_all_images=1000,
        max_num_iterations=NUM_STEPS,
        mixed_precision=False,
        pipeline=VanillaPipelineConfig(
            datamanager=FullImageDatamanagerConfig(
                dataparser=NerfstudioDataParserConfig(load_3D_points=True),
            ),
            model=WaterSplattingModelConfig(
                num_steps=NUM_STEPS,
                continue_cull_post_densification=False,
            ),
        ),
        optimizers={
            "means": {
                "optimizer": AdamOptimizerConfig(lr=1.6e-4, eps=1e-15),
                "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=5e-5,
                    max_steps=NUM_STEPS,
                ),
            },
            "features_dc": {
                "optimizer": AdamOptimizerConfig(lr=0.0025, eps=1e-15),
                "scheduler": None,
            },
            "features_rest": {
                "optimizer": AdamOptimizerConfig(lr=0.0025 / 20, eps=1e-15),
                "scheduler": None,
            },
            "opacities": {
                "optimizer": AdamOptimizerConfig(lr=0.05, eps=1e-15),
                "scheduler": None,
            },
            "scales": {
                "optimizer": AdamOptimizerConfig(lr=0.005, eps=1e-15),
                "scheduler": None,
            },
            "quats": {"optimizer": AdamOptimizerConfig(lr=0.001, eps=1e-15), "scheduler": None},
            "camera_opt": {
                "optimizer": AdamOptimizerConfig(lr=1e-3, eps=1e-15),
                "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=5e-5, max_steps=NUM_STEPS,
                    ),
            },
            "medium_mlp": {
                "optimizer": AdamOptimizerConfig(lr=1e-3, eps=1e-15, max_norm=0.001),
                "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=1.5e-4, max_steps=NUM_STEPS, 
                ),
            },
            "direction_encoding": {
                "optimizer": AdamOptimizerConfig(lr=1e-3, eps=1e-15, max_norm=0.001),
                "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=1.5e-4, max_steps=NUM_STEPS, 
                ),
            },
        },
        viewer=ViewerConfig(num_rays_per_chunk=1 << 15),
        vis="viewer",
    ),
    description="Water-Splatting big for underwater scenes.",
)