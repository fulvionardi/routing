import matplotlib.pyplot as plt
import pandas
import seaborn as sns

def read_dataset(titles, nodes, prob):
    df = pandas.read_csv("output_nodes_{}_prob_{}_times_1000.csv".format(nodes, prob))
    titles = titles + (list(zip(df["avg_received_packets"].tolist(), df["avg_steps_for_arrival"].tolist(),
                           ["nodes {} prob {}".format(nodes, prob) for i in range(df["avg_steps_for_arrival"].tolist().__len__())])))
    return titles

# plt.style.use('ggplot')
sns.set_theme()

nodes = ["20", "35", "50"]
prob = ["0.2"]

different_parameters = []
# accuracy = [["{}".format(i) for i in range(501) ]]

for n in nodes:
    for p in prob:
        different_parameters = read_dataset(different_parameters, n, p)

df = pandas.DataFrame(different_parameters, columns=["avg_received_packets", "avg_steps_for_arrival", "data set"])

rel = sns.scatterplot(data=df, x="avg_steps_for_arrival", y="avg_received_packets", hue="data set")

plt.xlabel('avg steps for arrival')
plt.ylabel('avg received packets')
plt.show()


