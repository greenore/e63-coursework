## CRAN packages
tidyverse_packages <- c("tidyverse")
data_packages <- c("jsonlite", "RNeo4j", "readr", "reshape2")
visualization_packages <- c("RColorBrewer", "pander", "scales",
                            "gridExtra", "ggbeeswarm",
                            "ggthemes")

required_packages <- c(tidyverse_packages, visualization_packages, data_packages)

packagesCRAN(required_packages,
             update=setMissingVar(var_name="update_package",
                                  value=FALSE))

## Clear Workspace
rm(list = ls())
