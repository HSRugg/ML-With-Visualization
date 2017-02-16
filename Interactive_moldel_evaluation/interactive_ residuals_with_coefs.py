import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Slider, RadioButtonGroup, Button, Label
from bokeh.io import show, curdoc
from bokeh.layouts import row, gridplot, widgetbox
from bokeh.sampledata.autompg import autompg as df
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle



			### get data into a Bokeh Dictionary ###


#Get the data from a pikled DataFrame
housing_train = pickle.load( open( "housing_train_full_df.p", "rb" ) )
saleprice = housing_train.pop('SalePrice')

#Scaled the Data
scaler = StandardScaler()
housing_train_scaled = scaler.fit_transform(housing_train)

#Put data in to ColumnDataSource.
source_all = ColumnDataSource(data=dict(x = housing_train,
                                        y = saleprice))

#Split the data 
X_train, X_test, y_train, y_test = train_test_split(source_all.data['x'],
							 source_all.data['y'], test_size=0.33, random_state=42)


#Put the split data in to ColumnDataSource.
source_trian = ColumnDataSource(data=dict(X_train = X_train,
                                            y_train = y_train))
source_test = ColumnDataSource(data=dict(X_test = X_test,
                                            y_test = y_test))

#Train model, and get predictions and residules
model = Ridge(alpha=1)
model.fit(source_trian.data['X_train'], source_trian.data['y_train'])
preds = model.predict(source_test.data['X_test'])
print preds.size, source_trian.data['X_train'].shape
residules = preds - y_test

#Get initile scores
r_score = model.score(source_test.data['X_test'], source_test.data['y_test'])
#Add the preds and residules to the test ColumnDataSource
source_test.add(preds.ravel(), name='preds')
source_test.add(residules.ravel(), name='residules')


#Get Coefs from model
coefs = model.coef_

#Put the coefs, and off sets for ploting into ColumnDataSource.
coefs = pd.Series(coefs)
coefs.sort_values(inplace=True)
coefs_y = [x + 1 for x, i in enumerate(coefs)]
x_off_set = [x/2.0 for x in coefs]
coefs = [x for x in coefs]

source_coefs= ColumnDataSource(data=dict(coefs = coefs,
                                          x_off_set = x_off_set,
                                          y = coefs_y))



		####   deffine wiget interactions ####


#set handler for new plit button:
# unpickles the selectaded file (these files should already be pandas DataFames)
#gets a new split of the currently selected data
#fits a model with the current alpha value
#updates scater data dictionarys.
#gets the new coefs, sorts them, creats offsets for rect plot and updatas dictonayr
#gets the score and updates plot
def my_radio_handler(new):
	if new == 0:
		print "Trigered if 0"
		housing_train = pickle.load( open( "housing_train_full_df.p", "rb" ))
		saleprice = housing_train.pop('SalePrice')
		source_all.data = dict(x = housing_train,
		                		y = saleprice)
	elif new == 1:
		Housing_train_df_imputed_lotFrontage = pickle.load( open( "Housing_train_just_mean_impute.p", "rb" ) )
		saleprice = Housing_train_df_imputed_lotFrontage.pop('SalePrice')
		source_all.data = dict(x = Housing_train_df_imputed_lotFrontage,
		                		y = saleprice)
	elif new == 2:
		Housing_train_df_loged_75up = pickle.load( open( "Housing_train_df_loged_75up.p", "rb" ) )
		saleprice = Housing_train_df_loged_75up.pop('SalePrice')
		source_all.data = dict(x = Housing_train_df_loged_75up,
		                		y = saleprice)
	

	X_train, X_test, y_train, y_test = train_test_split(source_all.data['x'],
	 source_all.data['y'], test_size=0.33)
	model = Ridge(alpha = alpha_slider.value)
	model.fit(X_train, y_train)
	preds = model.predict(X_test)
	residules = preds - y_test

	#source_test.add(preds.ravel(), name='preds')
	#source_test.add(residules.ravel(), name='residules')
	print type(source_test.data['preds'])
	print source_test.data['preds'][2]
	source_test.data = dict(X_test = X_test,
							y_test = y_test,
							preds = preds.ravel(),
							residules = residules.ravel())
	print source_test.data['preds'][2]

	#Get Coefs from model
	coefs = model.coef_

	#Put the coefs, and off sets for ploting into ColumnDataSource.
	coefs     = pd.Series(coefs)
	coefs.sort_values(inplace=True)
	coefs_y   = [x + 1 for x, i in enumerate(coefs)]
	x_off_set = [x/2.0 for x in coefs]
	coefs     = [x for x in coefs]

	source_coefs.data = dict(coefs     = coefs,
	                         x_off_set = x_off_set,
	                         y         = coefs_y)
	r_score = model.score(X_test, y_test)
	plot.title.text = "True Values VS Predicted Values r^2 =    " + str(r_score)


#set handler for new plit button:
#gets a new split of the currently selected data
#fits a model with the current alpha value
#updates scater data dictionarys.
#gets the new coefs, sorts them, creats offsets for rect plot and updatas dictonayr
#gets the score and updates plot
def get_new_split():
	X_train, X_test, y_train, y_test = train_test_split(source_all.data['x'],
	 source_all.data['y'], test_size=0.33)
	model = Ridge(alpha = alpha_slider.value)
	model.fit(X_train, y_train)
	preds = model.predict(X_test)
	residules = preds - y_test
	source_test.data = dict(X_test = X_test,
							y_test = y_test,
							preds = preds.ravel(),
							residules = residules.ravel())
	

	#Get Coefs from model
	coefs = model.coef_

	#Put the coefs, and off sets for ploting into ColumnDataSource.
	coefs     = pd.Series(coefs)
	coefs.sort_values(inplace=True)
	coefs_y   = [x + 1 for x, i in enumerate(coefs)]
	x_off_set = [x/2.0 for x in coefs]
	coefs     = [x for x in coefs]

	source_coefs.data = dict(coefs     = coefs,
	                         x_off_set = x_off_set,
	                         y         = coefs_y)
	r_score = model.score(X_test, y_test)
	plot.title.text = "True Values VS Predicted Values r^2 =    " + str(r_score)

 	

#set handler for alpha slider:
#fits a new modle with curent alpha value on the same data 
#updates scater data dictionarys.
#gets the new coefs, sorts them, creats offsets for rect plot and updatas dictonayr
#gets the score and updates plot
def ridge_alpha_handler(attrname, old, new):
	model = Ridge(alpha = alpha_slider.value)
	model.fit(source_trian.data['X_train'], source_trian.data['y_train'])
	preds = model.predict(source_test.data['X_test'])
	residules = preds - source_test.data['y_test']
	source_test.add(preds.ravel(), name='preds')
	source_test.add(residules.ravel(), name='residules')
	source_test.data = dict(X_test = X_test,
	                        y_test = y_test,
	                        preds = preds.ravel(),
	                        residules = residules.ravel())


	#Get Coefs from model
	coefs = model.coef_

	#Put the coefs, and off sets for ploting into ColumnDataSource.
	coefs = pd.Series(coefs)
	coefs.sort_values(inplace=True)
	coefs_y = [x + 1 for x, i in enumerate(coefs)]
	x_off_set = [x/2.0 for x in coefs]
	coefs = [x for x in coefs]

	source_coefs.data = dict(coefs = coefs,
	                         x_off_set = x_off_set,
	                         y = coefs_y)
	r_score = model.score(X_test, y_test)
	plot.title.text = "True Values VS Predicted Values r^2 = " + str(r_score)

    

		#####   Make widgets ####


radio_button_group = RadioButtonGroup(
        labels=["Starting", "After Imputation", "Loged"], active=0)
radio_button_group.on_click(my_radio_handler)

new_split_button = Button(label="New Split (Press Me To Start)", button_type="success")
new_split_button.on_click(get_new_split)

alpha_slider     = Slider(title="Ridge Alpha", value=1, start=1.0, end=1500.0, step=1)
alpha_slider.on_change('value', ridge_alpha_handler)


		#####   Make plots ####


plot = figure(title="True Values VS Predicted Values    r^2 =    " + str(r_score),
 x_range=(10, 14), y_range=(10, 14), width=450, height=450)
plot.xaxis.axis_label = "Predicted Values"
plot.yaxis.axis_label = "True Values"
plot2 = figure(title="True Values VS Risidule Values",
 x_range=(-4, 4), y_range = plot.y_range, width=450, height=450)
plot2.xaxis.axis_label = "Diffrence Between True and Predicted Values"

plot_coefs = figure(title="Coefs",
width=350, height=450)


#Prediction plots
plot.circle('preds' ,'y_test', source=source_test)
plot.line([10,14],[10,14], color='red')
plot2.circle('residules' ,'y_test', source=source_test)
plot2.line([0,0],[10,14], color='red')

#coef plot
plot_coefs.rect('x_off_set', 'y', 'coefs', .4, source=source_coefs)





		###  Set up layout and show  ###



rb_wb = widgetbox([radio_button_group])

wb = widgetbox([alpha_slider], width=800)

grid = gridplot([[rb_wb, new_split_button], [plot, plot2, plot_coefs],[wb]])
curdoc().add_root(grid)






