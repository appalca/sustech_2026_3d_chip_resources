import yaml

from matplotlib import pyplot as plt

from apparun.impact_model import ImpactModel
from utils.plot import multicriteria_bar_plot

EKI_NAME = "Eki et al."
NAKAMURA_NAME = "Nakamura et al."
J3DAI_NAME = "J3DAI"

impact_model = ImpactModel.from_yaml("data/multi_layer_CIS.yaml")

colors = ['#852D25', '#c74438', '#E9B5B0', '#0093A7']

with open("data/eki.yaml", "r") as stream:
    two_wafers_config = yaml.safe_load(stream)
    two_wafers_config.pop("Mpixel")
with open("data/nakamura.yaml", "r") as stream:
    three_wafers_config = yaml.safe_load(stream)
    three_wafers_config.pop("Mpixel")
with open("data/jedai.yaml", "r") as stream:
    jedai_config = yaml.safe_load(stream)
    jedai_config.pop("Mpixel")

fig = multicriteria_bar_plot(
    [impact_model.get_nodes_scores(**two_wafers_config, by_property="element"),
     impact_model.get_nodes_scores(**three_wafers_config, by_property="element"),
     impact_model.get_nodes_scores(**jedai_config, by_property="element")],
    [EKI_NAME,
     NAKAMURA_NAME,
     J3DAI_NAME],
    ["multi_layer_CIS"],
    colors=colors,
    show=False)
plt.savefig("figures/comparative_lca.pdf", dpi=300)
