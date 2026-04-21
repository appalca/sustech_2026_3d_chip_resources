import yaml
import csv
import pandas as pd
from matplotlib import pyplot as plt

from apparun.impact_model import ImpactModel
from apparun.results import get_result

from utils.plot import heatmap_multicriteria

IMPACT_METHOD_NAMES = ["EFV3_CLIMATE_CHANGE", "EFV3_IONISING_RADIATION"]

EKI_NAME = "Eki et al."
NAKAMURA_NAME = "Nakamura et al."
J3DAI_NAME = "J3DAI"

impact_model = ImpactModel.from_yaml("data/multi_layer_CIS.yaml")

with open("data/sensitivity_scenarios.yaml", "r") as f:
    sensitivity_scenarios = yaml.safe_load(f)

with open("data/eki.yaml", "r") as stream:
    two_wafers_config = yaml.safe_load(stream)
    two_wafers_config.pop("Mpixel")
with open("data/nakamura.yaml", "r") as stream:
    three_wafers_config = yaml.safe_load(stream)
    three_wafers_config.pop("Mpixel")
with open("data/jedai.yaml", "r") as stream:
    jedai_config = yaml.safe_load(stream)
    jedai_config.pop("Mpixel")

cis = {EKI_NAME: two_wafers_config,
       NAKAMURA_NAME: three_wafers_config,
       J3DAI_NAME: jedai_config, }

sensitivity_results = []
row_order = []
for sensitivity_scenario in sensitivity_scenarios:
    if sensitivity_scenario['parameter'] == "defect_density":
        scenario_name = "defect_density: favorable to unfavorable"
    else:
        scenario_name = f"{sensitivity_scenario['parameter']}: {sensitivity_scenario['reference']} to {sensitivity_scenario['target']}"
    row_order.append(scenario_name)
    for device_name, device_params in cis.items():
        reference_scores = impact_model.get_scores(**{**device_params, **{
            sensitivity_scenario["parameter"]: sensitivity_scenario["reference"]}})
        target_scores = impact_model.get_scores(**{**device_params, **{
            sensitivity_scenario["parameter"]: sensitivity_scenario["target"]}})
        sensitivity_result = {"device": device_name,
                              "param.: ref. to target": scenario_name}
        for impact_method in IMPACT_METHOD_NAMES:
            sensitivity_result[f"{impact_method}_reference"] = \
            reference_scores.scores[impact_method][0]
            sensitivity_result[f"{impact_method}_target"] = \
            target_scores.scores[impact_method][0]
            sensitivity_result[f"{impact_method}_variation"] = abs((sensitivity_result[
                                                                        f"{impact_method}_target"] -
                                                                    sensitivity_result[
                                                                        f"{impact_method}_reference"]) /
                                                                   sensitivity_result[
                                                                       f"{impact_method}_reference"]) * 100
        sensitivity_results.append(sensitivity_result)
sensitivity_results = pd.DataFrame(sensitivity_results)
print(sensitivity_results)

heatmap_multicriteria(sensitivity_results, IMPACT_METHOD_NAMES,
                      "param.: ref. to target",
                      "device",
                      "variation",
                      show=False,
                      row_order=row_order,
                      col_order=[cis_name for cis_name in cis.keys()])
plt.savefig("figures/sensitivity_analysis.pdf")
