# Weekly progress data plotting 

library(ggplot2)
library(readODS)

# Load data:
filepath <- readline("enter an ods file name: ")
dataframe <- read.ods(file = filepath, sheet = 1, formulaAsFormula = FALSE)
dataframe_week   <- as.numeric(format(dataframe$Date, "%W")) 
print("dataframe_week is", dataframe_week)
cat(dataframe_week)

# Graph by month: adds up all observations for the month
#ggplot(data = log, aes(Month, Quantity)) + stat_summary(fun.y = sum, geom = "bar") + # or "line"
#  scale_x_date(labels = date_format("%Y-%m"), breaks = "1 month") # custom x-axis labels

