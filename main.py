import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# -----------------------------
# CONFIG
# -----------------------------
INPUT_DIM = 10        # biometric + demographic features
HIDDEN_1 = 32         # identity encoding
HIDDEN_2 = 64         # service stack
HIDDEN_3 = 32         # economic behavior
OUTPUT_DIM = 3        # GDP, HDI, Inclusion

EPOCHS = 200
LR = 0.001

# -----------------------------
# SYNTHETIC DATA GENERATION
# -----------------------------
def generate_data(n=5000):
    X = np.random.rand(n, INPUT_DIM)

    # Simulate transformation effects
    identity_strength = np.sum(X[:, :5], axis=1)
    service_access = np.sum(X[:, 5:], axis=1)

    gdp = identity_strength * 0.6 + service_access * 0.8
    hdi = identity_strength * 0.7 + service_access * 0.5
    inclusion = identity_strength * 0.9 + service_access * 0.9

    Y = np.stack([gdp, hdi, inclusion], axis=1)

    # Normalize
    Y = Y / np.max(Y)

    return torch.tensor(X, dtype=torch.float32), torch.tensor(Y, dtype=torch.float32)

# -----------------------------
# MODEL
# -----------------------------
class AadhaarNet(nn.Module):
    def __init__(self):
        super(AadhaarNet, self).__init__()

        self.identity_layer = nn.Sequential(
            nn.Linear(INPUT_DIM, HIDDEN_1),
            nn.ReLU()
        )

        self.auth_layer = nn.Sequential(
            nn.Linear(HIDDEN_1, HIDDEN_2),
            nn.ReLU()
        )

        self.service_layer = nn.Sequential(
            nn.Linear(HIDDEN_2, HIDDEN_3),
            nn.ReLU()
        )

        self.output_layer = nn.Linear(HIDDEN_3, OUTPUT_DIM)

    def forward(self, x):
        x = self.identity_layer(x)
        x = self.auth_layer(x)
        x = self.service_layer(x)
        x = self.output_layer(x)
        return x

# -----------------------------
# TRAINING
# -----------------------------
def train():
    X, Y = generate_data()

    model = AadhaarNet()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)

    for epoch in range(EPOCHS):
        optimizer.zero_grad()

        outputs = model(X)
        loss = criterion(outputs, Y)

        loss.backward()
        optimizer.step()

        if epoch % 20 == 0:
            print(f"Epoch {epoch} | Loss {loss.item():.4f}")

    return model

# -----------------------------
# INFERENCE
# -----------------------------
def inference(model):
    test_input = torch.rand(1, INPUT_DIM)
    prediction = model(test_input).detach().numpy()

    print("\n--- Inference Example ---")
    print("Input Features:", test_input.numpy())
    print("Predicted [GDP, HDI, Inclusion]:", prediction)


if __name__ == "__main__":
    model = train()
    inference(model)
