import streamlit as st
from PIL import Image
import pandas as pd
from Rank_calculate import compute_point


def load_image(image_file):
	img = Image.open(image_file)
	return img


def comp_point_df(dataf, win, lose):
	iwin = dataf.index[dataf['Name'] == win].tolist()[0]
	ilose = dataf.index[dataf['Name'] == lose].tolist()[0]
	cur_win = dataf['Point'][iwin]
	cur_lose = dataf['Point'][ilose]
	new_win, new_lose = compute_point(cur_win, cur_lose)
	dataf.at[iwin, 'Point'] = int(new_win)
	dataf.at[ilose, 'Point'] = int(new_lose)
	dataf.sort_values(by='Point', ascending=False, inplace=True)
	return dataf


## Set icon
# icon = load_image('VECO.ico')
# st.set_page_config(
# 	page_title='VECO',
# 	page_icon=icon
# )

# Read Member's Score
num_mems = 3
spaces = 30
df = pd.read_csv("data.csv", encoding="windows-1252", low_memory=False, index_col=False)
df.set_index(pd.Index(list(range(1, num_mems + 1))), inplace=True)

# Admin accounts
password = 'badmintonislife'
with open('admin.txt', 'r') as file:
	admin_mode = file.read()
if admin_mode == 'Yes':
	st.title('Remember to exit admin mode at "Admin only"')

# Web API
menu = st.sidebar.selectbox('Option', ('Ranking', 'Announcements', 'Admin only'))
if menu == "Admin only":
	if admin_mode == 'Yes':
		st.text('You have enter admin mode')
		if st.button('Exit admin mode'):
			with open('admin.txt', 'w') as file:
				file.write('No')

	else:
		pass_input = st.text_input('Password')
		if pass_input and pass_input == password:
			with open('admin.txt', 'w') as file:
				file.write('Yes')
			st.text('You have enter admin mode')
		else:
			st.text('Wrong password')
elif menu == 'Ranking':
	st.header('Current Ranking')
	st.dataframe(df)
	if admin_mode == 'Yes':
		winner = st.text_input('Enter winner') + ' ' * spaces
		loser = st.text_input('Enter loser') + ' ' * spaces
		if winner != ' ' * spaces and loser != ' ' * spaces:
			df = comp_point_df(df, winner, loser)
			st.dataframe(df)
			df.to_csv("data.csv")
elif menu == 'Announcements':
	st.header('Announcements')
	with open('announcements.txt', 'r') as file:
		announces = file.read()
	st.text(announces)
	if admin_mode == 'Yes':
		st.text('ble')
		new_announce = '\n' + st.text_input('Add announcements')
		with open('announcements.txt', 'a') as file:
			file.write(new_announce)

