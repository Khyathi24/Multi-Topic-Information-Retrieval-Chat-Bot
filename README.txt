# Working Instructions to use the finished product ?

- The app is built on streamlit which is a python library. The code for the data model is put in src folder which is inside phase3 folder.
1. To run the app  streamlit run streamlit_app.py  type the command inside src folder
	
- I have used only columns that are required to visualize the plots in respective pages. So the data load happens in main page, from here the required columns are passed to respective pages. Hence to visualize the plots firstly we need to run the main page which is streamlit and then move on to visualizations
2. Before checking visualizations, select streamlit page this would pass on the data to respective pages to visualize data. 
3. By clicking on the page name in side bar, the plots appear for the first three pages right after main page. The plots are dynamic and some are interactive, we can select the columns we want in x and y axis. 
4. For training we can either choose logistic or xgboost or both, parameters can be changed. The model trains after every change that is made and results can be seen on the screen.
5. Prediction page can be used to predict the review of the query, provide the details in the input boxes. In the backend the model just trained will predict the results for you.