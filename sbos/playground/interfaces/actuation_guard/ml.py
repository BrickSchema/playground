import random
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from loguru import logger

from sbos.playground.interfaces.actuation_guard.base import ActuationGuard

# device = torch.device("cpu")
device = torch.device("cpu")


class VAE(nn.Module):
    def __init__(self, state_dim, action_dim, latent_dim, device):
        super().__init__()
        self.e1 = nn.Linear(state_dim + action_dim, 750)
        self.e2 = nn.Linear(750, 750)

        self.mean = nn.Linear(750, latent_dim)
        self.log_std = nn.Linear(750, latent_dim)

        self.d1 = nn.Linear(state_dim + latent_dim, 750)
        self.d2 = nn.Linear(750, 750)
        self.d3 = nn.Linear(750, action_dim)

        self.latent_dim = latent_dim
        self.device = device

    def forward(self, state, action):
        z = F.relu(self.e1(torch.cat([state, action], 1)))
        z = F.relu(self.e2(z))

        mean = self.mean(z)
        # Clamped for numerical stability
        log_std = self.log_std(z).clamp(-4, 15)
        std = torch.exp(log_std)
        z = mean + std * torch.randn_like(std)

        u = self.decode(state, z)

        return u, mean, std

    def decode(self, state, z=None):
        # When sampling from the VAE, the latent vector is clipped to [-0.5, 0.5]
        if z is None:
            z = (
                torch.randn((state.shape[0], self.latent_dim))
                .to(device)
                .clamp(-0.5, 0.5)
            )

        a = F.relu(self.d1(torch.cat([state, z], 1)))
        a = F.relu(self.d2(a))
        return self.d3(a)


ML_ENTITY_IDS = [
    "FM-ADX:SNE-198/FC-1.AH3-CVM-021.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-022.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-023.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-024.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-025.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-026.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-027.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-028.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-029.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-030.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-031.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-032.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-033.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-034.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-035.DA-T",
    "FM-ADX:SNE-198/FC-1.AH3-CVM-036.DA-T",
    "FM-ADX:SNE-198/FC-2.AH3-CVM-025.DA-T",
    "FM-ADX:SNE-198/FC-2.AH3-CVM-026.DA-T",
    "FM-ADX:SNE-198/FC-2.AH3-CVM-027.DA-T",
    "FM-ADX:SNE-198/FC-2.AH3-CVM-028.DA-T",
    "FM-ADX:SNE-198/FC-2.AH3-CVM-029.DA-T",
    "FM-ADX:SNE-198/FC-2.AH3-CVM-030.DA-T",
]


class ActuationGuardML(ActuationGuard):
    def __init__(self):
        super().__init__()
        model_file = (
            Path(__file__).parent.parent.parent.parent.parent / "models" / "model.pt"
        )
        # self.device = torch.device("cpu")
        # self.model = VAE(state_dim=22, action_dim=2, latent_dim=2 * 2, device=self.device)
        # self.model.load_state_dict(torch.load(model_file, map_location=self.device))
        import __main__

        setattr(__main__, "VAE", VAE)
        self.model = torch.load(model_file, map_location=device)

    # def inference(self, input):
    #     prediction = self.model.decode(torch.FloatTensor(input).reshape(1, -1).to(device))
    #     prediction = prediction.detach().cpu().numpy()
    #     print(f'\nInput:{input}\n\nOutput(inference): {prediction}')
    #     return None

    def __call__(self, entity_id, value) -> bool:
        # if entity_id not in ML_ENTITY_IDS:
        #     raise TypeError()
        # index = ML_ENTITY_IDS.index(entity_id)
        value = float(value)
        index = random.randint(0, len(ML_ENTITY_IDS) - 1)
        # TODO: get from db
        input_vector = [
            58.6129875,
            60.5962181,
            60.3656464,
            110.464554,
            60.2773094,
            70.251152,
            59.0658264,
            124.50721,
            68.3790512,
            60.8945732,
            60.8702507,
            72.7485809,
            84.9723434,
            85.3841095,
            76.1273956,
            75.4476242,
            86.0944901,
            73.2938614,
            60.3714371,
            113.095421,
            71.4996643,
            68.5879135,
        ]
        input_vector = [70] * len(input_vector)
        input_vector[index] = value
        prediction = self.model.decode(
            torch.FloatTensor(input_vector).reshape(1, -1).to(device)
        )
        prediction = prediction.detach().cpu().numpy()
        logger.info(input_vector)
        logger.info(prediction)
        return True


if __name__ == "__main__":
    torch.manual_seed(42)
    guard = ActuationGuardML()
    print(guard("FM-ADX:SNE-198/FC-1.AH3-CVM-021.DA-T", 500))
