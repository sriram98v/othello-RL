import torch 

class Q_Network(torch.nn.Module):
    def __init__(self):
        super().__init__()
        
        # Inputs to hidden layer linear transformation
        self.hidden1 = torch.nn.Linear(64, 50)
        self.sigmoid1 = torch.nn.Sigmoid()
        # Output layer, 10 units - one for each digit
        self.hidden2 = torch.nn.Linear(50, 64)
        
        # Define sigmoid activation and softmax output 
        self.sigmoid2 = torch.nn.Sigmoid()
        
    def forward(self, x):
        # Pass the input tensor through each of our operations
        x = self.hidden1(x)
        x = self.sigmoid1(x)
        x = self.hidden2(x)
        x = self.sigmoid2(x)
        
        return x
    
