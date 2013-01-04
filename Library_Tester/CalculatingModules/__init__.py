
#for structuring the modules only
#import all *.py file under /CalculatingModules

import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == "__init__.py" or module[-3:] != ".py":
        continue
    __import__(module[:-3], locals(), globals())


