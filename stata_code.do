*begin trend panel


	use  "${dir_dta}\nordpred_testis_output_recent.dta", clear

	replace py = 0 if age == 18
	replace cases = 0 if age == 18
	replace cases = 0 if cases < 0


	CSU_ASR age cases py,var_age_gr(country*)  by( country* base    year gof np  ) standardE("st_err")  var_ASR("asr") 

	merge m:1 country_code  using   "${dir_dta}\pop_estimate.dta"
	drop _m



	sort  country_code  year 
	format temp_ratio %4.1f

	CSU_country_info country_code
	drop continent* country_iso3

	sort  area_label country_code  year 
	egen dummy_country = group(country_code)

	tempfile temp_graph
	save `temp_graph' ,replace

	use `temp_graph' ,clear
	keep country* area* 
	duplicates drop 
	gsort area* country_label 
	bys area_code :gen order = _n
	gen str_order = string(order,"%02.0f") 
	drop order 
	tempfile temp_order
	save `temp_order' ,replace

	use `temp_graph' ,clear
	merge m:1 area* country* using `temp_order'
	drop _m 
	sort country* year 
	save `temp_graph' ,replace

	sum asr
	tab year

	forvalues i =1/ 26 {

		use `temp_graph' ,clear
		
		keep if dummy_country == `i'
		
		
		drop if year < 1975
		sum year
		local min_y = r(min)
		if mod( `min_y', 10) == 0 {
			local min2_y = `min_y'
		}
		else {
			local min2_y = `min_y'+5
		}
		
		local title_graph = country_label
		
		if national == 0 {
			local title_graph = "`title_graph'*"
			local subtitle_graph = "*: based on regional registries" 
		}
		else {
			local subtitle_graph = "" 
		}

		
		
		
		 # delimit ;
		twoway 
			
			(connected asr year if  base<=2 , lcolor( "25 113 159") lwidth(medthick) msymbol(none)  mlabcolor(black))
			(connected asr year if  base>=2 , lcolor( "25 113 159") lwidth(medthick) lpattern(dash) msymbol(none)  mlabcolor(black)) // 

			
				, 
				
				title( `title_graph', color(black))
				//caption( `subtitle_graph', size(2))
				ytitle( "Age standardized incidence rate per 100,000",size(small)) 
				yscale(  log range(0.9 17) titlegap(5)) // titlegap(1)
				ylabel( 1 1.2 1.5 2 2.5 3 4 5 6 7 8 9 10 12 13 15 17    , labels labsize(small) angle(horizontal) format(%3s) grid glwidth(vthin) glcolor(gs13)) 
				ymtick(0.9 (0.1) 2.5 2.5 (0.5) 5 5 (1) 17   , nolabels grid glwidth(vthin) glcolor(gs13)) 
				xtitle( "Year" ,size(small) ) 
				xscale( titlegap(3))
				xlabel( 1980 (10) 2030, labsize(small) valuelabel grid glwidth(vthin) glcolor(gs13) )  // labgap(1)
				xmtick( 1980 (5) 2035 , nolabels grid glwidth(vthin) glcolor(gs13)) 
				xline( 1980 ,   lwidth(vthin) lcolor(gs13)) 
				legend(off)
				name(graph`i', replace)
				graphregion(style(none) istyle(none))
				plotregion(style(none) istyle(none))
				ysize(10) xsize(7)  

			;
			
		# delimit cr
		
		
		local area_code = area_code
		local str_order = str_order
		local title_graph = country_label 		
		
		graph export "${dir_inkbash}\trend_panel\temp\graph_`area_code'_`str_order'.eps", as(eps) replace

	}
	 

*end 

*begin pie


	use "${dir_GHE_mortality}\GHE_mortality_2016.dta", clear

	keep if country_code == 250
	keep if sex == 0 
	drop if age == 7

	collapse (sum) cases, by(ghe* )

	replace ghe_level = 2 if ghe_level == 0 
	keep if ghe_level == 2
	gsort -cases

	gen rk_cases =_n
	drop if rk_cases > 6


	forvalues i=1(1)5 {

		replace cases = cases - cases[_n+`i'] if rk == 1 

	}

	replace rk_cases = 7 if rk == 1 
	replace ghe_cause = "Other" if rk == 7 
	sort  rk_cases

	csv_merge ghe_code using "${dir_DATA}\_dict\cancer_color.csv", master_key(10) using_key(10)
	keep if _m == 3
	drop _m v5 colorhex cancer cancer_lab

	sort rk_cases
	local color1= color[1]
	local color2= color[2]
	local color3= color[3]
	local color4= color[4]
	local color5= color[5]
	local color6= color[6]



	#delimit ;
	 
	graph pie cases , 	
			over(ghe_cause)
			sort(rk_cases) 
			angle(90) 
			fxsize( 100 )
			
			pie(1,  color ( `color1'))
			pie(2,  color ( `color2'))
			pie(3,  color ( `color3'))
			pie(4,  color ( `color4'))
			pie(5,  color ( `color5'))
			pie(6,  color ( `color6'))

			plabel(1 percent, size(medium) color (black) gap(10))
			plabel(2 percent, size(medium) color (black) gap(10))
			plabel(3 percent, size(medium) color (black) gap(10))
			plabel(4 percent, size(medium) color (black) gap(10))
			plabel(5 percent, size(medium) color (black) gap(10))
			plabel(6 percent, size(medium) color (black) gap(10))
			
			legend(off) 
			graphregion(style(none) istyle(none))
			plotregion(style(none) istyle(none))
	;
	#delimit cr

	keep rk ghe_cause cases
	outsheet using  "${dir_inkbash}\pie\temp\cancer_info.csv", comma replace
	

	graph export "${dir_inkbash}\pie\temp\temp.eps", as(eps) replace



*end 



*begin top5 pie bar auto



local sex 0
local country 900

		
		
		use "${dir_GLOBO2018}\Globocan_asr_cases_cumrisk_CRC.dta", clear
		drop asr cumrisk 
		keep if sex == `sex'

		drop if inlist(cancer_code,17,37,38,40) // drop skin, other cancer and unspecified cancer 
		
		//regroup for cancer_tabacco related 
		replace cancer_code =15 if inlist(cancer_code ,1,2,3,4,5,6,7,8,9,11,13,14,15,23,29,30 )
		replace cancer_label = "Smoking related cancer" if cancer_code ==15 
		
		collapse (sum) cases (mean) py, by (type sex cancer* country*)
		
		keep if country_code == `country'
		tab country_label

		collapse (sum) cases py, by(type sex cancer*) 

		gsort +type sex -cases
		bys type sex  : gen rk_cases =_n
		keep if rk_cases <= 6

		
		
		tempfile temp_tot
		save `temp_tot', replace
		
		gen percent = 0 
		forvalues i = 0(1)5 {
			replace percent = (cases/(cases[_n-`i']))*100 if rk == `i' +1
		}
		
		list


			*begin pie
			

			use `temp_tot', replace

			gen prop5 = 0 if rk == 1
			replace prop5 = 1 if rk > 1

			collapse (sum) cases, by(type prop5)
			gen percent = (cases - cases[_n+1])*100 / cases if prop5 == 0
			replace percent = cases *100 / cases[_n-1] if prop5 == 1 
			
			forvalue i = 0(1)2 {
			
			#delimit ;
				 
				graph pie percent if type == `i', 	
						over(prop5) 
						angle(90) 
						
						pie(2,  color (26 98 162))
						pie(1,  color ( 220 220 220))

						plabel(2 percent, size(medium) color (black) gap(5))
						plabel(1 percent, size(medium) color (black) gap(5))
						
						legend(off) 
						name(pie_`i', replace)
					graphregion(style(none) istyle(none))
					plotregion(style(none) istyle(none))
				;
				#delimit cr
				
				graph export "${inkbash}\pie_bar\temp\pie`i'.eps", as(eps) replace

				
			}

				


			

			*end

			*begin bar
			

			
			forvalue i = 0(1)2 {
			
				use `temp_tot', replace
				replace rk_cases = rk_cases -1
				drop if rk_cases == 0

				merge m:1 cancer_code using "${dir_DATA}\_dict\cancer_color_2018.dta"
				keep if _m == 3
				drop _m
				sort type rk 
				
				keep if type == `i'

				local color1= color[1]
				local color2= color[2]
				local color3= color[3]
				local color4= color[4]
				local color5= color[5]


				drop cancer* sex color
				reshape wide cases, i(type) j(rk)

				local total = cases1 + cases2 + cases3 + cases4 + cases5
				gen bar1 = cases1 / `total'  
				gen bar2 = cases2 / `total'  
				gen bar3 = cases3 / `total'  
				gen bar4 = cases4 / `total'  
				gen bar5 = cases5 / `total'  

				# delimit;
					graph bar (asis) bar5 bar4 bar3 bar2 bar1  , 
						stack
						yscale(off)
						bar(1, color ( `color5')) 
						bar(2, color ( `color4')) 
						bar(3, color ( `color3')) 
						bar(4, color ( `color2')) 
						bar(5, color ( `color1')) 
						ylabel(,nolabels noticks nogrid)
						legend(off)
						xsize(4)
						ysize(10)
						name(bar_`i', replace)
						graphregion(style(none) istyle(none))
						plotregion(style(none) istyle(none))
						;
						
				# delimit cr
				
				graph export "${inkbash}\pie_bar\temp\bar`i'.eps", as(eps) replace

				
				
				}

			use `temp_tot', replace
			replace rk_cases = rk_cases -1
			drop if rk_cases == 0
			merge m:1 cancer_code using "${dir_DATA}\_dict\cancer_color_2018.dta"
			keep if _m == 3
			drop _m 

			gsort type -rk 
			by type : egen tot=total(cases)
			by type  : gen pos = sum(cases)
			replace pos = pos - (cases/2) 
			replace pos = ((pos/tot)*312.001) + 98.582 - 7.2755
			replace pos = ((pos - 59.833)/1.33333)*(-1) 
			drop py color 
			gsort type rk
			keep cancer_label pos
			list
			outsheet using "${inkbash}\pie_bar\temp\cancer_label.csv", comma replace

			
			use `temp_tot', replace

			quietly gen prop5 = 0 if rk == 1
			quietly replace prop5 = 1 if rk > 1
			gsort type +prop
			quietly collapse (sum) cases, by(type prop5)
			keep cases 
			outsheet using "${inkbash}\pie_bar\temp\cancer_number.csv", comma replace
			

			
			*end
		
	

*end 



*begin top5 pie bar auto



forvalue a = 0(1)2 {
	forvalue b = 981(1)984 {
	
		if `a' == 0 {
			local sex_lab "both" 
		}
		else if `a' == 1{
			local sex_lab "male"
		
		}
		else if `a' == 2{
			local sex_lab "female"
		}
		
		if `b' == 981 {
			local country_lab "very" 
		}
		else if `b' == 982{
			local country_lab "high"
		
		}
		else if `b' == 983{
			local country_lab "medium"
		
		}
		else if `b' == 984{
			local country_lab "low"
		
		}


		
		
		use "${dir_GLOBO2018}\Globocan_asr_cases_cumrisk_CRC.dta", clear
		drop asr cumrisk 
		keep if sex == `a'

		drop if inlist(cancer_code,17,37,38,40) // drop skin, other cancer and unspecified cancer 
		keep if country_code == `b'
		tab country_label

		collapse (sum) cases py, by(type sex cancer*) 

		gsort +type sex -cases
		bys type sex  : gen rk_cases =_n
		keep if rk_cases <= 6
		list


		tempfile temp_tot
		save `temp_tot', replace

			*begin pie
			

			use `temp_tot', replace

			gen prop5 = 0 if rk == 1
			replace prop5 = 1 if rk > 1

			collapse (sum) cases, by(type prop5)
			gen percent = (cases - cases[_n+1])*100 / cases if prop5 == 0
			replace percent = cases *100 / cases[_n-1] if prop5 == 1 
			
			forvalue i = 0(1)2 {
			
			#delimit ;
				 
				graph pie percent if type == `i', 	
						over(prop5) 
						angle(90) 
						
						pie(2,  color (26 98 162))
						pie(1,  color ( 220 220 220))

						plabel(2 percent, size(medium) color (black) gap(5))
						plabel(1 percent, size(medium) color (black) gap(5))
						
						legend(off) 
						name(pie_`i', replace)
					graphregion(style(none) istyle(none))
					plotregion(style(none) istyle(none))
				;
				#delimit cr
				
				graph export "${inkbash}\pie_bar\temp\pie_`country_lab'_`sex_lab'_`i'.eps", as(eps) replace

				
			}

				


			

			*end

			*begin bar
			

			
			forvalue i = 0(1)2 {
			
				use `temp_tot', replace
				replace rk_cases = rk_cases -1
				drop if rk_cases == 0

				merge m:1 cancer_code using "${dir_DATA}\_dict\cancer_color_2018.dta"
				keep if _m == 3
				drop _m
				sort type rk 
				
				keep if type == `i'

				local color1= color[1]
				local color2= color[2]
				local color3= color[3]
				local color4= color[4]
				local color5= color[5]


				drop cancer* sex color
				reshape wide cases, i(type) j(rk)

				local total = cases1 + cases2 + cases3 + cases4 + cases5
				gen bar1 = cases1 / `total'  
				gen bar2 = cases2 / `total'  
				gen bar3 = cases3 / `total'  
				gen bar4 = cases4 / `total'  
				gen bar5 = cases5 / `total'  

				# delimit;
					graph bar (asis) bar5 bar4 bar3 bar2 bar1  , 
						stack
						yscale(off)
						bar(1, color ( `color5')) 
						bar(2, color ( `color4')) 
						bar(3, color ( `color3')) 
						bar(4, color ( `color2')) 
						bar(5, color ( `color1')) 
						ylabel(,nolabels noticks nogrid)
						legend(off)
						xsize(4)
						ysize(10)
						name(bar_`i', replace)
						graphregion(style(none) istyle(none))
						plotregion(style(none) istyle(none))
						;
						
				# delimit cr
				
				graph export "${inkbash}\pie_bar\temp\bar_`country_lab'_`sex_lab'_`i'.eps", as(eps) replace

				
				
				}

			use `temp_tot', replace
			replace rk_cases = rk_cases -1
			drop if rk_cases == 0
			merge m:1 cancer_code using "${dir_DATA}\_dict\cancer_color_2018.dta"
			keep if _m == 3
			drop _m 

			gsort type -rk 
			by type : egen tot=total(cases)
			by type  : gen pos = sum(cases)
			replace pos = pos - (cases/2) 
			replace pos = ((pos/tot)*312.001) + 98.582 - 7.2755
			replace pos = ((pos - 59.833)/1.33333)*(-1) 
			drop py color 
			gsort type rk
			keep cancer_label pos
			list
			outsheet using "${inkbash}\pie_bar\temp\cancer_label_`country_lab'_`sex_lab'.csv", comma replace

			
			use `temp_tot', replace

			quietly gen prop5 = 0 if rk == 1
			quietly replace prop5 = 1 if rk > 1
			gsort type +prop
			quietly collapse (sum) cases, by(type prop5)
			keep cases 
			outsheet using "${inkbash}\pie_bar\temp\cancer_number_`country_lab'_`sex_lab'.csv", comma replace
			

			
			*end
		}
	}

*end 


