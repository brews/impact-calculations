print("Checking climate data...")

from climate import discover

discoverer = discover.standard_variable('tas', 'day')
assert discoverer, "Cannot find TAS dataset."

readerset = next(discoverer)
assert readerset, "Cannot load TAS dataset."

scenario, mode, pastreader, futurereader = readerset
assert pastreader.read_year(2000), "Cannot read TAS dataset."
    
print("Checking socioeconomic data...")

from adaptation import econmodel

discoverer = econmodel.iterate_econmodels()
assert discoverer, "Cannot find economic dataset."

readerset = next(discoverer)
assert readerset, "Cannot load economic dataset."

model, scenario, economicmodel = readerset
assert economicmodel.get_loggdppc_year('IND.33.542.2153', 2000), "Cannot read economic dataset."

from impactlab_tools.utils import versions
import json

print(json.dumps(versions.check_version(['self', 'numpy', 'scipy', 'netCDF4', 'metacsv', 'impactlab-tools', 'open-estimate']), indent=4))

