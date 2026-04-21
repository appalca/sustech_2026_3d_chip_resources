import pandas as pd
import yaml

from matplotlib import pyplot as plt

from apparun.impact_model import ImpactModel

from utils.plot import multicriteria_bar_plot, two_yaxis_line_plot, short_to_unit, \
    method_to_short, colors

IMPACT_METHOD_NAMES = ["EFV3_ACIDIFICATION", "EFV3_CLIMATE_CHANGE",
                       "EFV3_IONISING_RADIATION", "EFV3_PARTICULATE_MATTER_FORMATION"]
PERF_UNIT = "suppl. MPixel"

EKI_NAME = "Eki et al."
NAKAMURA_NAME = "Nakamura et al."
J3DAI_NAME = "J3DAI"
impact_model = ImpactModel.from_yaml("data/multi_layer_CIS.yaml")

scenarios = pd.read_csv("data/scenarios.csv")
scenarios = scenarios[scenarios["name"] != "Default"]

with open("data/eki.yaml", "r") as stream:
    two_wafers_config = yaml.safe_load(stream)
with open("data/nakamura.yaml", "r") as stream:
    three_wafers_config = yaml.safe_load(stream)
with open("data/jedai.yaml", "r") as stream:
    jedai_config = yaml.safe_load(stream)

cis = {J3DAI_NAME: jedai_config,
       EKI_NAME: two_wafers_config,
       NAKAMURA_NAME: three_wafers_config}

performances = pd.DataFrame([{"CIS": key, "performance": value["Mpixel"]} for key, value in cis.items()])
impact_model_params = {key: {i: value[i] for i in value if i != 'Mpixel'} for key, value
                       in cis.items()}

#lifetimes = list(range(0, 31))
lifetimes = [0.74, 10] # for automotive, surveillance camera

two_layers_scores = impact_model.get_scores(
    **{**impact_model_params[EKI_NAME], **{"lifespan": lifetimes}})
three_layers_scores = impact_model.get_scores(
    **{**impact_model_params[NAKAMURA_NAME], **{"lifespan": lifetimes}})
jedai_scores = impact_model.get_scores(
    **{**impact_model_params[J3DAI_NAME], **{"lifespan": lifetimes}})

env_scores = []
perf_cost_scores = []

for impact_name in IMPACT_METHOD_NAMES:
    env_score = pd.DataFrame(
        {'cum. active time (year)': lifetimes,
         EKI_NAME: two_layers_scores.scores[impact_name],
         NAKAMURA_NAME: three_layers_scores.scores[impact_name],
         J3DAI_NAME: jedai_scores.scores[impact_name]})

    env_score = env_score.assign(
        best_env_cis_env=env_score[[J3DAI_NAME, EKI_NAME, NAKAMURA_NAME]].min(axis=1),
        best_env_cis_name=env_score[[J3DAI_NAME, EKI_NAME, NAKAMURA_NAME]].idxmin(axis=1))

    env_score = pd.merge(env_score, performances, left_on="best_env_cis_name", right_on="CIS")
    env_score = env_score.rename(columns={"performance": "best_env_cis_perf"})
    env_score["best_perf_cis_perf"] = performances["performance"].max()
    env_score["best_perf_cis_env"] = env_score[performances["CIS"][performances["performance"].idxmax()]]

    env_score["Cost of performance"] = (env_score["best_perf_cis_env"] - env_score[
        "best_env_cis_env"]) / (env_score["best_perf_cis_perf"] - env_score[
        "best_env_cis_perf"])
    env_score["Cost of performance"] = env_score["Cost of performance"].fillna(0)
    env_score["method"] = impact_name
    perf_cost_score = env_score[["cum. active time (year)", "Cost of performance", "method"]]
    env_score = pd.melt(env_score, id_vars=["cum. active time (year)", "method"],
                        value_vars=[EKI_NAME,
                                    NAKAMURA_NAME,
                                    J3DAI_NAME],
                        value_name="score", var_name="CIS")
    env_scores.append(env_score)
    perf_cost_scores.append(perf_cost_score)

scenarios["x"] = scenarios["lifespan"] * scenarios["active_ratio"]

env_scores = pd.concat(env_scores)
perf_cost_scores = pd.concat(perf_cost_scores)
two_yaxis_line_plot(env_scores, "cum. active time (year)",
                    "score", "CIS", colors[0],
                    None, perf_cost_scores, "cum. active time (year)",
                    "Cost of performance", None, colors[3], 's',
                    PERF_UNIT, scenarios[["name", "x"]],
                    show=False)

plt.savefig("figures/perf_cost.pdf", dpi=300)
