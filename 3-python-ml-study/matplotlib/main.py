import numpy as np
import matplotlib.pyplot as plt
np.random.seed(42)

toan = np.random.normal(65, 12, 120).clip(0, 100)
ly   = np.random.normal(58, 15, 120).clip(0, 100)
hoa  = np.random.normal(72,  9, 120).clip(0, 100)
anh  = np.random.normal(60, 18, 120).clip(0, 100)


data = [toan, ly, hoa, anh]

plt.boxplot(data, labels=["Toán", "Lý", "Hóa", "Anh"])

plt.title("Phân bố điểm các môn")
plt.ylabel("Điểm số")

plt.grid(True)
plt.show()