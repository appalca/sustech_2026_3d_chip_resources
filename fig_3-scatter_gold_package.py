import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

colors = ['#852D25', '#c74438', '#E9B5B0', '#0093A7', "#1E1E1E", "#3E4A83", "#FFCD31",
          "#A72587", "#BD987A"]
sns.set_style("whitegrid")

fig, ax = plt.subplots(1, 1)
df = pd.read_csv("data/gold_package_qfn_qfp.csv", delimiter=";")
sns.scatterplot(data=df, x="IOs", y="Gold (mg)", color=colors[0])

a, _, _, _ = np.linalg.lstsq(pd.DataFrame(df["IOs"]), df["Gold (mg)"])

plt.plot([df["IOs"].min(), df["IOs"].max()], [a * df["IOs"].min(), a * df["IOs"].max()],
         c=colors[1], ls=":")
fig.set_size_inches(3.2, 2.7)
plt.subplots_adjust(bottom=0.15, right=0.99, top=0.99)
plt.savefig("figures/scatter_gold.pdf")
