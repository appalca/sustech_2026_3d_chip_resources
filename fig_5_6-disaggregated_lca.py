import pandas as pd
import yaml

from matplotlib import pyplot as plt

from apparun.impact_model import ImpactModel
from utils.plot import relative_bar_plot

EKI_NAME = "Eki et al."
NAKAMURA_NAME = "Nakamura et al."
J3DAI_NAME = "J3DAI"

def normalize_contributors(scores_df, node_names: dict):
    norm_scores = [score for score in scores_df if score.name in node_names.keys()]
    norm_scores = pd.concat([score.to_unpivoted_df() for score in norm_scores])
    max_scores = norm_scores.groupby("method")["score"].sum().reset_index()
    max_scores = max_scores[["method", "score"]].rename(columns={"score": "max_score"})
    norm_scores = norm_scores.merge(max_scores, on="method")
    norm_scores["name"] = norm_scores["name"].replace(node_names)
    norm_scores["norm_score"] = norm_scores["score"] / norm_scores["max_score"]
    return norm_scores


package_materials = {"package_copper": "Copper",
                     "package_electricity": "Electricity",
                     "package_gold": "Gold",
                     "package_iron": "Iron",
                     "package_nickel": "Nickel",
                     "package_palladium": "Palladium",
                     "package_silver": "Silver",
                     "package_tin": "Tin",
                     "package_zinc": "Zinc"}

assembly_steps = {"hb": "HB sequences",
                  "tsv": "TSV sequences",
                  "grinding": "Thinning sequences"}

impact_model = ImpactModel.from_yaml("data/multi_layer_CIS.yaml")

colors = ['#852D25', '#c74438', '#E9B5B0', '#0093A7']

with open("data/nakamura.yaml", "r") as stream:
    three_wafers_config = yaml.safe_load(stream)
    three_wafers_config.pop("Mpixel")

scores = impact_model.get_nodes_scores(**three_wafers_config)
package_norm_scores = normalize_contributors(scores, package_materials)

relative_bar_plot(package_norm_scores, "method", "norm_score", "name")
plt.savefig("figures/comparative_package.pdf", dpi=300)

assembly_norm_scores = normalize_contributors(scores, assembly_steps)
relative_bar_plot(assembly_norm_scores, "method", "norm_score", "name")
plt.savefig("figures/comparative_assembly.pdf", dpi=300)