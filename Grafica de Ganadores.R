### Observar datos de full data

data <- read.csv("D:/Proyectos/FIFA-WorldCup-Analyst/data/PredictComplete.csv")

head(data)

data$Primer.Lugar <- factor(data$Primer.Lugar)
data$Segundo.Lugar <- factor(data$Segundo.Lugar)
data$Tercer.Lugar <- factor(data$Tercer.Lugar)
data$Cuarto.Lugar <- factor(data$Cuarto.Lugar)

par(mfrow = c(2,2))
plot(data$Primer.Lugar,col = "#FFC300")
plot(data$Segundo.Lugar,col = "#C4C7C3")
plot(data$Tercer.Lugar,col = "#8D5E04")
plot(data$Cuarto.Lugar,col = "#055578")
