library(data.table)
library(Rcan)
library(ggplot2)
library(gridExtra)
library(Cairo)
library(officer)

setwd("C:/Projects/inkbash/ci5_365")
source("source/Rcan_core.r")
file_cancer_color_ci5 <- "data/color_cancer_ci5.csv"
file_cancer_color_globo <- "data/color_cancer_globocan.csv"
file_globocan_dict <- "data/cancer_ci5_globocan.csv"
file_data <- "data/"
file_pptx <-paste(sep="/","slide_template", "shiny_template.pptx")
file_utf8 <- ""

graph_width <- 8
graph_width_vertical <- 4
radioCancer <- "ci5"

dt_cancer_color_ci5 <- data.table(read.csv(file_cancer_color_ci5))
dt_cancer_color_globo <- data.table(read.csv(file_cancer_color_globo))
dt_globo_dict <- data.table(read.csv(file_globocan_dict))


check_country <- FALSE

if (check_country) {
		fileCSV <- paste0("country_list", file_utf8, ".csv")
		title <- "Country"
	  var_code <- "country_code"
	  var_label <- "country_label"
	  fileRDS <- "CI5XI_country.rds"
	} else {
		fileCSV <-  paste0("registry_list", file_utf8, ".csv")
		title <- "Registry"
	  var_code <- "registry"
	  var_label <- "registry_lab"
	  fileRDS <- "CI5XI.rds"
  	  
}


dt_temp <- data.table(readRDS(paste0(file_data, fileRDS)))

dt_list <- read.csv(paste0(file_data, fileCSV))


registry_list <- list()
for (i in 1:nrow(dt_list)) {
  registry_list[[as.character(dt_list$registry_lab[i])]] <- dt_list$registry[i]
}
  
registry_data <- data.table(dt_list)


dt_list <- read.csv(paste0(file_data, fileCSV))
registry_data <- data.table(dt_list)

setnames(dt_temp,var_code,"registry"  )
setnames(dt_temp,var_label,"registry_lab"  )

dt_temp[sex == 1 & cancer %in% 29:36, cases := 0]
dt_temp[sex == 2 & cancer %in% 38:41, cases := 0]

dt_CI5 <- copy(dt_temp)


for (select_registry in unique(dt_CI5$registry))
{

	dt_temp<- dt_CI5[registry == select_registry, ]

	registry_label <- registry_data[registry==select_registry,]$registry_lab

	registry_label <- sub("\\s\\(\\d.*\\)", "", registry_label)
	registry_file <- gsub("\\s?\\W\\s?", "_", registry_label)
	registry_file <- gsub("\\s", "_", registry_file)

	dt_temp <- dt_temp[age==19, py:=0]
	dt_temp[py>0, age_group_label:=paste0((age-1)*5, "-", (age*5)-1)]
	dt_temp[py>0 ,temp_max:=max(age)]
	dt_temp[age==temp_max ,age_group_label:=paste0((age-1)*5, "+")]
	max_age <- max(dt_temp[py >0,]$age)        

	if (radioCancer == "ci5") {
	            
		dt_temp <- dt_temp[cancer != 63,]
		dt_temp <- dt_temp[cancer != 62,]
		dt_temp <- dt_temp[cancer != 25,]
	  
	} else {
	  
	  dt_temp <- merge(dt_temp, dt_globo_dict, by=c("cancer", "cancer_lab"))
	  dt_temp <- dt_temp[globocan_code != 99,]
	  dt_temp <- dt_temp[,cancer := NULL]
	  dt_temp <- dt_temp[,cancer_lab := NULL]
	  setnames(dt_temp, "globocan_code", "cancer")
	  setnames(dt_temp, "globocan_label", "cancer_lab")
	  
	  dt_temp <- dt_temp[cancer != 29,]
	  
	  group_by <- c("cancer_lab","cancer", "age","age_group_label", "sex")
	  dt_temp <-  dt_temp[,list(cases=sum(cases), py=mean(py)), by=group_by]
	  
	  
	}

	dt_temp$sex <- factor(dt_temp$sex, levels=c(1,2), labels=c("Male", "Female"))
	dt_temp[, cancer :=factor(cancer)]

	first_age <- 1
	last_age <- 18

	dt_temp <- Rcan:::core.csu_asr(df_data =dt_temp,
	   var_age="age", var_cases="cases", var_py="py",
	   group_by = c("cancer", "cancer_lab", "sex"), 
	   first_age = first_age,
	   last_age= last_age,
	   missing_age = 19)



	nb_top <- 10
	age2 <- paste0(((max_age-1)*5), "+")
	var_top <- "asr"
	digit <- 1
	ytitle <- paste0("Age-standardized incidence rate per ", formatC(100000, format="d", big.mark=","), ", ", 0, "-", age2, " years old" )


	dt_temp$cancer_lab <-Rcan:::core.csu_legend_wrapper(dt_temp$cancer_lab, 25)


	file_label <- paste0("_figs/barchart_sex","/bar_top10_asr_male_female_", registry_file)


	 	file_svg <- paste0(file_label, ".svg")
		file_pdf <- paste0(file_label, ".pdf")

	source("source/Rcan_core.r")

	  svg(file_svg,width = 12, height = 10, pointsize = 6)

	  	canreg_bar_top(df_data=dt_temp,
	     var_top = var_top,
	     var_bar = "cancer_lab",
	     group_by = "sex",
	     color_bar=c("Male" = "#2c7bb6", "Female" = "#b62ca1"), nb_top = nb_top,nsmall = digit,
	     canreg_header  = NULL,
	     ytitle=ytitle)

	  dev.off()



   system(paste0('python "barchart_sex_twitter.py" ', file_svg,' ',  paste0('"',registry_label, '"' )),
			         wait=FALSE, intern = TRUE)
   system(paste0('inkscape --without-gui --export-pdf=', file_pdf," ", file_svg), 
			         wait=FALSE, intern = TRUE)


   	print(registry_label)

}