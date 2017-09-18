## CRAN packages
tidyverse_packages <- c("tidyverse", "reshape2")
visualization_packages <- c("RColorBrewer", "pander", "scales",
                            "gridExtra", "ggbeeswarm", "corrplot",
                            "ggthemes")

required_packages <- c(tidyverse_packages, visualization_packages)

packagesCRAN(required_packages,
             update=setMissingVar(var_name="update_package",
                                  value=FALSE))

## Clear Workspace
rm(list = ls())
